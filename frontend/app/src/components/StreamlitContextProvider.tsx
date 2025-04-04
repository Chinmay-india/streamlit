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

import React, { memo, PropsWithChildren, useMemo } from "react"

import { AppConfig } from "@streamlit/connection"
import {
  LibConfig,
  LibContext,
  LibContextProps,
  ThemeConfig,
} from "@streamlit/lib"
import { IGitInfo, PageConfig } from "@streamlit/protobuf"
import {
  AppContext,
  AppContextProps,
} from "@streamlit/app/src/components/AppContext"

export type StreamlitContextProviderProps = PropsWithChildren<{
  // AppContext values
  wideMode: boolean
  initialSidebarState: PageConfig.SidebarState
  embedded: boolean
  showPadding: boolean
  disableScrolling: boolean
  showToolbar: boolean
  showColoredLine: boolean
  pageLinkBaseUrl: string
  sidebarChevronDownshift: number
  widgetsDisabled: boolean
  gitInfo: IGitInfo | null
  appConfig: AppConfig

  // LibContext values
  isFullScreen: boolean
  setFullScreen: (value: boolean) => void
  addScriptFinishedHandler: (func: () => void) => void
  removeScriptFinishedHandler: (func: () => void) => void
  activeTheme: ThemeConfig
  setTheme: (theme: ThemeConfig) => void
  availableThemes: ThemeConfig[]
  addThemes: (themes: ThemeConfig[]) => void
  onPageChange: (pageScriptHash: string) => void
  currentPageScriptHash: string
  libConfig: LibConfig
  fragmentIdsThisRun: Array<string>
  locale: typeof window.navigator.language
}>

/**
 * Provider component for all contexts within the Streamlit App.
 * This centralizes the context values in one place.
 */
const StreamlitContextProvider: React.FC<StreamlitContextProviderProps> = ({
  wideMode,
  initialSidebarState,
  embedded,
  showPadding,
  disableScrolling,
  showToolbar,
  showColoredLine,
  pageLinkBaseUrl,
  sidebarChevronDownshift,
  widgetsDisabled,
  gitInfo,
  appConfig,
  isFullScreen,
  setFullScreen,
  addScriptFinishedHandler,
  removeScriptFinishedHandler,
  activeTheme,
  setTheme,
  availableThemes,
  addThemes,
  onPageChange,
  currentPageScriptHash,
  libConfig,
  fragmentIdsThisRun,
  locale,
  children,
}: StreamlitContextProviderProps) => {
  const appContextProps: AppContextProps = useMemo(
    () => ({
      wideMode,
      initialSidebarState,
      embedded,
      showPadding,
      disableScrolling,
      showToolbar,
      showColoredLine,
      pageLinkBaseUrl,
      sidebarChevronDownshift,
      widgetsDisabled,
      gitInfo,
      appConfig,
    }),
    [
      wideMode,
      initialSidebarState,
      embedded,
      showPadding,
      disableScrolling,
      showToolbar,
      showColoredLine,
      pageLinkBaseUrl,
      sidebarChevronDownshift,
      widgetsDisabled,
      gitInfo,
      appConfig,
    ]
  )

  const libContextProps: LibContextProps = useMemo(
    () => ({
      isFullScreen,
      setFullScreen,
      addScriptFinishedHandler,
      removeScriptFinishedHandler,
      activeTheme,
      setTheme,
      availableThemes,
      addThemes,
      onPageChange,
      currentPageScriptHash,
      libConfig,
      fragmentIdsThisRun,
      locale,
    }),
    [
      isFullScreen,
      setFullScreen,
      addScriptFinishedHandler,
      removeScriptFinishedHandler,
      activeTheme,
      setTheme,
      availableThemes,
      addThemes,
      onPageChange,
      currentPageScriptHash,
      libConfig,
      fragmentIdsThisRun,
      locale,
    ]
  )

  return (
    <AppContext.Provider value={appContextProps}>
      <LibContext.Provider value={libContextProps}>
        {children}
      </LibContext.Provider>
    </AppContext.Provider>
  )
}

export default memo(StreamlitContextProvider)
