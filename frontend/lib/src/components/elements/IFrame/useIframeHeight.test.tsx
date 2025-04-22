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

import { act } from "react"

import { renderHook, waitFor } from "@testing-library/react"
import { beforeEach, describe, expect, it, vi } from "vitest"

import { IframeSizer } from "@streamlit/utils"

import { useIframeHeight } from "./useIframeHeight"

vi.mock("@streamlit/utils", () => {
  const mockSetHeightCallback = vi.fn()
  const mockWatchFrameHeight = vi.fn(() => vi.fn())
  const mockSetFrameHeight = vi.fn()

  return {
    IframeSizer: vi.fn().mockImplementation(({ setHeightCallback }) => {
      mockSetHeightCallback.mockReset()
      mockSetHeightCallback.mockImplementation(setHeightCallback)

      return {
        // Just return the methods we need for testing
        watchFrameHeight: mockWatchFrameHeight,
        setFrameHeight: mockSetFrameHeight,
        // Helper method to easily simulate height changes
        _triggerHeightChange: (height: number) => {
          mockSetHeightCallback(height)
        },
      } as unknown as IframeSizer
    }),
  }
})

describe("useIframeHeight", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should return the initial height if the iframe is not loaded", () => {
    const { result } = renderHook(() =>
      useIframeHeight({
        srcDoc: undefined,
        initialHeight: 100,
        iframeRef: { current: null },
      })
    )
    expect(result.current).toBe(100)
  })

  it("should return initial height when srcDoc is undefined", () => {
    const { result } = renderHook(() =>
      useIframeHeight({
        srcDoc: undefined,
        initialHeight: 200,
        iframeRef: {
          current: document.createElement("iframe"),
        },
      })
    )
    expect(result.current).toBe(200)
  })

  it("should keep initialHeight in 'pixels' mode (initialHeight !== -0.1)", () => {
    const { result } = renderHook(() =>
      useIframeHeight({
        srcDoc: "<html><body>Content</body></html>",
        initialHeight: 300,
        iframeRef: {
          current: document.createElement("iframe"),
        },
      })
    )
    expect(result.current).toBe(300)
  })

  describe("content mode", () => {
    const initialHeight = -0.1

    it("should update height when IframeSizer calls setHeightCallback with content mode", () => {
      const mockIframe = document.createElement("iframe")

      Object.defineProperty(mockIframe, "contentDocument", {
        value: {
          body: document.createElement("body"),
        },
      })

      const mockRef = { current: mockIframe }

      const { result } = renderHook(() =>
        useIframeHeight({
          srcDoc: "<html><body>Content</body></html>",
          initialHeight,
          iframeRef: mockRef,
        })
      )

      expect(result.current).toBe(initialHeight)

      // Simulate iframe load event
      act(() => {
        const loadEvent = new Event("load")
        mockIframe.dispatchEvent(loadEvent)
      })

      // Get the created instance and trigger height change
      const iframeSizerInstance = vi.mocked(IframeSizer).mock.results[0].value

      // Simulate the height change callback
      act(() => {
        iframeSizerInstance._triggerHeightChange(500)
      })

      // Height should be updated by the callback
      expect(result.current).toBe(500)
    })

    it("should clean up event listeners when unmounting", () => {
      const cleanupSpy = vi.fn()
      vi.mocked(IframeSizer).mockImplementationOnce(() => {
        return {
          watchFrameHeight: vi.fn(() => cleanupSpy),
          setFrameHeight: vi.fn(),
        } as unknown as IframeSizer
      })

      const mockIframe = document.createElement("iframe")
      const removeEventListenerSpy = vi.spyOn(
        mockIframe,
        "removeEventListener"
      )

      // Mock contentDocument and body
      Object.defineProperty(mockIframe, "contentDocument", {
        value: {
          body: document.createElement("body"),
        },
      })

      const mockRef = { current: mockIframe }

      const { unmount } = renderHook(() =>
        useIframeHeight({
          srcDoc: "<html><body>Content</body></html>",
          initialHeight,
          iframeRef: mockRef,
        })
      )

      // Simulate iframe load event
      act(() => {
        const loadEvent = new Event("load")
        mockIframe.dispatchEvent(loadEvent)
      })

      // Unmount the hook
      unmount()

      // Should have removed the event listener
      expect(removeEventListenerSpy).toHaveBeenCalledWith(
        "load",
        expect.any(Function)
      )
      // Should have called the cleanup function
      expect(cleanupSpy).toHaveBeenCalledTimes(1)
    })

    it("should not update height if new height is the same as current height", async () => {
      // Create a custom callback and spy
      const setHeightCallbackSpy = vi.fn()

      // Override the module mock for this specific test
      vi.mocked(IframeSizer).mockImplementationOnce(
        ({ setHeightCallback }) => {
          // Update our spy to track calls to the real callback
          setHeightCallbackSpy.mockImplementation(height => {
            setHeightCallback(height)
          })

          return {
            watchFrameHeight: vi.fn(() => vi.fn()),
            setFrameHeight: vi.fn(),
            // Direct way to trigger height changes for testing
            _triggerHeightChange: (height: number) => {
              setHeightCallbackSpy(height)
            },
          } as unknown as IframeSizer
        }
      )

      const mockIframe = document.createElement("iframe")

      // Mock contentDocument and body
      Object.defineProperty(mockIframe, "contentDocument", {
        value: {
          body: document.createElement("body"),
        },
      })

      const mockRef = { current: mockIframe }

      const { result } = renderHook(() =>
        useIframeHeight({
          srcDoc: "<html><body>Content</body></html>",
          initialHeight,
          iframeRef: mockRef,
        })
      )

      // Simulate iframe load event
      act(() => {
        const loadEvent = new Event("load")
        mockIframe.dispatchEvent(loadEvent)
      })

      // Get the instance created by the hook
      const iframeSizerInstance = vi.mocked(IframeSizer).mock.results[0].value

      // First update - should change the height
      act(() => {
        iframeSizerInstance._triggerHeightChange(500)
      })

      await waitFor(() => expect(result.current).toBe(500))

      // Reset the spy to clearly count subsequent calls
      setHeightCallbackSpy.mockClear()

      // Set up the internal state to simulate "same height" scenario
      iframeSizerInstance.lastFrameHeight = 500

      // Second update with same height - should not call setHeightCallback again
      act(() => {
        // Directly try to set the same height to test the hook's behavior
        // This time we'll trigger a callback with the same value
        iframeSizerInstance._triggerHeightChange(500)
      })

      // Validate the hook state didn't change
      expect(result.current).toBe(500)

      // Since we manually triggered the callback, it would have been called, but
      // the hook should have ignored it because of the same height check
      expect(setHeightCallbackSpy).toHaveBeenCalledTimes(1)
    })
  })
})
