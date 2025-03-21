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

/**
 * Convert a mask pattern to a regular expression
 * @param mask The mask pattern (e.g., "999-aa-**")
 */
const maskToRegex = (mask: string): RegExp => {
  const pattern = mask
    .replace(/[.+?^${}()|[\]\\]/g, "\\$&") // Escape regex special chars
    .replace(/9/g, "\\d") // 9 -> digits
    .replace(/a/gi, "[A-Za-z]") // a/A -> letters
    .replace(/\*/g, "[A-Za-z\\d]") // * -> alphanumeric

  return new RegExp(`^${pattern}$`)
}

/**
 * Check if a value matches the given mask pattern
 * @param value The value to validate
 * @param mask The mask pattern to validate against
 */
export const isValidMaskedValue = (value: string, mask: string): boolean => {
  if (!mask || !value) return true
  const regex = maskToRegex(mask)
  return regex.test(value)
}
