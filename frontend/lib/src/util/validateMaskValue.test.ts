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

import { isValidMaskedValue } from "./validateMaskValue"

describe("validateMaskValue", () => {
  describe("isValidMaskedValue", () => {
    it("should return true for empty mask or value", () => {
      expect(isValidMaskedValue("", "")).toBe(true)
      expect(isValidMaskedValue("123", "")).toBe(true)
      expect(isValidMaskedValue("", "999")).toBe(true)
    })

    it("should validate digit patterns correctly", () => {
      expect(isValidMaskedValue("123", "999")).toBe(true)
      expect(isValidMaskedValue("12a", "999")).toBe(false)
      expect(isValidMaskedValue("1234", "999")).toBe(false)
      expect(isValidMaskedValue("12", "999")).toBe(false)
    })

    it("should validate letter patterns correctly", () => {
      expect(isValidMaskedValue("abc", "aaa")).toBe(true)
      expect(isValidMaskedValue("ABC", "aaa")).toBe(true)
      expect(isValidMaskedValue("ab1", "aaa")).toBe(false)
      expect(isValidMaskedValue("abcd", "aaa")).toBe(false)
    })

    it("should validate alphanumeric patterns correctly", () => {
      expect(isValidMaskedValue("1a2", "***")).toBe(true)
      expect(isValidMaskedValue("ABC", "***")).toBe(true)
      expect(isValidMaskedValue("123", "***")).toBe(true)
      expect(isValidMaskedValue("@#$", "***")).toBe(false)
    })

    it("should handle complex patterns", () => {
      expect(isValidMaskedValue("123-AB-4c", "999-aa-**")).toBe(true)
      expect(isValidMaskedValue("12A-AB-4c", "999-aa-**")).toBe(false)
      expect(isValidMaskedValue("123-12-4c", "999-aa-**")).toBe(false)
    })

    it("should handle escaped special characters", () => {
      expect(isValidMaskedValue("(123) 456-7890", "(999) 999-9999")).toBe(true)
      expect(isValidMaskedValue("123-456-7890", "999-999-9999")).toBe(true)
      expect(isValidMaskedValue("(abc) def-ghij", "(999) 999-9999")).toBe(
        false
      )
    })

    it("should validate phone number formats", () => {
      expect(isValidMaskedValue("(123) 456-7890", "(999) 999-9999")).toBe(true)
      expect(isValidMaskedValue("(123) 456 7890", "(999) 999 9999")).toBe(true)
      expect(isValidMaskedValue("123.456.7890", "999.999.9999")).toBe(true)
    })

    it("should validate dates", () => {
      expect(isValidMaskedValue("01/01/2023", "99/99/9999")).toBe(true)
      expect(isValidMaskedValue("2023-01-01", "9999-99-99")).toBe(true)
      expect(isValidMaskedValue("01-Jan-23", "99-aaa-99")).toBe(true)
    })
  })
})
