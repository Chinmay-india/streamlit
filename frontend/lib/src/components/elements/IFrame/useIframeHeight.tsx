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
import React, { useEffect, useState } from "react"

import { IframeSizer } from "@streamlit/utils"

import { assertNever } from "~lib/util/assertNever"

type IframeHeightMode = "content" | "pixels"

/**
 * Custom hook to manage the dynamic height of an iframe using IframeSizer.
 */
export function useIframeHeight({
  srcDoc,
  initialHeight,
  iframeRef,
}: {
  srcDoc: string | undefined
  initialHeight: number
  iframeRef: React.RefObject<HTMLIFrameElement>
}): number | undefined {
  const [currentHeight, setCurrentHeight] = useState<number>(initialHeight)

  /**
   * -0.1 indicates "content"
   * @see #iframeV1Height
   */
  const iframeHeightMode: IframeHeightMode =
    parseFloat(initialHeight.toFixed(1)) === -0.1 ? "content" : "pixels"

  useEffect(() => {
    if (!srcDoc || iframeHeightMode === "pixels") {
      setCurrentHeight(initialHeight)
      return undefined
    }

    const iframeElement = iframeRef.current
    if (!iframeElement) {
      return undefined
    }

    let sizer: IframeSizer | undefined
    let stopWatching: (() => void) | undefined

    const handleLoad = (): void => {
      const contentBody = iframeElement.contentDocument?.body
      if (!contentBody) {
        // Cannot find body inside iframe
        return
      }

      sizer = new IframeSizer({
        setHeightCallback: (height: number) => {
          switch (iframeHeightMode) {
            case "content":
              // Set the state only if the height has actually changed
              // to avoid potential loops if the height setting itself causes a resize.
              setCurrentHeight(current =>
                current !== height ? height : current
              )
              break
            default:
              assertNever(iframeHeightMode)
          }
        },
      })

      // Start watching the iframe's body for size changes
      stopWatching = sizer.watchFrameHeight(contentBody)

      // Initial height check after setup
      sizer.setFrameHeight(undefined, contentBody)
    }

    // We need to wait for the iframe to load its content before we can access
    // the contentDocument and its body.
    iframeElement.addEventListener("load", handleLoad)

    return () => {
      iframeElement.removeEventListener("load", handleLoad)
      stopWatching?.()
    }
  }, [srcDoc, initialHeight, iframeRef, iframeHeightMode])

  return currentHeight
}
