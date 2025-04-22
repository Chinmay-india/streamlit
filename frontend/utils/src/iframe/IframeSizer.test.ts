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

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"

import { IframeSizer } from "./IframeSizer"

class IframeSizerTesting extends IframeSizer {
  /**
   * Returns internal state for testing purposes.
   */
  public getInternalStateForTesting(): {
    lastFrameHeight: number | undefined
    hasResizeObserver: boolean
    hasMutationObserver: boolean
    hasDebouncedUpdateHeight: boolean
    getSetHeightCallback: () => (height: number) => void
    forceStopWatching: () => void
  } {
    return {
      lastFrameHeight: this.lastFrameHeight,
      hasResizeObserver: this.resizeObserver !== undefined,
      hasMutationObserver: this.mutationObserver !== undefined,
      hasDebouncedUpdateHeight: this.debouncedUpdateHeight !== undefined,
      getSetHeightCallback: () => this.setHeightCallback,
      forceStopWatching: () => this.stopWatchingFrameHeight(),
    }
  }
}

const mockResizeObserver = vi.fn()
let resizeCallback: ResizeObserverCallback | null = null
mockResizeObserver.mockImplementation(cb => {
  resizeCallback = cb
  return {
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }
})
vi.stubGlobal("ResizeObserver", mockResizeObserver)

const mockMutationObserver = vi.fn()
let mutationCallback: MutationCallback | null = null
mockMutationObserver.mockImplementation(cb => {
  mutationCallback = cb
  return {
    observe: vi.fn(),
    disconnect: vi.fn(),
    takeRecords: vi.fn(),
  }
})
vi.stubGlobal("MutationObserver", mockMutationObserver)

describe("IframeSizer", () => {
  // Helper function to create spies for the observers
  function createObserverMocks(): {
    resizeDisconnectSpy: ReturnType<typeof vi.fn>
    mutationDisconnectSpy: ReturnType<typeof vi.fn>
  } {
    // Reset the mocks to get fresh instances on next calls
    mockResizeObserver.mockClear()
    mockMutationObserver.mockClear()

    // Create the mock functions that will be used for disconnect
    const resizeDisconnectMock = vi.fn()
    const mutationDisconnectMock = vi.fn()

    // Configure the global stubs to return instances using these mocks
    mockResizeObserver.mockImplementationOnce(cb => {
      resizeCallback = cb
      return {
        observe: vi.fn(),
        unobserve: vi.fn(),
        disconnect: resizeDisconnectMock, // Use the specific mock function
      }
    })

    mockMutationObserver.mockImplementationOnce(cb => {
      mutationCallback = cb
      return {
        observe: vi.fn(),
        disconnect: mutationDisconnectMock, // Use the specific mock function
        takeRecords: vi.fn(),
      }
    })

    // Return the mock functions directly so they can be asserted against
    return {
      resizeDisconnectSpy: resizeDisconnectMock,
      mutationDisconnectSpy: mutationDisconnectMock,
    }
  }

  let iframeSizer: IframeSizerTesting
  let mockSetHeightCallback: ReturnType<typeof vi.fn>
  let mockElement: HTMLElement
  // Use a separate state object to control scrollHeight
  let mockScrollHeight: number

  beforeEach(() => {
    vi.useFakeTimers()
    mockSetHeightCallback = vi.fn()
    iframeSizer = new IframeSizerTesting({
      setHeightCallback: mockSetHeightCallback,
    })

    // Create a base element
    mockElement = document.createElement("div")
    // Initial height
    mockScrollHeight = 100

    // Mock the scrollHeight getter
    vi.spyOn(mockElement, "scrollHeight", "get").mockImplementation(
      () => mockScrollHeight
    )

    // Reset mocks before each test
    mockSetHeightCallback.mockClear()
    mockResizeObserver.mockClear()
    mockMutationObserver.mockClear()
    resizeCallback = null
    mutationCallback = null
  })

  afterEach(() => {
    vi.useRealTimers()
    // Ensure observers are disconnected if a test failed mid-way
    iframeSizer.getInternalStateForTesting().forceStopWatching()
  })

  it("should initialize correctly", () => {
    expect(iframeSizer).toBeInstanceOf(IframeSizerTesting)
    expect(
      iframeSizer.getInternalStateForTesting().getSetHeightCallback()
    ).toBe(mockSetHeightCallback)
  })

  describe("setFrameHeight", () => {
    it("should call setHeightCallback with specified height", () => {
      iframeSizer.setFrameHeight(150, mockElement)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(150)
      expect(iframeSizer.getInternalStateForTesting().lastFrameHeight).toBe(
        150
      )
    })

    it("should not call setHeightCallback if element is null", () => {
      iframeSizer.setFrameHeight(150, null as unknown as HTMLElement)
      expect(mockSetHeightCallback).not.toHaveBeenCalled()
      expect(
        iframeSizer.getInternalStateForTesting().lastFrameHeight
      ).toBeUndefined()
    })

    it("should call setHeightCallback with element scrollHeight if height is undefined", () => {
      // Update mock scrollHeight
      mockScrollHeight = 120
      iframeSizer.setFrameHeight(undefined, mockElement)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(120)
      expect(iframeSizer.getInternalStateForTesting().lastFrameHeight).toBe(
        120
      )
    })

    it("should use document.body if element is not provided", () => {
      // Temporarily mock document.body.scrollHeight
      const originalScrollHeight = Object.getOwnPropertyDescriptor(
        document.body,
        "scrollHeight"
      )
      Object.defineProperty(document.body, "scrollHeight", {
        value: 200,
        configurable: true,
      })

      iframeSizer.setFrameHeight() // No height, no element
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      // 200 + 16 to account for margin
      expect(mockSetHeightCallback).toHaveBeenCalledWith(216)
      expect(iframeSizer.getInternalStateForTesting().lastFrameHeight).toBe(
        216
      )

      // Restore original property descriptor
      if (originalScrollHeight) {
        Object.defineProperty(
          document.body,
          "scrollHeight",
          originalScrollHeight
        )
      } else {
        delete (document.body as any).scrollHeight
      }
    })

    it("should not call setHeightCallback if height is the same as lastFrameHeight", () => {
      iframeSizer.setFrameHeight(100, mockElement) // First call
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(100)

      mockSetHeightCallback.mockClear()
      iframeSizer.setFrameHeight(100, mockElement) // Second call with same height
      expect(mockSetHeightCallback).not.toHaveBeenCalled()
    })

    it("should call setHeightCallback if height changes", () => {
      iframeSizer.setFrameHeight(100, mockElement)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(100)
      iframeSizer.setFrameHeight(200, mockElement)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(200)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(2)
      expect(iframeSizer.getInternalStateForTesting().lastFrameHeight).toBe(
        200
      )
    })
  })

  describe("watchFrameHeight", () => {
    let stopWatching: () => void
    let mockObservers: ReturnType<typeof createObserverMocks>

    beforeEach(() => {
      // Create mocks for observers before starting to watch
      mockObservers = createObserverMocks()

      // Start watching in beforeEach for relevant tests
      stopWatching = iframeSizer.watchFrameHeight(mockElement)
    })

    it("should return an empty function if element is null", () => {
      // Reset the mocks to isolate this test from the beforeEach
      mockResizeObserver.mockClear()
      mockMutationObserver.mockClear()

      const stopFn = iframeSizer.watchFrameHeight(
        null as unknown as HTMLElement
      )

      // The returned function should be callable without errors
      expect(() => stopFn()).not.toThrow()

      // Ensure no observers were created
      expect(mockResizeObserver).not.toHaveBeenCalled()
      expect(mockMutationObserver).not.toHaveBeenCalled()
    })

    it("should call setHeightCallback immediately with initial scrollHeight", () => {
      // watchFrameHeight is called in beforeEach
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(100)
    })

    it("should set up ResizeObserver and MutationObserver", () => {
      expect(mockResizeObserver).toHaveBeenCalledTimes(1)
      expect(mockMutationObserver).toHaveBeenCalledTimes(1)

      const internalState = iframeSizer.getInternalStateForTesting()
      expect(internalState.hasResizeObserver).toBe(true)
      expect(internalState.hasMutationObserver).toBe(true)
    })

    it("should call debounced setHeightCallback on resize observation", () => {
      mockSetHeightCallback.mockClear() // Clear initial call
      expect(resizeCallback).toBeDefined()

      // Update mock scrollHeight
      mockScrollHeight = 150
      resizeCallback!([], {} as ResizeObserver) // Simulate resize observer trigger
      expect(mockSetHeightCallback).not.toHaveBeenCalled() // Debounced

      vi.advanceTimersByTime(50) // Advance time less than debounce wait
      expect(mockSetHeightCallback).not.toHaveBeenCalled()

      vi.advanceTimersByTime(100) // Advance time past debounce wait (100ms)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(150)
    })

    it("should call debounced setHeightCallback on mutation observation", () => {
      mockSetHeightCallback.mockClear() // Clear initial call
      expect(mutationCallback).toBeDefined()

      // Update mock scrollHeight
      mockScrollHeight = 180
      mutationCallback!([], {} as MutationObserver) // Simulate mutation observer trigger
      expect(mockSetHeightCallback).not.toHaveBeenCalled() // Debounced

      vi.advanceTimersByTime(100) // Advance time past debounce wait (100ms)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      expect(mockSetHeightCallback).toHaveBeenCalledWith(180)
    })

    it("should debounce multiple rapid changes", () => {
      mockSetHeightCallback.mockClear() // Clear initial call

      // Simulate rapid changes
      mockScrollHeight = 110
      resizeCallback!([], {} as ResizeObserver)
      vi.advanceTimersByTime(20)

      mockScrollHeight = 120
      mutationCallback!([], {} as MutationObserver)
      vi.advanceTimersByTime(20)

      mockScrollHeight = 130
      resizeCallback!([], {} as ResizeObserver)

      expect(mockSetHeightCallback).not.toHaveBeenCalled() // Still debounced

      vi.advanceTimersByTime(100) // Advance past the last debounce wait
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
      // Should be called with the latest height
      expect(mockSetHeightCallback).toHaveBeenCalledWith(130)

      // Check that no more calls happen after
      vi.advanceTimersByTime(200)
      expect(mockSetHeightCallback).toHaveBeenCalledTimes(1)
    })

    it("should return a stopWatching function that disconnects observers and cancels debounce", () => {
      mockSetHeightCallback.mockClear()

      // Trigger a change but don't advance timer
      mockScrollHeight = 200
      resizeCallback!([], {} as ResizeObserver)

      stopWatching() // Call the cleanup function

      expect(mockObservers.resizeDisconnectSpy).toHaveBeenCalledTimes(1)
      expect(mockObservers.mutationDisconnectSpy).toHaveBeenCalledTimes(1)

      const internalState = iframeSizer.getInternalStateForTesting()
      expect(internalState.hasResizeObserver).toBe(false)
      expect(internalState.hasMutationObserver).toBe(false)
      expect(internalState.hasDebouncedUpdateHeight).toBe(false)
      expect(internalState.lastFrameHeight).toBeUndefined() // Should reset

      // Ensure the debounced call was actually cancelled
      vi.advanceTimersByTime(200)
      expect(mockSetHeightCallback).not.toHaveBeenCalled()
    })

    it("should handle calling watchFrameHeight multiple times by stopping previous watchers", () => {
      // Mocks for the first call (already done in beforeEach)
      const firstMocks = mockObservers
      const firstStopWatching = stopWatching // From beforeEach

      // Set up mocks for the *second* call to watchFrameHeight *before* calling it
      const secondMocks = createObserverMocks()

      // Call watch again - this should disconnect previous observers and set up new ones
      const secondStopWatching = iframeSizer.watchFrameHeight(mockElement)

      // Previous observers (firstMocks) should be disconnected
      expect(firstMocks.resizeDisconnectSpy).toHaveBeenCalledTimes(1)
      expect(firstMocks.mutationDisconnectSpy).toHaveBeenCalledTimes(1)

      // Stop watching with the second function - this should disconnect the second observers
      secondStopWatching()
      expect(secondMocks.resizeDisconnectSpy).toHaveBeenCalledTimes(1)
      expect(secondMocks.mutationDisconnectSpy).toHaveBeenCalledTimes(1)

      // Make sure the first stop function doesn't throw error (it's now a no-op internally)
      expect(() => firstStopWatching()).not.toThrow()

      // Ensure internal state reflects stopped observers
      const internalState = iframeSizer.getInternalStateForTesting()
      expect(internalState.hasResizeObserver).toBe(false)
      expect(internalState.hasMutationObserver).toBe(false)
    })
  })

  describe("stopWatchingFrameHeight direct call", () => {
    it("should disconnect observers and cancel debounce when called directly", () => {
      // Create mocks for observers before starting to watch
      const mockObservers = createObserverMocks()

      // Start watching first
      iframeSizer.watchFrameHeight(mockElement)

      // Call stopWatching directly via our test utility
      iframeSizer.getInternalStateForTesting().forceStopWatching()

      expect(mockObservers.resizeDisconnectSpy).toHaveBeenCalledTimes(1)
      expect(mockObservers.mutationDisconnectSpy).toHaveBeenCalledTimes(1)

      const internalState = iframeSizer.getInternalStateForTesting()
      expect(internalState.hasResizeObserver).toBe(false)
      expect(internalState.hasMutationObserver).toBe(false)
      expect(internalState.hasDebouncedUpdateHeight).toBe(false)
      expect(internalState.lastFrameHeight).toBeUndefined()
    })
  })
})

// Restore original observers after all tests
afterAll(() => {
  vi.unstubAllGlobals()
})
