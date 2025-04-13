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

import { describe, expect, it } from "vitest"

import {
  getWidth,
  isNumber,
  getHeight,
  getFlex,
  getVerticalScroll,
} from "./useLayoutStyles"

describe("#isNumber", () => {
  it.each([
    [42, true],
    [0, true],
    [-100, true],
    [1.0, true],
    ["42", true],
    ["0", true],
    ["-100", true],
    ["3.14", true],
    ["stretch", false],
    ["content", false],
    ["123abc", false],
    ["NaN", false],
    ["", false],
    [" ", false],
    [undefined, false],
    [null, false],
  ])("isNumber(%p) should return %s", (value, expected) => {
    expect(isNumber(value)).toBe(expected)
  })
})

describe("#getWidth", () => {
  it.each([
    // When useContainerWidth is true - returns containerWidth or "100%"
    [true, "300", 800, 800],
    [true, "stretch", 800, 800],
    [true, "content", 800, 800],
    [true, null, 800, 800],
    [true, "300", "200", "200"],
    [true, "300", undefined, "100%"],

    // When commandWidth is numeric - should append 'px'
    [false, "200", 800, "200px"],
    [false, "1000", 800, "1000px"],

    // When commandWidth is special value
    [false, "stretch", 800, "100%"],
    [false, "content", 800, "fit-content"],

    // When commandWidth is invalid - return "auto"
    [false, "0", 800, "auto"],
    [false, null, 800, "auto"],
    [false, undefined, 800, "auto"],
    [false, "invalid", 800, "auto"],
  ])(
    "getWidth(%s, %p, %p) should return %p",
    (useContainerWidth, commandWidth, containerWidth, expected) => {
      expect(getWidth(useContainerWidth, commandWidth, containerWidth)).toBe(
        expected
      )
    }
  )
})

describe("#getHeight", () => {
  it.each([
    ["stretch", "auto"],
    ["content", "fit-content"],
    ["200", "200px"],
    ["0", "auto"],
    ["1000", "1000px"],
    [null, "auto"],
    [undefined, "auto"],
    ["invalid", "auto"],
  ])("when commandHeight is %s, returns %s", (commandHeight, expected) => {
    expect(getHeight(commandHeight)).toBe(expected)
  })
})

describe("#getFlex", () => {
  it.each([
    // When useContainerWidth is true
    [true, undefined, undefined, 500, undefined, 1, "1 1 500px"],
    [true, undefined, undefined, "100%", undefined, 1, "1 1 100%"],
    [true, undefined, undefined, undefined, undefined, 1, undefined],

    // When commandWidth is "stretch"
    [false, "stretch", undefined, 500, "row", 2, "2"],
    [false, "stretch", undefined, 500, "row", 0.5, "0.5"],
    [false, "content", "stretch", 500, "row", 1, undefined],
    [false, "stretch", undefined, undefined, "row", undefined, undefined],

    // When commandHeight is "stretch"
    [false, undefined, "stretch", 500, "column", 2, "2"],
    [false, undefined, "stretch", 500, "column", 0.5, "0.5"],
    [false, "stretch", "content", 500, "column", 1, undefined],
    [false, undefined, "stretch", undefined, "column", undefined, undefined],

    // When commandWidth is numeric
    [false, "200", undefined, 500, "row", undefined, "0 1 200px"],
    [false, undefined, "200", 500, "row", undefined, undefined],

    // When commandHeight is numeric
    [false, undefined, "200", 500, "column", undefined, "0 1 200px"],
    [false, "200", undefined, 500, "column", undefined, undefined],

    // Edge cases that should return undefined
    [false, undefined, undefined, undefined, undefined, undefined, undefined],
  ])(
    "getFlex(%s, %p, %p, %p, %p, %p) should return %p",
    (
      useContainerWidth,
      commandWidth,
      commandHeight,
      containerWidth,
      direction,
      scale,
      expected
    ) => {
      expect(
        getFlex(
          useContainerWidth,
          commandWidth,
          commandHeight,
          containerWidth,
          direction as "row" | "column" | undefined,
          scale
        )
      ).toBe(expected)
    }
  )
})

describe("#getVerticalScroll", () => {
  it.each([
    // Positive numbers should return true
    ["100", true],
    ["1", true],
    ["0.1", true],

    // Zero or negative numbers should return false
    ["0", false],
    ["-10", false],
    ["-0.5", false],

    // Non-numeric strings should return false
    ["auto", false],
    ["stretch", false],
    ["content", false],
    ["invalid", false],
    ["", false],
    [" ", false],

    // null and undefined should return false
    [null, false],
    [undefined, false],
  ])("getVerticalScroll(%p) should return %s", (height, expected) => {
    expect(getVerticalScroll(height)).toBe(expected)
  })
})
