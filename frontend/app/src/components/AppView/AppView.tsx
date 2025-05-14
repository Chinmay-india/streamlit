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

import React, { ReactElement, useContext, useMemo } from "react"

import { getLogger } from "loglevel"

import { StreamlitEndpoints } from "@streamlit/connection"
import {
  AppRoot,
  BlockNode,
  ComponentRegistry,
  ContainerContentsWrapper,
  FileUploadClient,
  FormsData,
  IGuestToHostMessage,
  LibContext,
  Profiler,
  ScriptRunState,
  VerticalBlock,
  WidgetStateManager,
} from "@streamlit/lib"
import { IAppPage, Logo, Navigation, PageConfig } from "@streamlit/protobuf"
import ThemedSidebar from "@streamlit/app/src/components/Sidebar"
import EventContainer from "@streamlit/app/src/components/EventContainer"
import { AppContext } from "@streamlit/app/src/components/AppContext"
import Header from "@streamlit/app/src/components/Header"
import { TopNav } from "@streamlit/app/src/components/Navigation"
import { useAppContext } from "@streamlit/app/src/components/StreamlitContextProvider"
import { LogoComponent } from "@streamlit/app/src/components/Logo"
import {
  StyledAppViewBlockContainer,
  StyledAppViewBlockSpacer,
  StyledAppViewContainer,
  StyledAppViewMain,
  StyledBottomBlockContainer,
  StyledEventBlockContainer,
  StyledIFrameResizerAnchor,
  StyledInnerBottomContainer,
  StyledMainContent,
  StyledSidebarBlockContainer,
  StyledStickyBottomContainer,
} from "./styled-components"
import ScrollToBottomContainer from "./ScrollToBottomContainer"
import { StyledLogoContainer } from "@streamlit/app/src/components/Header/styled-components"
import HeaderColoredLine from "@streamlit/app/src/components/HeaderColoredLine"

const LOG = getLogger("AppView")
export interface AppViewProps {
  elements: AppRoot

  endpoints: StreamlitEndpoints

  sendMessageToHost: (message: IGuestToHostMessage) => void

  // The unique ID for the most recent script run.
  scriptRunId: string

  scriptRunState: ScriptRunState

  widgetMgr: WidgetStateManager

  uploadClient: FileUploadClient

  componentRegistry: ComponentRegistry

  formsData: FormsData

  appLogo: Logo | null

  appPages: IAppPage[]

  navSections: string[]

  onPageChange: (pageName: string) => void

  currentPageScriptHash: string

  hideSidebarNav: boolean

  expandSidebarNav: boolean

  navigationPosition: Navigation.Position

  // Header props
  topRightContent?: React.ReactNode

  // Base URL for page links
  pageLinkBaseUrl?: string
}

/**
 * Renders a Streamlit app.
 */
function AppView(props: AppViewProps): ReactElement {
  const {
    elements,
    scriptRunId,
    scriptRunState,
    widgetMgr,
    uploadClient,
    componentRegistry,
    formsData,
    appLogo,
    appPages,
    navSections,
    onPageChange,
    currentPageScriptHash,
    expandSidebarNav,
    hideSidebarNav,
    sendMessageToHost,
    endpoints,
    navigationPosition,
    topRightContent,
    pageLinkBaseUrl = "",
  } = props

  React.useEffect(() => {
    const listener = (): void => {
      sendMessageToHost({
        type: "UPDATE_HASH",
        hash: window.location.hash,
      })
    }
    window.addEventListener("hashchange", listener, false)
    return () => window.removeEventListener("hashchange", listener, false)
  }, [sendMessageToHost])

  const {
    wideMode,
    initialSidebarState,
    embedded,
    showPadding,
    disableScrolling,
    showToolbar,
    showColoredLine,
    sidebarChevronDownshift,
    widgetsDisabled,
  } = useAppContext()

  const {
    addScriptFinishedHandler,
    removeScriptFinishedHandler,
    activeTheme,
  } = useContext(LibContext)

  const layout = wideMode ? "wide" : "narrow"
  const hasSidebarElements = !elements.sidebar.isEmpty
  const hasEventElements = !elements.event.isEmpty
  const hasBottomElements = !elements.bottom.isEmpty

  const [showSidebarOverride, setShowSidebarOverride] = React.useState(false)

  const showSidebar =
    hasSidebarElements ||
    (!hideSidebarNav && appPages.length > 1) ||
    showSidebarOverride

  React.useEffect(() => {
    // Handle sidebar flicker/unmount with MPA & hideSidebarNav
    if (showSidebar && hideSidebarNav && !showSidebarOverride) {
      setShowSidebarOverride(true)
    }
  }, [showSidebar, hideSidebarNav, showSidebarOverride])

  const scriptFinishedHandler = React.useCallback(() => {
    // Check at end of script run if no sidebar elements
    if (!hasSidebarElements && showSidebarOverride) {
      setShowSidebarOverride(false)
    }
  }, [hasSidebarElements, showSidebarOverride])

  React.useEffect(() => {
    addScriptFinishedHandler(scriptFinishedHandler)
    return () => {
      removeScriptFinishedHandler(scriptFinishedHandler)
    }
  }, [
    scriptFinishedHandler,
    addScriptFinishedHandler,
    removeScriptFinishedHandler,
  ])

  const handleLogoError = (logoUrl: string): void => {
    // StyledLogo does not retain the e.currentEvent.src like other onerror cases
    // store and read from ref instead
    LOG.error(`Client Error: Logo source error - ${logoUrl}`)
    endpoints.sendClientErrorToHost(
      "Logo",
      "Logo source failed to load",
      "onerror triggered",
      logoUrl
    )
  }

  const renderLogo = (appLogo: Logo): ReactElement => {
    const displayImage = appLogo.iconImage ? appLogo.iconImage : appLogo.image
    const source = endpoints.buildMediaURL(displayImage)

    const logo = (
      <StyledLogo
        src={source}
        size={appLogo.size}
        alt="Logo"
        className="stLogo"
        data-testid="stLogo"
        // Save to logo's src to send on load error
        onError={_ => handleLogoError(source)}
      />
    )

    if (appLogo.link) {
      return (
        <StyledLogoLink
          href={appLogo.link}
          target="_blank"
          rel="noreferrer"
          data-testid="stLogoLink"
        >
          {logo}
        </StyledLogoLink>
      )
    }
    return logo
  }

  // Activate scroll to bottom whenever there are bottom elements:
  const Component = hasBottomElements
    ? ScrollToBottomContainer
    : StyledAppViewMain

  const renderBlock = (node: BlockNode): ReactElement => (
    <ContainerContentsWrapper
      node={node}
      endpoints={endpoints}
      scriptRunId={scriptRunId}
      scriptRunState={scriptRunState}
      widgetMgr={widgetMgr}
      widgetsDisabled={widgetsDisabled}
      uploadClient={uploadClient}
      componentRegistry={componentRegistry}
      formsData={formsData}
    />
  )

  const [isSidebarCollapsed, setSidebarIsCollapsed] = React.useState<boolean>(
    initialSidebarState === PageConfig.SidebarState.COLLAPSED ||
      (initialSidebarState === PageConfig.SidebarState.AUTO &&
        window.innerWidth <= parseInt(activeTheme.emotion.breakpoints.md, 10))
  )

  const toggleSidebar = React.useCallback(() => {
    setSidebarIsCollapsed(prev => !prev)
  }, [])

  console.log({ navigationPosition })

  // Logo component to be used in the header when sidebar is closed
  const logoElement = useMemo(() => {
    if (!appLogo) return null

    return (
      <LogoComponent
        appLogo={appLogo}
        endpoints={endpoints}
        componentName="Header Logo"
      />
    )
  }, [appLogo, endpoints])

  // The tabindex is required to support scrolling by arrow keys.
  return (
    <>
      <HeaderColoredLine />
      <StyledAppViewContainer
        className="stAppViewContainer appview-container"
        data-testid="stAppViewContainer"
        data-layout={layout}
      >
        {showSidebar && (
          <Profiler id="Sidebar">
            <ThemedSidebar
              endpoints={endpoints}
              appLogo={appLogo}
              appPages={appPages}
              navSections={navSections}
              hasElements={hasSidebarElements}
              onPageChange={onPageChange}
              currentPageScriptHash={currentPageScriptHash}
              hideSidebarNav={hideSidebarNav}
              expandSidebarNav={expandSidebarNav}
              isCollapsed={isSidebarCollapsed}
              onToggleCollapse={setSidebarIsCollapsed}
            >
              <StyledSidebarBlockContainer>
                {renderBlock(elements.sidebar)}
              </StyledSidebarBlockContainer>
            </ThemedSidebar>
          </Profiler>
        )}
        <StyledMainContent>
          <Header
            isStale={scriptRunState === ScriptRunState.RUNNING_STALE}
            hasSidebar={showSidebar}
            isSidebarOpen={showSidebar && !isSidebarCollapsed}
            onToggleSidebar={toggleSidebar}
            navigation={
              navigationPosition === Navigation.Position.TOP &&
              appPages.length > 1 ? (
                <TopNav
                  endpoints={endpoints}
                  pageLinkBaseUrl={pageLinkBaseUrl}
                  currentPageScriptHash={currentPageScriptHash}
                  appPages={appPages}
                  onPageChange={onPageChange}
                />
              ) : null
            }
            rightContent={topRightContent}
            logoComponent={logoElement}
          />
          <Component
            tabIndex={0}
            isEmbedded={embedded}
            disableScrolling={disableScrolling}
            className="stMain"
            data-testid="stMain"
          >
            <Profiler id="Main">
              <StyledAppViewBlockContainer
                className="stMainBlockContainer block-container"
                data-testid="stMainBlockContainer"
                isWideMode={wideMode}
                showPadding={showPadding}
                addPaddingForHeader={
                  showToolbar ||
                  showColoredLine ||
                  navigationPosition === Navigation.Position.TOP
                }
                hasBottom={hasBottomElements}
                isEmbedded={embedded}
                hasSidebar={showSidebar}
              >
                {renderBlock(elements.main)}
              </StyledAppViewBlockContainer>
            </Profiler>
            {/* Anchor indicates to the iframe resizer that this is the lowest
        possible point to determine height. But we don't add an anchor if there is
        a bottom container in the app, since those two aspects don't work
        well together. */}
            {!hasBottomElements && (
              <StyledIFrameResizerAnchor
                data-testid="stAppIframeResizerAnchor"
                data-iframe-height
              />
            )}
            {hasBottomElements && (
              <Profiler id="Bottom">
                {/* We add spacing here to make sure that the sticky bottom is
           always pinned the bottom. Using sticky layout here instead of
           absolute / fixed is a trick to automatically account for the bottom
           height in the scroll area. Thereby, the bottom container will never
           cover something if you scroll to the end.*/}
                <StyledAppViewBlockSpacer />
                <StyledStickyBottomContainer
                  className="stBottom"
                  data-testid="stBottom"
                >
                  <StyledInnerBottomContainer>
                    <StyledBottomBlockContainer
                      data-testid="stBottomBlockContainer"
                      isWideMode={wideMode}
                      showPadding={showPadding}
                    >
                      {renderBlock(elements.bottom)}
                    </StyledBottomBlockContainer>
                  </StyledInnerBottomContainer>
                </StyledStickyBottomContainer>
              </Profiler>
            )}
          </Component>
        </StyledMainContent>
        {hasEventElements && (
          <Profiler id="Event">
            <EventContainer>
              <StyledEventBlockContainer
                className="stEvent"
                data-testid="stEvent"
              >
                {renderBlock(elements.event)}
              </StyledEventBlockContainer>
            </EventContainer>
          </Profiler>
        )}
      </StyledAppViewContainer>
    </>
  )
}

export default AppView
