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

import { Element, IAlert, streamlit } from "@streamlit/protobuf"

import { useLayoutStyles } from "./useLayoutStyles"

class MockElement {
  widthConfig?: streamlit.WidthConfig

  heightConfig?: streamlit.HeightConfig

  type?: string

  constructor(props: Partial<MockElement> = {}) {
    Object.assign(this, props)
  }

  toJSON() {
    return this
  }
}

describe("#useLayoutStyles", () => {
  describe("with an element", () => {
    describe("that has useContainerWidth set to a falsy value", () => {
      const useContainerWidth = false

      it.each([
        [undefined, { width: "auto", height: "auto" }],
        [0, { width: "auto", height: "auto" }],
        [-100, { width: "auto", height: "auto" }],
        [NaN, { width: "auto", height: "auto" }],
        [100, { width: 100, height: "auto" }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = new MockElement() as Element
        const subElement = { width, useContainerWidth }
        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe('that has useContainerWidth set to "true"', () => {
      const useContainerWidth = true

      it.each([
        [undefined, { width: "100%", height: "auto" }],
        [0, { width: "100%", height: "auto" }],
        [-100, { width: "100%", height: "auto" }],
        [NaN, { width: "100%", height: "auto" }],
        [100, { width: "100%", height: "auto" }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = new MockElement() as Element
        const subElement = { width, useContainerWidth }
        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe("that is an image list", () => {
      const useContainerWidth = false

      it.each([
        [undefined, { width: "100%", height: "auto" }],
        [0, { width: "100%", height: "auto" }],
        [-100, { width: "100%", height: "auto" }],
        [NaN, { width: "100%", height: "auto" }],
        [100, { width: "100%", height: "auto" }],
      ])("and with a width value of %s, returns %o", (width, expected) => {
        const element = new MockElement({ type: "imgs" }) as Element
        const subElement = { width, useContainerWidth }
        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe("that has widthConfig set", () => {
      it.each([
        [
          new streamlit.WidthConfig({ useStretch: true }),
          false,
          { width: "100%", height: "auto" },
        ],
        [
          new streamlit.WidthConfig({ useStretch: true }),
          true,
          { width: "100%", height: "auto" },
        ],
        [
          new streamlit.WidthConfig({ useContent: true }),
          false,
          { width: "fit-content", height: "auto" },
        ],
        [
          new streamlit.WidthConfig({ useContent: true }),
          true,
          { width: "100%", height: "auto" },
        ],
        [
          new streamlit.WidthConfig({ pixelWidth: 100 }),
          false,
          { width: 100, height: "auto" },
        ],
        [
          new streamlit.WidthConfig({ pixelWidth: 100 }),
          true,
          { width: "100%", height: "auto" },
        ],
      ])(
        "and with a widthConfig value of %o and useContainerWidth %s, returns %o",
        (widthConfig, useContainerWidth, expected) => {
          const element = new MockElement({ widthConfig }) as Element
          const subElement = { useContainerWidth }
          const { result } = renderHook(() =>
            useLayoutStyles({ element, subElement })
          )
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("that has widthConfig set to invalid pixelWidth values", () => {
      it.each([
        [0, false, { width: "auto", height: "auto" }],
        [-100, false, { width: "auto", height: "auto" }],
        [NaN, false, { width: "auto", height: "auto" }],
        [100, false, { width: 100, height: "auto" }],
        [0, true, { width: "100%", height: "auto" }],
        [-100, true, { width: "100%", height: "auto" }],
        [NaN, true, { width: "100%", height: "auto" }],
        [100, true, { width: "100%", height: "auto" }],
      ])(
        "and with a pixelWidth value of %s and useContainerWidth %s, returns %o",
        (pixelWidth, useContainerWidth, expected) => {
          const element = new MockElement({
            widthConfig: new streamlit.WidthConfig({ pixelWidth }),
          }) as Element
          const subElement = { useContainerWidth }
          const { result } = renderHook(() =>
            useLayoutStyles({ element, subElement })
          )
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("with variations on element", () => {
      it.each([
        [
          { widthConfig: undefined, useContainerWidth: false },
          { width: "auto", height: "auto" },
        ],
        [
          { widthConfig: undefined, useContainerWidth: true },
          { width: "100%", height: "auto" },
        ],
      ])("and with element %o, returns %o", (props, expected) => {
        const element = new MockElement({
          widthConfig: props.widthConfig,
        }) as Element
        const subElement = { useContainerWidth: props.useContainerWidth }
        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe("with width included along with widthConfig", () => {
      it.each([
        [
          {
            widthConfig: new streamlit.WidthConfig({ useStretch: true }),
            width: 100,
          },
          false,
          { width: "100%", height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ useContent: true }),
            width: 100,
          },
          false,
          { width: "fit-content", height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: 200 }),
            width: 100,
          },
          false,
          { width: 200, height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: 200 }),
            width: 100,
          },
          true,
          { width: "100%", height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: 0 }),
            width: 100,
          },
          false,
          { width: "auto", height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: -100 }),
            width: 100,
          },
          false,
          { width: "auto", height: "auto" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: NaN }),
            width: 100,
          },
          false,
          { width: "auto", height: "auto" },
        ],
      ])(
        "and with element props %o and useContainerWidth %s, returns %o",
        (props, useContainerWidth, expected) => {
          const element = new MockElement({
            widthConfig: props.widthConfig,
          }) as Element

          const subElement = {
            width: props.width,
            useContainerWidth,
          }

          const { result } = renderHook(() =>
            useLayoutStyles({ element, subElement })
          )
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("that has heightConfig set", () => {
      it.each([
        [
          new streamlit.HeightConfig({ useStretch: true }),
          { width: "auto", height: "100%" },
        ],
        [
          new streamlit.HeightConfig({ useContent: true }),
          { width: "auto", height: "auto" },
        ],
        [
          new streamlit.HeightConfig({ pixelHeight: 100 }),
          { width: "auto", height: 100 },
        ],
      ])(
        "and with a heightConfig value of %o, returns %o",
        (heightConfig, expected) => {
          const element = new MockElement({ heightConfig }) as Element
          const { result } = renderHook(() => useLayoutStyles({ element }))
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("that has heightConfig set to invalid pixelHeight values", () => {
      it.each([
        [0, { width: "auto", height: "auto" }],
        [-100, { width: "auto", height: "auto" }],
        [NaN, { width: "auto", height: "auto" }],
      ])(
        "and with a pixelHeight value of %s, returns %o",
        (pixelHeight, expected) => {
          const element = new MockElement({
            heightConfig: new streamlit.HeightConfig({ pixelHeight }),
          }) as Element
          const { result } = renderHook(() => useLayoutStyles({ element }))
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("with height included in subElement", () => {
      it.each([
        [undefined, { width: "auto", height: "auto" }],
        [0, { width: "auto", height: "auto" }],
        [-100, { width: "auto", height: "auto" }],
        [NaN, { width: "auto", height: "auto" }],
        [100, { width: "auto", height: 100 }],
      ])("and with a height value of %s, returns %o", (height, expected) => {
        const element = new MockElement() as Element
        const subElement = { height }
        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe("with height included along with heightConfig", () => {
      it.each([
        [
          {
            heightConfig: new streamlit.HeightConfig({ useStretch: true }),
            height: 100,
          },
          { width: "auto", height: "100%" },
        ],
        [
          {
            heightConfig: new streamlit.HeightConfig({ useContent: true }),
            height: 100,
          },
          { width: "auto", height: "auto" },
        ],
        [
          {
            heightConfig: new streamlit.HeightConfig({ pixelHeight: 200 }),
            height: 100,
          },
          { width: "auto", height: 200 },
        ],
        [
          {
            heightConfig: new streamlit.HeightConfig({ pixelHeight: 0 }),
            height: 100,
          },
          { width: "auto", height: "auto" },
        ],
        [
          {
            heightConfig: new streamlit.HeightConfig({ pixelHeight: -100 }),
            height: 100,
          },
          { width: "auto", height: "auto" },
        ],
        [
          {
            heightConfig: new streamlit.HeightConfig({ pixelHeight: NaN }),
            height: 100,
          },
          { width: "auto", height: "auto" },
        ],
      ])("and with element props %o, returns %o", (props, expected) => {
        const element = new MockElement({
          heightConfig: props.heightConfig,
        }) as Element

        const subElement = {
          height: props.height,
        }

        const { result } = renderHook(() =>
          useLayoutStyles({ element, subElement })
        )
        expect(result.current).toEqual(expected)
      })
    })

    describe("with both width and height configurations", () => {
      it.each([
        [
          {
            widthConfig: new streamlit.WidthConfig({ pixelWidth: 200 }),
            heightConfig: new streamlit.HeightConfig({ pixelHeight: 300 }),
          },
          { width: 200, height: 300 },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ useStretch: true }),
            heightConfig: new streamlit.HeightConfig({ useStretch: true }),
          },
          { width: "100%", height: "100%" },
        ],
        [
          {
            widthConfig: new streamlit.WidthConfig({ useContent: true }),
            heightConfig: new streamlit.HeightConfig({ useContent: true }),
          },
          { width: "fit-content", height: "auto" },
        ],
      ])("and with element props %o, returns %o", (props, expected) => {
        const element = new MockElement(props) as Element
        const { result } = renderHook(() => useLayoutStyles({ element }))
        expect(result.current).toEqual(expected)
      })
    })

    describe("with both width and height in subElement", () => {
      it.each([
        [
          { width: 200, height: 300 },
          { width: 200, height: 300 },
        ],
        [
          { width: 0, height: 100 },
          { width: "auto", height: 100 },
        ],
        [
          { width: 100, height: 0 },
          { width: 100, height: "auto" },
        ],
      ])(
        "and with subElement props %o, returns %o",
        (subElementProps, expected) => {
          const element = new MockElement() as Element
          const { result } = renderHook(() =>
            useLayoutStyles({ element, subElement: subElementProps })
          )
          expect(result.current).toEqual(expected)
        }
      )
    })

    describe("with widthConfig on the subElement (using type assertions)", () => {
      it.each([
        [
          {
            subElementWidthConfig: new streamlit.WidthConfig({
              useStretch: true,
            }),
          },
          { width: "100%", height: "auto" },
        ],
        [
          {
            subElementWidthConfig: new streamlit.WidthConfig({
              useContent: true,
            }),
          },
          { width: "fit-content", height: "auto" },
        ],
        [
          {
            subElementWidthConfig: new streamlit.WidthConfig({
              pixelWidth: 150,
            }),
          },
          { width: 150, height: "auto" },
        ],
      ])(
        "and with subElement widthConfig %o, returns %o",
        (props, expected) => {
          const element = new MockElement() as Element

          // Use type assertion to bypass TypeScript checks
          const subElement = {
            widthConfig: props.subElementWidthConfig,
          } as IAlert

          const { result } = renderHook(() =>
            useLayoutStyles({
              element,
              subElement,
            })
          )
          expect(result.current).toEqual(expected)
        }
      )
    })
  })
})
