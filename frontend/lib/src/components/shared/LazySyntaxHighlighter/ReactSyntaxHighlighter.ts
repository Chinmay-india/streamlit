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

import { lazy, useEffect, useState } from "react"

/**
 * This is a lazy-loaded Prism component from react-syntax-highlighter.
 * It's done async because the react-syntax-highlighter package is large.
 *
 * @returns The Prism component from react-syntax-highlighter
 */
export const SyntaxHighlighter = lazy(() =>
  import("react-syntax-highlighter").then(m => {
    return {
      default: m.Prism,
    }
  })
)

export type CreateElementFunction =
  typeof import("react-syntax-highlighter").createElement

/**
 * This is a lazy-loaded createElement function from react-syntax-highlighter.
 * It's done async because the react-syntax-highlighter package is large.
 *
 * @returns The createElement function from react-syntax-highlighter, or null if it's not loaded yet.
 */
export const useLazyCreateElement = (): CreateElementFunction | null => {
  const [loadedCreateElementFn, setLoadedCreateElementFn] =
    useState<CreateElementFunction | null>(null)

  useEffect(() => {
    let isMounted = true

    const doWork = async (): Promise<void> => {
      const loadedModule = await import("react-syntax-highlighter")
      const { createElement } = loadedModule

      if (isMounted) {
        setLoadedCreateElementFn(() => createElement)
      }
    }

    doWork()

    return () => {
      isMounted = false
    }
  }, [])

  return loadedCreateElementFn
}
