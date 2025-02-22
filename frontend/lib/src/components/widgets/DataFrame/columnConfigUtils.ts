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

import { ColumnConfigProps } from "./hooks/useColumnLoader"

/**
 * Updates an existing column config mapping with the new type props.
 *
 * @param columnId - The id of the column to update.
 * @param columnConfigMapping - The column config mapping to update.
 * @param updatedTypeProps - The new type props to update the column config with.
 */
export const updateColumnConfigTypeProps = ({
  columnId,
  columnConfigMapping,
  updatedProps,
}: {
  columnId: string
  columnConfigMapping: Map<string, ColumnConfigProps>
  updatedProps?: ColumnConfigProps
}): Map<string, ColumnConfigProps> => {
  const newColumnConfigMapping = new Map(columnConfigMapping)
  const existingConfig = newColumnConfigMapping.get(columnId)
  newColumnConfigMapping.set(columnId, {
    ...(existingConfig || {}),
    // update other props but not type config:
    ...(updatedProps || {}),
    // update type-specific config:
    type_config: {
      ...(existingConfig?.type_config || {}),
      ...(updatedProps?.type_config || {}),
    },
  })
  return newColumnConfigMapping
}
