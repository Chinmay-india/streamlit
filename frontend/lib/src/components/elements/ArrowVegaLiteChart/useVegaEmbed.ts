/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { RefObject, useCallback, useRef, useState } from "react"

import { truthy, View as VegaView } from "vega"
import embed from "vega-embed"
import { expressionInterpreter } from "vega-interpreter"

import { WidgetStateManager } from "@streamlit/lib/src/WidgetStateManager"
import { Quiver } from "@streamlit/lib/src/dataframes/Quiver"
import { ensureError } from "@streamlit/lib/src/util/ErrorHandling"
import { logMessage, logWarning } from "@streamlit/lib/src/util/log"
import { notNullOrUndefined } from "@streamlit/lib/src/util/utils"

import {
  dataIsAnAppendOfPrev,
  getDataArray,
  getDataArrays,
  getDataSets,
  getInlineData,
  VegaLiteChartElement,
  WrappedNamedDataset,
} from "./arrowUtils"
import { useVegaLiteSelections } from "./useVegaLiteSelection"

const DEFAULT_DATA_NAME = "source"

interface UseVegaEmbedOutput {
  error: Error | null
  createView: (
    containerRef: RefObject<HTMLDivElement>,
    spec: any
  ) => Promise<VegaView | null>
  updateView: (
    data: Quiver | null,
    datasets: WrappedNamedDataset[]
  ) => Promise<VegaView | null>
  finalizeView: () => void
}

export function useVegaEmbed(
  inputElement: VegaLiteChartElement,
  widgetMgr: WidgetStateManager,
  fragmentId?: string
): UseVegaEmbedOutput {
  const vegaView = useRef<VegaView | null>(null)
  const vegaFinalizer = useRef<(() => void) | null>(null)
  const defaultDataName = useRef<string>(DEFAULT_DATA_NAME)
  const dataRef = useRef<Quiver | null>(null)
  const datasetsRef = useRef<WrappedNamedDataset[]>([])
  const [error, setError] = useState<Error | null>(null)

  // This hook is responsible for providing the setup function for selections in the chart
  const maybeConfigureSelections = useVegaLiteSelections(
    inputElement,
    widgetMgr,
    fragmentId
  )

  const { id: chartId } = inputElement

  const finalizeView = useCallback(() => {
    if (vegaFinalizer.current) {
      vegaFinalizer.current()
    }

    vegaFinalizer.current = null
    vegaView.current = null
  }, [])

  const createView = useCallback(
    async (
      containerRef: RefObject<HTMLDivElement>,
      element: VegaLiteChartElement
    ): Promise<VegaView | null> => {
      try {
        logMessage("Creating a new Vega view.")

        if (containerRef.current === null) {
          throw new Error("Element missing.")
        }

        // Finalize the previous view so it can be garbage collected.
        finalizeView()

        const options = {
          // Adds interpreter support for Vega expressions that is compliant with CSP
          ast: true,
          expr: expressionInterpreter,

          // Disable default styles so that vega doesn't inject <style> tags in the
          // DOM. We set these styles manually for finer control over them and to
          // avoid inlining styles.
          tooltip: { disableDefaultStyle: true },
          defaultStyle: false,
          forceActionsMenu: true,
        }

        const { vgSpec, view, finalize } = await embed(
          containerRef.current,
          element.spec,
          options
        )

        vegaView.current = view

        maybeConfigureSelections(view)

        vegaFinalizer.current = finalize

        // Try to load the previous state of the chart from the element state.
        // This is useful to restore the selection state when the component is re-mounted
        // or when its put into fullscreen mode.
        const viewState = widgetMgr.getElementState(chartId, "viewState")
        if (notNullOrUndefined(viewState)) {
          try {
            vegaView.current = view.setState(viewState)
          } catch (e) {
            logWarning("Failed to restore view state", e)
          }
        }

        const dataArrays = getDataArrays(
          element.datasets as WrappedNamedDataset[]
        )

        // Heuristic to determine the default dataset name.
        const datasetNames = dataArrays ? Object.keys(dataArrays) : []
        if (datasetNames.length === 1) {
          const [datasetName] = datasetNames
          defaultDataName.current = datasetName
        } else if (datasetNames.length === 0 && vgSpec.data) {
          defaultDataName.current = DEFAULT_DATA_NAME
        }

        const dataObj = getInlineData(element.data as Quiver | null)
        if (dataObj) {
          vegaView.current.insert(defaultDataName.current, dataObj)
        }
        if (dataArrays) {
          for (const [name, data] of Object.entries(dataArrays)) {
            vegaView.current.insert(name, data)
          }
        }

        datasetsRef.current = element.datasets
        dataRef.current = element.data

        await vegaView.current.runAsync()

        // Fix bug where the "..." menu button overlaps with charts where width is
        // set to -1 on first load.
        await vegaView.current.resize().runAsync()

        return vegaView.current
      } catch (e) {
        setError(ensureError(e))
        return null
      }
    },
    [chartId, finalizeView, maybeConfigureSelections, widgetMgr]
  )

  const updateData = useCallback(
    (name: string, prevData: Quiver | null, data: Quiver | null): void => {
      if (!vegaView.current) {
        return
      }

      if (!data || data.data.numRows === 0) {
        // The new data is empty, so we remove the dataset from the
        // chart view if the named dataset exists.
        try {
          vegaView.current.remove(name, truthy)
        } finally {
          return
        }
      }

      if (!prevData || prevData.data.numRows === 0) {
        // The previous data was empty, so we just insert the new data.
        vegaView.current.insert(name, getDataArray(data))
        return
      }

      const { dataRows: prevNumRows, dataColumns: prevNumCols } =
        prevData.dimensions
      const { dataRows: numRows, dataColumns: numCols } = data.dimensions

      // Check if dataframes have same "shape" but the new one has more rows.
      if (
        dataIsAnAppendOfPrev(
          prevData,
          prevNumRows,
          prevNumCols,
          data,
          numRows,
          numCols
        )
      ) {
        if (prevNumRows < numRows) {
          // Insert the new rows.
          vegaView.current.insert(name, getDataArray(data, prevNumRows))
        }
      } else {
        // Clean the dataset and insert from scratch.
        vegaView.current.data(name, getDataArray(data))
        logMessage(
          `Had to clear the ${name} dataset before inserting data through Vega view.`
        )
      }
    },
    []
  )

  const updateView = useCallback(
    async (
      inputData: Quiver | null,
      inputDatasets: WrappedNamedDataset[]
    ): Promise<VegaView | null> => {
      // At this point the previous data should be updated
      const prevData = dataRef.current
      const prevDatasets = datasetsRef.current

      if (dataRef.current || inputData) {
        updateData(defaultDataName.current, prevData, inputData)
      }

      const prevDataSets = getDataSets(prevDatasets) ?? {}
      const dataSets = getDataSets(inputDatasets) ?? {}

      for (const [name, dataset] of Object.entries(dataSets)) {
        const datasetName = name || defaultDataName.current
        const prevDataset = prevDataSets[datasetName]

        updateData(datasetName, prevDataset, dataset)
      }

      // Remove all datasets that are in the previous but not the current datasets.
      for (const name of Object.keys(prevDataSets)) {
        if (
          !dataSets.hasOwnProperty(name) &&
          name !== defaultDataName.current
        ) {
          updateData(name, null, null)
        }
      }

      await vegaView.current?.resize().runAsync()

      dataRef.current = inputData

      datasetsRef.current = inputDatasets

      return vegaView.current
    },
    [updateData]
  )

  return { error, createView, updateView, finalizeView }
}
