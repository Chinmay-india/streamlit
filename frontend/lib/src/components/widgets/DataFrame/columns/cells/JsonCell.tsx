/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
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

import * as React from "react"

import JSON5 from "json5"
import { getLuminance } from "color2k"
import {
  type CustomCell,
  type CustomRenderer,
  drawTextCell,
  GridCellKind,
  type ProvideEditorCallback,
  TextCell,
  TextCellEntry,
} from "@glideapps/glide-data-grid"
import ReactJson from "react-json-view"

import { isNullOrUndefined } from "@streamlit/utils"

import { toSafeString } from "~lib/components/widgets/DataFrame/columns/utils"

export function toJsonString(
  value: string | object | undefined | null
): string {
  if (typeof value === "string") {
    return value
  }
  try {
    return JSON.stringify(value)
  } catch (error) {
    return toSafeString(value)
  }
}

interface JsonViewerProps {
  jsonValue: string | object | undefined | null
  theme: any
}

/**
 * A component to be used in cell overlay (editor) that is able to display
 * JSON values in a nice JSON-viewer.
 *
 * If the value cannot be parsed into a JSON object, the value will be displayed
 * as raw text.
 **/
const JsonViewer: React.FC<JsonViewerProps> = ({ jsonValue, theme }) => {
  let parsedJson = undefined
  try {
    if (jsonValue) {
      parsedJson =
        typeof jsonValue === "string"
          ? JSON5.parse(jsonValue)
          : JSON5.parse(JSON5.stringify(jsonValue))
    }
  } catch (error) {
    parsedJson = undefined
  }

  if (isNullOrUndefined(parsedJson)) {
    return (
      <TextCellEntry
        highlight={true}
        autoFocus={false}
        disabled={true}
        value={toJsonString(jsonValue) ?? ""}
        onChange={() => undefined}
      />
    )
  }

  return (
    <div style={{ padding: theme.cellHorizontalPadding }}>
      <ReactJson
        src={parsedJson}
        collapsed={2}
        theme={getLuminance(theme.bgCell) > 0.5 ? "rjv-default" : "monokai"}
        displayDataTypes={false}
        displayObjectSize={false}
        name={false}
        enableClipboard={true}
        style={{
          fontFamily: theme.fontFamily,
          fontSize: theme.baseFontStyle,
          backgroundColor: theme.bgCell,
          whiteSpace: "pre-wrap", // preserve whitespace
        }}
      />
    </div>
  )
}

interface JsonCellProps {
  readonly kind: "json-cell"
  /* The JSON string data or object to display. */
  readonly value: string | object | undefined | null
  /* The stringified JSON to display. */
  readonly displayValue?: string
}

export type JsonCell = CustomCell<JsonCellProps>

/**
 * The cell overlay editor used by JSON columns to render
 * the value in a JSON-viewer.
 *
 * Note: this "editor" does not actually support editing at
 * the moment.
 */
export const JsonCellEditor: ReturnType<
  ProvideEditorCallback<JsonCell>
> = cell => {
  const theme = cell.theme
  const cellData = cell.value.data

  return (
    <JsonViewer
      jsonValue={cellData.value || cellData.displayValue}
      theme={theme}
    />
  )
}

/**
 * The cell overlay editor that is configured as custom editor to render
 * all text cell values that look like JSON.
 *
 * This is configured in the useCustomEditors hook.
 *
 * Note: this "editor" does not actually support editing at
 * the moment.
 */
export const JsonTextCellEditor: ReturnType<
  ProvideEditorCallback<TextCell>
> = cell => {
  const theme = cell.theme
  const cellData = cell.value

  return <JsonViewer jsonValue={cellData.data} theme={theme} />
}

/**
 * The full JSON cell renderer used by the JSON column.
 * This is configured in the useCustomRenderer hook.
 */
const renderer: CustomRenderer<JsonCell> = {
  kind: GridCellKind.Custom,
  isMatch: (c): c is JsonCell => (c.data as any).kind === "json-cell",
  draw: (args, cell) => {
    const { value, displayValue } = cell.data
    drawTextCell(
      args,
      displayValue ?? toJsonString(value) ?? "",
      cell.contentAlign
    )
    return true
  },
  measure: (ctx, cell, theme) => {
    const { value, displayValue } = cell.data
    const displayText = displayValue ?? toJsonString(value) ?? ""
    return (
      (displayText ? ctx.measureText(displayText).width : 0) +
      theme.cellHorizontalPadding * 2
    )
  },
  provideEditor: () => ({
    editor: JsonCellEditor,
  }),
}

export default renderer
