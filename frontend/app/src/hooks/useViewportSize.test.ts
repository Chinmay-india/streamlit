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

import React from "react"

import { act, renderHook } from "@testing-library/react"

import { LibContext, LibContextProps } from "@streamlit/lib"

import { useViewportSize } from "./useViewportSize"

const mockContextValue = {
  activeTheme: {
    emotion: {
      breakpoints: {
        md: "768px",
      },
    },
  },
} as unknown as LibContextProps

// Wrapper component to provide context
const wrapper = ({
  children,
}: {
  children: React.ReactNode
}): React.ReactElement =>
  React.createElement(LibContext.Provider, {
    value: mockContextValue,
    children,
  })

describe("useViewportSize", () => {
  const originalInnerWidth = window.innerWidth

  afterEach(() => {
    // Restore original window.innerWidth
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: originalInnerWidth,
    })
  })

  it("should return isMobile=true when window width is below theme breakpoint", () => {
    // Set window width below the md breakpoint (768px)
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 767,
    })

    const { result } = renderHook(() => useViewportSize(), { wrapper })

    expect(result.current.isMobile).toBe(true)
  })

  it("should return isMobile=false when window width is at theme breakpoint", () => {
    // Set window width exactly at the md breakpoint (768px)
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 768,
    })

    const { result } = renderHook(() => useViewportSize(), { wrapper })

    expect(result.current.isMobile).toBe(false)
  })

  it("should return isMobile=false when window width is above theme breakpoint", () => {
    // Set window width above the md breakpoint (768px)
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1024,
    })

    const { result } = renderHook(() => useViewportSize(), { wrapper })

    expect(result.current.isMobile).toBe(false)
  })

  it("should update isMobile when window is resized", () => {
    // Start with desktop width
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1024,
    })

    const { result } = renderHook(() => useViewportSize(), { wrapper })

    expect(result.current.isMobile).toBe(false)

    // Resize to mobile width
    act(() => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 500,
      })
      window.dispatchEvent(new Event("resize"))
    })

    expect(result.current.isMobile).toBe(true)

    // Resize back to desktop width
    act(() => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 1024,
      })
      window.dispatchEvent(new Event("resize"))
    })

    expect(result.current.isMobile).toBe(false)
  })

  it("should cleanup resize event listener on unmount", () => {
    const removeEventListenerSpy = vi.spyOn(window, "removeEventListener")

    const { unmount } = renderHook(() => useViewportSize(), { wrapper })

    unmount()

    expect(removeEventListenerSpy).toHaveBeenCalledWith(
      "resize",
      expect.any(Function)
    )

    removeEventListenerSpy.mockRestore()
  })
})
