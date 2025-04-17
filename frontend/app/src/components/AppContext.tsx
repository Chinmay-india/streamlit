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

import { AppConfig } from "@streamlit/connection"
import { IGitInfo, PageConfig } from "@streamlit/protobuf"

export interface AppContextProps {
  /**
   * The sidebar's default display state.
   * Set from the PageConfig protobuf.
   */
  initialSidebarState: PageConfig.SidebarState

  /**
   * Part of URL construction for an app page in a multi-page app;
   * this is set from the host communication manager via host message.
   * @see SidebarNav
   */
  pageLinkBaseUrl: string

  /**
   * If non-zero, this is the number of pixels that the sidebar's
   * "chevron" icon is shifted. (If sidebarChevronDownshift is 0, then
   * the current theme's spacing is used.);
   * this is set from the host communication manager via host message.
   * @see StyledSidebarCollapsedControl
   */
  sidebarChevronDownshift: number

  /**
   * Whether to disable widgets and sidebar page navigation links, based on connection
   * state and whether the host has disabled inputs.
   * @see SidebarNavLink
   */
  widgetsDisabled: boolean

  /**
   * The latest state of the git information related to the app.
   */
  gitInfo: IGitInfo | null

  /** The app-specific configuration from the apps host which is requested via the
   * _stcore/host-config endpoint.
   */
  appConfig: AppConfig
}

export const AppContext = React.createContext<AppContextProps | null>({
  initialSidebarState: PageConfig.SidebarState.AUTO,
  pageLinkBaseUrl: "",
  sidebarChevronDownshift: 0,
  widgetsDisabled: false,
  gitInfo: null,
  appConfig: {},
})
AppContext.displayName = "AppContext"
