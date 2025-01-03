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

import React from "react"

import { DataEditorProps } from "@glideapps/glide-data-grid"

import { BaseColumn } from "@streamlit/lib/src/components/widgets/DataFrame/columns"

type ColumnInteractivityReturn = Pick<DataEditorProps, "onColumnMoved">

/**
 * A React hook that provides features to interact with columns from UI.
 *
 * @param columns - The columns of the table.
 * @param freezeColumns - The number of columns to freeze.
 * @param clearSelection - A callback to clear current selections in the table.
 * @param setColumnConfigMapping - A callback to set the column config mapping.
 * @param setColumnOrder - A callback to set the column order.
 *
 * @returns An object containing the following properties:
 * - `onColumnMoved`: A callback to handle column movement.
 */
function useColumnMove(
  columns: BaseColumn[],
  freezeColumns: number,
  pinColumn: (columnName: string) => void,
  unpinColumn: (columnName: string) => void,
  setColumnOrder: React.Dispatch<React.SetStateAction<string[]>>
): ColumnInteractivityReturn {
  const onColumnMoved = React.useCallback(
    (startIndex: number, endIndex: number): void => {
      // Create a shallow copy of the original columns
      const newColumns = [...columns]

      // Remove the column from its original position
      const [movedColumn] = newColumns.splice(startIndex, 1)

      // Insert the column into its new position
      newColumns.splice(endIndex, 0, movedColumn)

      // Pin or unpin the column if necessary:
      if (endIndex < freezeColumns && !movedColumn.isPinned) {
        pinColumn(movedColumn.name)
      } else if (endIndex >= freezeColumns && movedColumn.isPinned) {
        unpinColumn(movedColumn.name)
      }

      // Update the column order with the new sequence of column names
      setColumnOrder(newColumns.map(column => column.name))
    },
    [columns, freezeColumns, pinColumn, unpinColumn, setColumnOrder]
  )

  return {
    onColumnMoved,
  }
}

export default useColumnMove
