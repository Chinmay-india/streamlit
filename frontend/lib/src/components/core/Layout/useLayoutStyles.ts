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

import { useContext, useMemo } from "react"
import { FlexContext } from "../Flex/FlexContext"

export type UseLayoutStylesArgs<T> = {
  width: React.CSSProperties["width"] | undefined
  element:
    | (T & {
        width?: string | undefined | null
        height?: string | undefined | null
        useContainerWidth?: boolean | undefined
        flex?: string
        scale?: number | undefined | null
        size?: number | "stretch"
        type?: string
      })
    | undefined
  isFlexContainer: boolean
}

export type UseLayoutStylesShape = {
  width: React.CSSProperties["width"]
  maxWidth?: React.CSSProperties["maxWidth"]
  maxHeight?: React.CSSProperties["maxHeight"]
  flex?: React.CSSProperties["flex"]
  height?: React.CSSProperties["height"]
  marginLeft?: React.CSSProperties["marginLeft"]
  marginTop?: React.CSSProperties["marginTop"]
  verticalScroll?: boolean
  alignSelf?: React.CSSProperties["alignSelf"]
}

export const isNumber = (
  value: string | number | undefined | null
): value is number => {
  return (
    !(typeof value === "string" && value.trim().length === 0) &&
    value !== null &&
    value !== undefined &&
    !Number.isNaN(Number(value))
  )
}

export const getWidth = (
  useContainerWidth: boolean,
  commandWidth: string | undefined | null,
  containerWidth: React.CSSProperties["width"] | undefined
) => {
  if (useContainerWidth) {
    return containerWidth ?? "100%"
  }
  if (String(commandWidth) === "stretch") {
    return "100%"
  } else if (String(commandWidth) === "content") {
    return "fit-content"
  } else if (isNumber(commandWidth) && commandWidth > 0) {
    return `${commandWidth}px`
  }
  return "auto"
}

export const getHeight = (commandHeight: string | undefined | null) => {
  if (String(commandHeight) === "stretch") {
    return "auto"
  } else if (String(commandHeight) === "content") {
    return "fit-content"
  } else if (isNumber(commandHeight) && commandHeight > 0) {
    return `${commandHeight}px`
  }

  return "auto"
}

export const getFlex = (
  useContainerWidth: boolean,
  commandWidth: string | undefined | null,
  commandHeight: string | undefined | null,
  containerWidth: React.CSSProperties["width"] | undefined,
  direction: "row" | "column" | undefined,
  scale: number | undefined | null
) => {
  if (useContainerWidth) {
    if (isNumber(containerWidth)) {
      return `1 1 ${containerWidth}px`
    } else if (containerWidth !== undefined) {
      return `1 1 ${containerWidth}`
    } else {
      return undefined
    }
  }
  if (
    String(commandWidth) === "stretch" &&
    scale !== undefined &&
    direction === "row"
  ) {
    return `${scale}`
  } else if (
    String(commandHeight) === "stretch" &&
    scale !== undefined &&
    direction === "column"
  ) {
    return `${scale}`
  } else if (isNumber(commandWidth) && direction === "row") {
    return `0 1 ${commandWidth}px`
  } else if (isNumber(commandHeight) && direction === "column") {
    return `0 1 ${commandHeight}px`
  }
  return undefined
}

export const getVerticalScroll = (height: string | null | undefined) => {
  return isNumber(height) && Number(height) > 0
}

/**
 * Returns the contextually-aware style values for an element container
 */
export const useLayoutStyles = <T>({
  width: containerWidth,
  element,
  isFlexContainer,
}: UseLayoutStylesArgs<T>): UseLayoutStylesShape => {
  /**
   * The width set from the `st.<command>`
   */
  const commandWidth = element?.width
  const commandHeight = element?.height
  const useContainerWidth = element?.useContainerWidth ?? false
  const flexContext = useContext(FlexContext)

  let direction: "column" | "row" | undefined
  if (flexContext) {
    if (isFlexContainer) {
      direction = flexContext.parentContainerDirection
    } else {
      direction = flexContext.direction
    }
  }

  // Note: Consider rounding the width to the nearest pixel so we don't have
  // subpixel widths, which leads to blurriness on screen
  const layoutStyles = useMemo((): UseLayoutStylesShape => {
    // If we don't have an element, we are rendering a root-level node, likely a
    // `StyledAppViewBlockContainer`
    if (!element) {
      return {
        width: containerWidth,
      }
    }

    if ("size" in element) {
      const size = element.size
      const isNumeric = isNumber(size)
      const isStretch = size === "stretch"

      const isHorizontal = direction === "row"

      if (isNumeric) {
        // Fixed size space
        const sizeValue = `${size}px`

        if (isHorizontal) {
          // In horizontal container, set width
          return {
            width: sizeValue,
          }
        } else {
          // In vertical container, set height
          return {
            width: "100%",
            height: sizeValue,
          }
        }
      } else if (isStretch) {
        // Stretch space - push content to edges
        if (isHorizontal) {
          // In horizontal container, push horizontally
          return {
            width: "auto",
            marginLeft: "auto",
          }
        } else {
          // In vertical container, push vertically
          return {
            width: "auto",
            marginTop: "auto",
          }
        }
      }

      // Default fallback if size is not recognized
      return {
        width: "auto",
      }
    }

    if ("imgs" in element) {
      /**
       * ImageList overrides its `width` param and handles its own width in the
       * component. There should not be any element-specific carve-outs in this
       * file, but given the long-standing behavior of ImageList, we have to
       * make an exception here.
       *
       * @see WidthBehavior on the Backend
       * @see the Image.proto file
       */
      let flex
      if (isNumber(containerWidth)) {
        flex = `${element.scale ?? 1} 1 ${containerWidth}px`
      } else {
        flex = `${element.scale ?? 1} 1 0%`
      }

      return {
        width: containerWidth,
        flex: flex,
      }
    }

    const width = getWidth(useContainerWidth, commandWidth, containerWidth)
    const flex = getFlex(
      useContainerWidth,
      commandWidth,
      commandHeight,
      containerWidth,
      direction,
      element?.scale
    )
    const height = getHeight(commandHeight)
    const verticalScroll = getVerticalScroll(commandHeight)
    const styles: UseLayoutStylesShape = {
      width,
      height,
      maxWidth: "100%",
      maxHeight: "100%",
      flex,
      verticalScroll,
    }

    if (String(commandHeight) === "stretch") {
      styles.alignSelf = "stretch"
    }

    return styles
  }, [useContainerWidth, commandWidth, containerWidth, element])

  return layoutStyles
}
