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
import { renderHook } from "@testing-library/react"

import { streamlit } from "@streamlit/protobuf"
import { useLayoutStyles } from "./useLayoutStyles"

describe("#useLayoutStyles", () => {
  describe("with an element", () => {
    describe("that has useContainerWidth set to a falsy value", () => {
      const useContainerWidth = false

      it.each([
        [undefined, { width: "auto" }],
        [0, { width: "auto" }],
        [-100, { width: "auto" }],
        [NaN, { width: "auto" }],
        [100, { width: 100 }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = { width, useContainerWidth }
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })

    describe('that has useContainerWidth set to "true"', () => {
      const useContainerWidth = true

      it.each([
        [undefined, { width: "100%" }],
        [0, { width: "100%" }],
        [-100, { width: "100%" }],
        [NaN, { width: "100%" }],
        [100, { width: "100%" }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = { width, useContainerWidth }
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })

    describe("that is an image list", () => {
      const useContainerWidth = false

      it.each([
        [undefined, { width: "100%" }],
        [0, { width: "100%" }],
        [-100, { width: "100%" }],
        [NaN, { width: "100%" }],
        [100, { width: "100%" }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = { width, useContainerWidth, imgs: [] }
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })

    describe("that has widthType set", () => {
      it.each([
        [streamlit.Width.STRETCH, false, { width: "100%" }],
        [streamlit.Width.STRETCH, true, { width: "100%" }],
        [streamlit.Width.CONTENT, false, { width: "auto" }],
        [streamlit.Width.CONTENT, true, { width: "100%" }],
        [streamlit.Width.PIXEL, false, { width: "auto" }],
        [streamlit.Width.PIXEL, true, { width: "100%" }],
      ])(
        "and with a widthType value of %s and useContainerWidth %s, returns %o",
        (widthType, useContainerWidth, expected) => {
          const element = { widthType, useContainerWidth }
          const { result } = renderHook(() => useLayoutStyles({ element }))
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("that has widthType set to PIXEL with pixelWidth", () => {
      it.each([
        [0, false, { width: "auto" }],
        [-100, false, { width: "auto" }],
        [NaN, false, { width: "auto" }],
        [100, false, { width: 100 }],
        [0, true, { width: "100%" }],
        [-100, true, { width: "100%" }],
        [NaN, true, { width: "100%" }],
        [100, true, { width: "100%" }],
      ])(
        "and with a pixelWidth value of %s and useContainerWidth %s, returns %o",
        (pixelWidth, useContainerWidth, expected) => {
          const element = {
            widthType: streamlit.Width.PIXEL,
            pixelWidth,
            useContainerWidth,
          }
          const { result } = renderHook(() => useLayoutStyles({ element }))
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("with variations on element", () => {
      it.each([
        [{ widthType: 999, useContainerWidth: false }, { width: "auto" }],
        [{ widthType: 999, useContainerWidth: true }, { width: "100%" }],
      ])("and with element %o, returns %o", (element, expected) => {
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })

    describe("with width included along with widthType and pixelWidth", () => {
      it.each([
        [
          {
            widthType: streamlit.Width.STRETCH,
            width: 100,
            pixelWidth: 200,
            useContainerWidth: false,
          },
          { width: "100%" },
        ],
        [
          {
            widthType: streamlit.Width.CONTENT,
            width: 100,
            pixelWidth: 200,
            useContainerWidth: false,
          },
          { width: "auto" },
        ],
        [
          {
            widthType: streamlit.Width.PIXEL,
            width: 100,
            pixelWidth: 200,
            useContainerWidth: false,
          },
          { width: 200 },
        ],
        [
          {
            widthType: streamlit.Width.PIXEL,
            width: 100,
            pixelWidth: 200,
            useContainerWidth: true,
          },
          { width: "100%" },
        ],
        [
          {
            widthType: streamlit.Width.PIXEL,
            width: 100,
            pixelWidth: 0,
            useContainerWidth: false,
          },
          { width: "auto" },
        ],
        [
          {
            widthType: streamlit.Width.PIXEL,
            width: 100,
            pixelWidth: -100,
            useContainerWidth: false,
          },
          { width: "auto" },
        ],
        [
          {
            widthType: streamlit.Width.PIXEL,
            width: 100,
            pixelWidth: NaN,
            useContainerWidth: false,
          },
          { width: "auto" },
        ],
      ])("and with element %o, returns %o", (element, expected) => {
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })
  })
})
