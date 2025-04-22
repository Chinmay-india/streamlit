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

import { useMemo } from "react"

import { streamlit } from "@streamlit/protobuf"

type LayoutElement = {
  width?: number
  pixelWidth?: number
  widthType?: streamlit.Width
  useContainerWidth?: boolean | null
}

export type UseLayoutStylesArgs<T> = {
  element: (T & LayoutElement) | undefined
}

const isNonZeroPositiveNumber = (value: unknown): value is number =>
  typeof value === "number" && value > 0 && !isNaN(value)

type LayoutWidth = {
  pixels?: number | undefined
  layoutWidthType: streamlit.Width
}

const getWidth = (element: LayoutElement): LayoutWidth => {
  // This can be simplified once all elements have been updated to use the
  // new `pixelWidth` and `widthType` fields.
  let pixels: number | undefined
  let type: streamlit.Width = streamlit.Width.CONTENT

  if (element.widthType === streamlit.Width.STRETCH) {
    type = streamlit.Width.STRETCH
  } else if (element.widthType === streamlit.Width.CONTENT) {
    type = streamlit.Width.CONTENT
  } else if (
    element.widthType === streamlit.Width.PIXEL &&
    isNonZeroPositiveNumber(element.pixelWidth)
  ) {
    type = streamlit.Width.PIXEL
    pixels = element.pixelWidth
  } else if (
    isNonZeroPositiveNumber(element.width) &&
    element.widthType === undefined
  ) {
    pixels = element.width
    type = streamlit.Width.PIXEL
  }
  // The current behaviour is for useContainerWidth to take precedence over
  // width, see arrow.py for reference.
  if (element.useContainerWidth) {
    type = streamlit.Width.STRETCH
  }
  return { pixels, layoutWidthType: type }
}

export type UseLayoutStylesShape = {
  width: React.CSSProperties["width"]
}

/**
 * Returns the contextually-aware style values for an element container
 */
export const useLayoutStyles = <T>({
  element,
}: UseLayoutStylesArgs<T>): UseLayoutStylesShape => {
  // Note: Consider rounding the width to the nearest pixel so we don't have
  // subpixel widths, which leads to blurriness on screen
  const layoutStyles = useMemo((): UseLayoutStylesShape => {
    if (!element) {
      return {
        width: "auto",
      }
    }

    const { pixels: commandWidth, layoutWidthType } = getWidth(element)
    // The st.image element is potentially a list of images, so we always want
    // the enclosing container to be full width. The size of individual
    // images is managed in the ImageList component.
    const isImgList = element && "imgs" in element

    if (layoutWidthType === streamlit.Width.STRETCH || isImgList) {
      return {
        width: "100%",
      }
    } else if (layoutWidthType === streamlit.Width.PIXEL) {
      return {
        width: commandWidth,
      }
    }
    return {
      width: "auto",
    }
  }, [element])

  return layoutStyles
}
