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

import React, { useState } from "react"
import { PLACEMENT, TRIGGER_TYPE, Popover as UIPopover } from "baseui/popover"
import SidebarNavLink from "../Sidebar/SidebarNavLink"
import { Icon } from "@streamlit/lib"
import {
  KeyboardArrowDown,
  KeyboardArrowUp,
} from "@emotion-icons/material-outlined"
import { isNullOrUndefined } from "@streamlit/utils"
import { useTheme } from "@emotion/react"
import { hasLightBackgroundColor } from "@streamlit/lib"
import { transparentize } from "color2k"
import {
  StyledNavSection,
  StyledSidebarNavLinkContainer,
  StyledNavSectionText,
  StyledSectionName,
  StyledPopoverContent,
  StyledIconContainer,
} from "./styled-components"
import { IAppPage } from "@streamlit/protobuf"
import { StreamlitEndpoints } from "@streamlit/connection"

interface NavSectionProps {
  handlePageChange: (pageScriptHash: string) => void
  title: string
  sections: IAppPage[][]
  endpoints: StreamlitEndpoints
  pageLinkBaseUrl: string
  currentPageScriptHash: string
  hideChevron?: boolean
}

const NavSection = ({
  title,
  sections,
  handlePageChange,
  endpoints,
  pageLinkBaseUrl,
  currentPageScriptHash,
  hideChevron = false,
}: NavSectionProps) => {
  if (
    isNullOrUndefined(sections) ||
    sections.length === 0 ||
    sections[0].length === 0
  ) {
    return null
  }

  const [open, setOpen] = useState(false)
  const theme = useTheme()
  const lightBackground = hasLightBackgroundColor(theme)
  const showSections = sections.length > 1

  const hoverBgColor = transparentize(theme.colors.darkenedBgMix25, 0.1)

  return (
    <UIPopover
      triggerType={TRIGGER_TYPE.click}
      placement={PLACEMENT.bottomLeft}
      content={() => (
        <StyledPopoverContent>
          {sections.map((section, sectionIndex) => {
            const sectionName = section[0].sectionHeader

            return section.map((item, index) => {
              const handleClick = (e: React.MouseEvent) => {
                e.preventDefault()
                if (item.pageScriptHash) {
                  handlePageChange(item.pageScriptHash)
                }
                setOpen(false)
                return false
              }

              // Convert potentially null pageName to string safely
              const pageName = String(item.pageName || "")

              return (
                <React.Fragment key={`${sectionIndex}-${index}-${pageName}`}>
                  {index === 0 && showSections && (
                    <StyledSectionName>{sectionName}</StyledSectionName>
                  )}
                  <StyledSidebarNavLinkContainer>
                    <SidebarNavLink
                      {...item}
                      icon={item.icon || null}
                      isTopNav={true}
                      isActive={currentPageScriptHash === item.pageScriptHash}
                      onClick={handleClick}
                      pageUrl={endpoints.buildAppPageURL(
                        pageLinkBaseUrl,
                        item
                      )}
                    >
                      {pageName}
                    </SidebarNavLink>
                  </StyledSidebarNavLinkContainer>
                </React.Fragment>
              )
            })
          })}
        </StyledPopoverContent>
      )}
      isOpen={open}
      onClickOutside={() => setOpen(false)}
      onClick={() => (open ? setOpen(false) : undefined)}
      onEsc={() => setOpen(false)}
      // Consistently render the content for smoother opening/closing
      renderAll={true}
      overrides={{
        Body: {
          style: () => ({
            marginTop: theme.spacing.sm,
            marginRight: theme.spacing.lg,
            marginBottom: theme.spacing.lg,

            maxHeight: "70vh",
            overflow: "auto",
            maxWidth: `calc(${theme.sizes.contentMaxWidth} - 2*${theme.spacing.lg})`,

            borderTopLeftRadius: theme.radii.xl,
            borderTopRightRadius: theme.radii.xl,
            borderBottomRightRadius: theme.radii.xl,
            borderBottomLeftRadius: theme.radii.xl,

            borderLeftWidth: theme.sizes.borderWidth,
            borderRightWidth: theme.sizes.borderWidth,
            borderTopWidth: theme.sizes.borderWidth,
            borderBottomWidth: theme.sizes.borderWidth,

            borderLeftStyle: "solid",
            borderRightStyle: "solid",
            borderTopStyle: "solid",
            borderBottomStyle: "solid",

            borderLeftColor: theme.colors.borderColor,
            borderRightColor: theme.colors.borderColor,
            borderTopColor: theme.colors.borderColor,
            borderBottomColor: theme.colors.borderColor,

            boxShadow: lightBackground
              ? "0px 4px 16px rgba(0, 0, 0, 0.16)"
              : "0px 4px 16px rgba(0, 0, 0, 0.7)",

            [`@media (max-width: ${theme.breakpoints.sm})`]: {
              maxWidth: `calc(100% - ${theme.spacing.threeXL})`,
            },
          }),
        },
      }}
    >
      <div>
        <StyledNavSection
          tabIndex={0}
          onClick={() => setOpen(!open)}
          isOpen={open}
        >
          <StyledNavSectionText>{title}</StyledNavSectionText>
          {!hideChevron && (
            <StyledIconContainer>
              <Icon
                content={open ? KeyboardArrowUp : KeyboardArrowDown}
                size="lg"
              />
            </StyledIconContainer>
          )}
        </StyledNavSection>
      </div>
    </UIPopover>
  )
}

export default NavSection
