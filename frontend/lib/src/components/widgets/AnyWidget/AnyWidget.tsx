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
import React, { memo, useCallback, useEffect, useRef, useState } from "react"
import { WidgetStateManager } from "~lib/WidgetStateManager"
import { AnyWidget as AnyWidgetProto } from "@streamlit/protobuf"

interface Props {
  element: AnyWidgetProto
  widgetMgr: WidgetStateManager
  width?: number
  disabled: boolean
}

interface WidgetModel {
  get: (key: string) => any
  set: (key: string, value: any) => void
  on: (event: string, callback: () => void) => void
  off: (event: string, callback: () => void) => void
  save_changes: () => void
}

export function AnyWidget({
  element,
  widgetMgr,
  width,
  disabled,
}: Props): React.ReactElement {
  const containerRef = useRef<HTMLDivElement>(null)
  const widgetInstance = useRef<any | null>(null)
  const eventHandlers = useRef<Map<string, () => void>>(new Map())

  // Store widget state in React state
  const [widgetState, setWidgetState] = useState<any>(null)
  const widgetStateRef = useRef<any>(null)

  // Initialize the widget when component mounts or when dependencies change
  useEffect(() => {
    const initializeWidget = async () => {
      try {
        // Parse the widget specification
        const spec = JSON.parse(element.spec!) as { esm: string; css?: string }

        // Initialize widget state
        let initialState: any
        try {
          // Get the initial value from the protobuf
          const initialValue = JSON.parse(
            new TextDecoder().decode(element.initialValue)
          )

          // Check if we have a stored value in widgetMgr and use it if available
          const storedValue = widgetMgr.getJsonValue({ id: element.id! })
          initialState = storedValue ? JSON.parse(storedValue) : initialValue

          // Set the widget state
          setWidgetState(initialState)
          widgetStateRef.current = initialState
          console.log("Widget state initialized:", initialState)
        } catch (error) {
          console.error("Error parsing widget state:", error)
          initialState = {}
          setWidgetState(initialState)
          widgetStateRef.current = initialState
        }

        // Create model with Streamlit integration
        const model: WidgetModel = {
          get: (key: string) => {
            console.log(
              "Getting key:",
              key,
              "Value:",
              widgetStateRef.current?.[key]
            )
            return widgetStateRef.current?.[key]
          },

          set: (key: string, value: any) => {
            console.log("Setting key:", key, "Value:", value)

            // Update widget state using React's state setter
            setWidgetState((prevState: any) => {
              const newState = {
                ...prevState,
                [key]: value,
              }

              // Update the ref for immediate access
              widgetStateRef.current = newState

              // Send updated state to Streamlit
              widgetMgr.setJsonValue(
                { id: element.id! },
                newState,
                { fromUi: true },
                undefined
              )

              return newState
            })
          },

          on: (event: string, callback: () => void) => {
            const eventName = `anywidget-${element.id}-${event}`
            eventHandlers.current.set(eventName, callback)
            window.addEventListener(eventName, callback)
          },

          off: (event: string, callback: () => void) => {
            const eventName = `anywidget-${element.id}-${event}`
            window.removeEventListener(eventName, callback)
            eventHandlers.current.delete(eventName)
          },

          save_changes: () => {
            // Trigger change event
            window.dispatchEvent(new Event(`anywidget-${element.id}-change`))
          },
        }

        // Load ESM module
        const module = await import(/* @vite-ignore */ spec.esm)

        // Render widget
        if (containerRef.current && module.default) {
          // Clear container first to avoid duplicates on re-renders
          containerRef.current.innerHTML = ""

          // Render the widget
          const instance = module.default.render({
            model,
            el: containerRef.current,
          })

          widgetInstance.current = instance

          // Add CSS if provided
          if (spec.css) {
            const styleId = `anywidget-style-${element.id}`
            if (!document.getElementById(styleId)) {
              const style = document.createElement("style")
              style.id = styleId
              style.textContent = spec.css
              document.head.appendChild(style)
            }
          }
        }
      } catch (error) {
        console.error("Error loading widget:", error)
        if (containerRef.current) {
          containerRef.current.innerHTML = `<div style="color: red; padding: 1rem;">
              Error loading widget: ${error}
            </div>`
        }
      }
    }

    initializeWidget()

    // Clean up function
    return () => {
      // Clean up event listeners
      eventHandlers.current.forEach((handler, eventName) => {
        window.removeEventListener(eventName, handler)
      })
      eventHandlers.current.clear()

      // Clean up widget instance if it has a remove method
      if (
        widgetInstance.current &&
        typeof widgetInstance.current.remove === "function"
      ) {
        widgetInstance.current.remove()
      }

      // Remove CSS if it was added
      const styleId = `anywidget-style-${element.id}`
      const styleElement = document.getElementById(styleId)
      if (styleElement) {
        styleElement.remove()
      }

      // Clear container
      if (containerRef.current) {
        containerRef.current.innerHTML = ""
      }
    }
  }, [element.id, element.spec, widgetMgr])

  return (
    <div
      ref={containerRef}
      className="stAnyWidget"
      style={{
        width,
        opacity: disabled ? 0.5 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
      data-testid="stAnyWidget"
    />
  )
}

export default memo(AnyWidget)
