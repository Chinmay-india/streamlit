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
import { render, screen, fireEvent } from "@testing-library/react"
import { vi } from "vitest"
import { IAppPage } from "@streamlit/protobuf"
import { TopNav } from "./index"
import { StyledOverflowContainer } from "./styled-components"
import { mockEndpoints } from "@streamlit/lib"

// Mock the Overflow component since we can't control responsive behavior in tests
vi.mock("rc-overflow", () => {
  return {
    default: ({
      component: Component,
      data,
      renderItem,
      renderRest,
    }: {
      component: React.ComponentType<any>
      data: any[]
      renderItem: (item: any, info: any) => React.ReactNode
      renderRest: (items: any[]) => React.ReactNode
    }) => {
      return (
        <Component>
          {data.map((item, i) => (
            <React.Fragment key={i} data-testid={`visible-item-${i}`}>
              {renderItem(item, {})}
            </React.Fragment>
          ))}
          <div data-testid="overflow-rest">{renderRest(data.slice(-2))}</div>
        </Component>
      )
    },
  }
})

const mockBuildAppPageURL = vi.fn(
  (baseUrl, page) => `${baseUrl}/${page.pageName}`
)
const endpoints = mockEndpoints({
  buildAppPageURL: mockBuildAppPageURL,
})

describe("TopNav", () => {
  const mockOnPageChange = vi.fn()
  const currentPageScriptHash = "page1hash"
  const pageLinkBaseUrl = "/"

  // Basic pages setup - no sections
  const basicPages: IAppPage[] = [
    { pageName: "Home", pageScriptHash: "page1hash" },
    { pageName: "About", pageScriptHash: "page2hash" },
    { pageName: "Contact", pageScriptHash: "page3hash" },
    { pageName: "Products", pageScriptHash: "page4hash" },
    { pageName: "Services", pageScriptHash: "page5hash" },
  ]

  // Pages with sections
  const pagesWithSections: IAppPage[] = [
    {
      pageName: "Overview",
      pageScriptHash: "page1hash",
      sectionHeader: "Main",
    },
    {
      pageName: "Details",
      pageScriptHash: "page2hash",
      sectionHeader: "Main",
    },
    { pageName: "Team", pageScriptHash: "page3hash", sectionHeader: "About" },
    {
      pageName: "History",
      pageScriptHash: "page4hash",
      sectionHeader: "About",
    },
    {
      pageName: "Support",
      pageScriptHash: "page5hash",
      sectionHeader: "Help",
    },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("renders navigation items correctly", () => {
    render(
      <TopNav
        currentPageScriptHash={currentPageScriptHash}
        appPages={basicPages}
        onPageChange={mockOnPageChange}
        pageLinkBaseUrl={pageLinkBaseUrl}
        endpoints={endpoints}
      />
    )

    // Check that visible items are rendered
    expect(screen.getByTestId("visible-item-0")).toBeInTheDocument()
    expect(screen.getByTestId("visible-item-1")).toBeInTheDocument()
    expect(screen.getByTestId("visible-item-2")).toBeInTheDocument()

    // Check that overflow is rendered
    expect(screen.getByTestId("overflow-rest")).toBeInTheDocument()
  })

  it("handles page navigation clicks", () => {
    render(
      <TopNav
        currentPageScriptHash={currentPageScriptHash}
        appPages={basicPages}
        onPageChange={mockOnPageChange}
        pageLinkBaseUrl={pageLinkBaseUrl}
        endpoints={endpoints}
      />
    )

    // Find and click on a navigation link
    const aboutLink = screen.getByText("About")
    fireEvent.click(aboutLink)

    // Check that onPageChange was called with the correct hash
    expect(mockOnPageChange).toHaveBeenCalledWith("page2hash")
  })

  it("renders sectioned navigation correctly", () => {
    render(
      <TopNav
        currentPageScriptHash={currentPageScriptHash}
        appPages={pagesWithSections}
        onPageChange={mockOnPageChange}
        pageLinkBaseUrl={pageLinkBaseUrl}
        endpoints={endpoints}
      />
    )

    // We should see section titles in the navigation
    const mainSectionItems = screen.getAllByText("Main")
    expect(mainSectionItems.length).toBeGreaterThan(0)
  })

  it("displays overflow items correctly", () => {
    render(
      <TopNav
        currentPageScriptHash={currentPageScriptHash}
        appPages={basicPages}
        onPageChange={mockOnPageChange}
        pageLinkBaseUrl={pageLinkBaseUrl}
        endpoints={endpoints}
      />
    )

    // Verify the overflow section exists
    const overflowSection = screen.getByTestId("overflow-rest")
    expect(overflowSection).toBeInTheDocument()

    // Verify correct number of additional items
    expect(screen.getByText("2 more")).toBeInTheDocument()
  })

  it("highlights the active page", () => {
    render(
      <TopNav
        currentPageScriptHash={currentPageScriptHash}
        appPages={basicPages}
        onPageChange={mockOnPageChange}
        pageLinkBaseUrl={pageLinkBaseUrl}
        endpoints={endpoints}
      />
    )

    // The Home link should be active
    const homeLink = screen.getByText("Home")
    expect(homeLink.closest("a")).toHaveAttribute("aria-current", "page")

    // Other links should not be active
    const aboutLink = screen.getByText("About")
    expect(aboutLink.closest("a")).not.toHaveAttribute("aria-current", "page")
  })
})
