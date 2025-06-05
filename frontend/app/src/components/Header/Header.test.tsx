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

import { screen } from "@testing-library/react"

import { render } from "@streamlit/lib"
import * as StreamlitContextProviderModule from "@streamlit/app/src/components/StreamlitContextProvider"

import Header, { HeaderProps } from "./Header"

const getProps = (propOverrides: Partial<HeaderProps> = {}): HeaderProps => ({
  hasSidebar: false,
  isSidebarOpen: false,
  onToggleSidebar: vi.fn(),
  ...propOverrides,
})

describe("Header", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it("renders a Header without crashing", () => {
    render(<Header {...getProps()} />)

    expect(screen.getByTestId("stHeader")).toBeInTheDocument()
  })

  it("renders toolbar when showToolbar is true in context and content exists", () => {
    vi.spyOn(StreamlitContextProviderModule, "useAppContext").mockReturnValue({
      showToolbar: true,
      showColoredLine: true,
      widgetsDisabled: false,
      initialSidebarState: 1,
      pageLinkBaseUrl: "",
      currentPageScriptHash: "",
      onPageChange: vi.fn(),
      navSections: [],
      appPages: [],
      appLogo: null,
      sidebarChevronDownshift: 0,
      expandSidebarNav: false,
      hideSidebarNav: false,
      gitInfo: null,
    })

    render(<Header {...getProps({ navigation: <div>Nav</div> })} />)
    expect(screen.getByTestId("stToolbar")).toBeVisible()
  })

  it("does not render toolbar when showToolbar is false in context", () => {
    vi.spyOn(StreamlitContextProviderModule, "useAppContext").mockReturnValue({
      showToolbar: false,
      showColoredLine: true,
      widgetsDisabled: false,
      initialSidebarState: 1,
      pageLinkBaseUrl: "",
      currentPageScriptHash: "",
      onPageChange: vi.fn(),
      navSections: [],
      appPages: [],
      appLogo: null,
      sidebarChevronDownshift: 0,
      expandSidebarNav: false,
      hideSidebarNav: false,
      gitInfo: null,
    })

    render(<Header {...getProps({ navigation: <div>Nav</div> })} />)
    expect(screen.queryByTestId("stToolbar")).not.toBeInTheDocument()
  })

  it("does not render toolbar when no content exists", () => {
    vi.spyOn(StreamlitContextProviderModule, "useAppContext").mockReturnValue({
      showToolbar: true,
      showColoredLine: true,
      widgetsDisabled: false,
      initialSidebarState: 1,
      pageLinkBaseUrl: "",
      currentPageScriptHash: "",
      onPageChange: vi.fn(),
      navSections: [],
      appPages: [],
      appLogo: null,
      sidebarChevronDownshift: 0,
      expandSidebarNav: false,
      hideSidebarNav: false,
      gitInfo: null,
    })

    render(<Header {...getProps()} />) // No navigation or rightContent
    expect(screen.queryByTestId("stToolbar")).not.toBeInTheDocument()
  })

  it("renders with transparent background when isTransparentBackground is true", () => {
    render(<Header {...getProps({ isTransparentBackground: true })} />)

    const header = screen.getByTestId("stHeader")
    expect(header).toHaveStyle("background-color: rgba(0, 0, 0, 0)")
  })

  it("renders with default background when isTransparentBackground is false", () => {
    render(<Header {...getProps({ isTransparentBackground: false })} />)

    const header = screen.getByTestId("stHeader")
    // Check that it doesn't have transparent background
    expect(header).not.toHaveStyle("background-color: rgba(0, 0, 0, 0)")
  })

  it("renders navigation content in the left section", () => {
    const navigationContent = <div data-testid="test-nav">Navigation</div>
    render(<Header {...getProps({ navigation: navigationContent })} />)

    expect(screen.getByTestId("test-nav")).toBeInTheDocument()
    // Navigation is rendered directly in the toolbar, not in a specific section
    expect(screen.getByTestId("stToolbar")).toContainElement(
      screen.getByTestId("test-nav")
    )
  })

  it("renders right content in the right section", () => {
    const rightContent = <div data-testid="test-right">Right Content</div>
    render(<Header {...getProps({ rightContent })} />)

    expect(screen.getByTestId("test-right")).toBeInTheDocument()
    // Right content is rendered in the toolbar
    expect(screen.getByTestId("stToolbar")).toContainElement(
      screen.getByTestId("test-right")
    )
  })

  it("renders logo in the left section when provided", () => {
    const logo = <div data-testid="test-logo">Logo</div>
    render(<Header {...getProps({ logoComponent: logo })} />)

    expect(screen.getByTestId("test-logo")).toBeInTheDocument()
    // Logo is rendered in the toolbar
    expect(screen.getByTestId("stToolbar")).toContainElement(
      screen.getByTestId("test-logo")
    )
  })

  it("renders sidebar expand button when hasSidebar is true", () => {
    render(<Header {...getProps({ hasSidebar: true })} />)

    expect(screen.getByTestId("stExpandSidebarButton")).toBeInTheDocument()
  })

  it("does not render sidebar expand button when hasSidebar is false", () => {
    render(<Header {...getProps({ hasSidebar: false })} />)

    expect(
      screen.queryByTestId("stExpandSidebarButton")
    ).not.toBeInTheDocument()
  })

  it("calls onToggleSidebar when expand button is clicked", () => {
    const onToggleSidebar = vi.fn()
    render(<Header {...getProps({ hasSidebar: true, onToggleSidebar })} />)

    const expandButton = screen.getByTestId("stExpandSidebarButton")
    expandButton.click()

    expect(onToggleSidebar).toHaveBeenCalled()
  })
})
