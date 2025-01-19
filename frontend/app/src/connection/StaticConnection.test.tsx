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

import {
  ForwardMsgList,
  localStorageAvailable,
  logError,
} from "@streamlit/lib"

import { ConnectionState } from "./ConnectionState"
import {
  dispatchAppForwardMessages,
  getProtoResponse,
  getStaticConfig,
  StaticConnection,
} from "./StaticConnection"

vi.mock("@streamlit/lib", () => ({
  localStorageAvailable: vi.fn(),
  logError: vi.fn(),
  ForwardMsgList: {
    decode: vi.fn(),
  },
}))

global.fetch = vi.fn()

global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
}

describe("StaticConnection", () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  describe("getStaticConfig", () => {
    it("fetches URL from localStorage if available", async () => {
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue("https://example.com")

      const result = await getStaticConfig()

      expect(result).toBe("https://example.com")
    })

    it("fetches URL from STATIC_ASSET_CONFIG if not in localStorage", async () => {
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue(null)

      fetch.mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue({ static_url: "https://example.com" }),
      })

      const result = await getStaticConfig()

      expect(fetch).toHaveBeenCalledWith(
        "https://data.streamlit.io/static.json",
        expect.objectContaining({ signal: expect.any(AbortSignal) })
      )
      expect(result).toBe("https://example.com")
      expect(global.localStorage.setItem).toHaveBeenCalledWith(
        "stStaticAssetUrl",
        "https://example.com"
      )
    })

    it("logs error when fetch fails", async () => {
      fetch.mockRejectedValue(new Error("Fetch error"))

      const result = await getStaticConfig()

      expect(result).toBe("")
      expect(logError).toHaveBeenCalledWith(
        "Failed to fetch static config url:",
        expect.any(Error)
      )
    })
  })

  describe("getProtoResponse", () => {
    it("fetches proto response from correct URL", async () => {
      const staticNotebookId = "123"
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue("www.example.com")

      fetch.mockResolvedValue({
        ok: true,
        arrayBuffer: vi.fn().mockResolvedValue(new ArrayBuffer(8)),
      })

      const result = await getProtoResponse(staticNotebookId)

      expect(fetch).toHaveBeenCalledWith(
        "www.example.com/123/protos.pb",
        expect.objectContaining({ signal: expect.any(AbortSignal) })
      )
      expect(result).toBeInstanceOf(ArrayBuffer)
    })

    it("logs error if fetch fails", async () => {
      const staticNotebookId = "123"
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue("www.example.com")

      fetch.mockResolvedValue({ ok: false, status: 404 })

      const result = await getProtoResponse(staticNotebookId)

      expect(result).toBeUndefined()
      expect(logError).toHaveBeenCalledWith(
        `Failed to fetch static app protos for id: ${staticNotebookId}`,
        404
      )
    })
  })

  describe("dispatchAppForwardMessages", () => {
    beforeEach(() => {
      // Handles getStaticConfig
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue("www.example.com")
    })

    it("decodes and dispatches messages", async () => {
      const staticNotebookId = "123"
      const onMessage = vi.fn()

      // Handles getProtoResponse
      fetch.mockResolvedValue({
        ok: true,
        arrayBuffer: vi.fn().mockResolvedValue(new ArrayBuffer(8)),
      })

      const mockMessages = [{ id: 1 }, { id: 2 }]
      vi.spyOn(ForwardMsgList, "decode").mockReturnValue({
        messages: mockMessages,
      })

      await dispatchAppForwardMessages(staticNotebookId, onMessage)

      expect(ForwardMsgList.decode).toHaveBeenCalled()
      expect(onMessage).toHaveBeenCalledTimes(2)
      expect(onMessage).toHaveBeenCalledWith(mockMessages[0])
      expect(onMessage).toHaveBeenCalledWith(mockMessages[1])
    })

    it("logs error if arrayBuffer is undefined", async () => {
      const staticNotebookId = "123"
      const onMessage = vi.fn()

      // Handles getProtoResponse
      fetch.mockResolvedValue({
        ok: true,
        arrayBuffer: vi.fn().mockResolvedValue(null),
      })

      await dispatchAppForwardMessages(staticNotebookId, onMessage)

      expect(logError).toHaveBeenCalledWith(
        "Failed to retrieve static app protos"
      )
    })
  })

  describe("StaticConnection", () => {
    beforeEach(() => {
      // Handles getStaticConfig
      localStorageAvailable.mockReturnValue(true)
      global.localStorage.getItem.mockReturnValue("www.example.com")

      // Handles getProtoResponse
      fetch.mockResolvedValue({
        ok: true,
        arrayBuffer: vi.fn().mockResolvedValue(new ArrayBuffer(8)),
      })
    })

    it("handles connection state changes and message dispatch", async () => {
      const staticNotebookId = "123"
      const onConnectionStateChange = vi.fn()
      const onMessage = vi.fn()

      StaticConnection({
        staticNotebookId,
        onConnectionStateChange,
        onMessage,
      })

      expect(onConnectionStateChange).toHaveBeenCalledWith(
        ConnectionState.STATIC_CONNECTING
      )
      await dispatchAppForwardMessages(staticNotebookId, onMessage)
      expect(onConnectionStateChange).toHaveBeenCalledWith(
        ConnectionState.STATIC_CONNECTED
      )
    })
  })
})
