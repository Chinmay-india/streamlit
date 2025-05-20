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

import { Block as BlockProto, Element, streamlit } from "@streamlit/protobuf"

type SubElement = {
  useContainerWidth?: boolean | null
  height?: number
  width?: number
  // We must include this for backwards compatiblity since
  // Alert.proto has been released with the field in this position.
  widthConfig?: streamlit.IWidthConfig | null | undefined
}

export type UseLayoutStylesArgs<T> = {
  element: Element | BlockProto
  // subElement supports older config where the width/height is set on the lower
  // level element.
  subElement?: T & SubElement
}

const isNonZeroPositiveNumber = (value: unknown): value is number =>
  typeof value === "number" && value > 0 && !isNaN(value)

enum DimensionType {
  PIXEL = "pixel",
  STRETCH = "stretch",
  CONTENT = "content",
}

type LayoutDimensionConfig = {
  type: DimensionType | undefined
  pixels?: number | undefined
}

const getWidth = (
  element: Element | BlockProto,
  // subElement supports older config where the width is set on the lower
  // level element.
  subElement?: SubElement
): LayoutDimensionConfig => {
  // We need to support old width configurations for backwards compatibility,
  // since some integrations cache the messages and we want to ensure that the FE
  // can still support old message formats.
  let pixels: number | undefined
  let type: DimensionType | undefined

  const isStretch =
    (element.widthConfig && element.widthConfig.useStretch) ||
    (subElement?.widthConfig && subElement.widthConfig.useStretch)
      ? true
      : false
  const isContent =
    (element.widthConfig && element.widthConfig.useContent) ||
    (subElement?.widthConfig && subElement.widthConfig.useContent)
      ? true
      : false
  const isPixel =
    (element.widthConfig && element.widthConfig.pixelWidth) ||
    (subElement?.widthConfig && subElement.widthConfig.pixelWidth)
      ? true
      : false

  if (isStretch) {
    type = DimensionType.STRETCH
  } else if (isContent) {
    type = DimensionType.CONTENT
  } else if (
    isPixel &&
    isNonZeroPositiveNumber(element.widthConfig?.pixelWidth)
  ) {
    type = DimensionType.PIXEL
    pixels = element.widthConfig?.pixelWidth
  } else if (
    isPixel &&
    isNonZeroPositiveNumber(subElement?.widthConfig?.pixelWidth)
  ) {
    type = DimensionType.PIXEL
    pixels = subElement?.widthConfig?.pixelWidth
  } else if (
    isNonZeroPositiveNumber(subElement?.width) &&
    !element.widthConfig
  ) {
    pixels = subElement?.width
    type = DimensionType.PIXEL
  }
  // The current behaviour is for useContainerWidth to take precedence over
  // width, see arrow.py for reference.
  if (subElement?.useContainerWidth) {
    type = DimensionType.STRETCH
  }
  return { pixels, type }
}

const getHeight = (
  element: Element | BlockProto,
  // subElement supports older config where the height is set on the lower
  // level element.
  subElement?: SubElement
): LayoutDimensionConfig => {
  // We need to support old height configurations for backwards compatibility,
  // since some integrations cache the messages and we want to ensure that the FE
  // can still support old message formats.
  let pixels: number | undefined
  let type: DimensionType | undefined

  const isStretch =
    element.heightConfig && element.heightConfig.useStretch ? true : false
  const isContent =
    element.heightConfig && element.heightConfig.useContent ? true : false
  const isPixel =
    element.heightConfig && element.heightConfig.pixelHeight ? true : false

  if (isStretch) {
    type = DimensionType.STRETCH
  } else if (isContent) {
    type = DimensionType.CONTENT
  } else if (
    isPixel &&
    isNonZeroPositiveNumber(element.heightConfig?.pixelHeight)
  ) {
    type = DimensionType.PIXEL
    pixels = element.heightConfig?.pixelHeight
  } else if (
    isNonZeroPositiveNumber(subElement?.height) &&
    !element.heightConfig
  ) {
    pixels = subElement?.height
    type = DimensionType.PIXEL
  }

  return { pixels, type }
}

export type UseLayoutStylesShape = {
  width: React.CSSProperties["width"]
  height: React.CSSProperties["height"]
  overflow: React.CSSProperties["overflow"]
}

/**
 * Returns the contextually-aware style values for an element container
 */
export const useLayoutStyles = <T>({
  element,
  subElement,
}: UseLayoutStylesArgs<T>): UseLayoutStylesShape => {
  // Note: Consider rounding the width to the nearest pixel so we don't have
  // subpixel widths, which leads to blurriness on screen
  const layoutStyles = useMemo((): UseLayoutStylesShape => {
    if (!element) {
      return {
        width: "auto",
        height: "auto",
        overflow: "visible",
      }
    }

    // The st.image element is potentially a list of images, so we always want
    // the enclosing container to be full width. The size of individual
    // images is managed in the ImageList component.
    const isImgList = element.type === "imgs"

    const { pixels: commandWidth, type: widthType } = getWidth(
      element,
      subElement
    )
    let width: React.CSSProperties["width"] = "auto"

    if (widthType === DimensionType.STRETCH || isImgList) {
      width = "100%"
    } else if (widthType === DimensionType.PIXEL) {
      width = commandWidth
    } else if (widthType === DimensionType.CONTENT) {
      width = "fit-content"
    }

    const { pixels: commandHeight, type: heightType } = getHeight(
      element,
      subElement
    )
    let height: React.CSSProperties["height"] = "auto"
    let overflow: React.CSSProperties["overflow"] = "visible"

    // The st.text_area element has a legacy implementation where the height
    // is measuing only the input box so the pixel height must be set in the element
    // and the container must be allowed to expand.
    const isTextArea = element.type === "textArea"

    if (heightType === DimensionType.STRETCH) {
      height = "100%"
    } else if (heightType === DimensionType.CONTENT || isTextArea) {
      height = "auto"
    } else if (heightType === DimensionType.PIXEL) {
      height = commandHeight
      overflow = "auto"
    }

    return {
      width,
      height,
      overflow,
    }
  }, [element, subElement])

  return layoutStyles
}
