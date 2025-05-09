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

import styled from "@emotion/styled"
import { getNavTextColor } from "../Sidebar/styled-components"
import { transparentize } from "color2k"

export const StyledOverflowContainer = styled.div({
  display: "flex",
  alignItems: "center",
  width: "100%",
  flexShrink: 1,
  overflow: "hidden",
})

interface StyledNavSectionProps {
  isOpen: boolean
}

export const StyledNavSection = styled.div<StyledNavSectionProps>(
  ({ theme, isOpen }) => ({
    marginLeft: theme.spacing.sm,
    marginRight: theme.spacing.sm,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    position: "relative",
    lineHeight: theme.lineHeights.menuItem,
    fontSize: theme.fontSizes.sm,
    padding: `0 ${theme.spacing.sm}`,
    color: getNavTextColor(theme, false, false, true),
    borderRadius: theme.radii.default,
    ...(isOpen ? { backgroundColor: theme.colors.darkenedBgMix25 } : {}),
    "&:hover": {
      backgroundColor: theme.colors.darkenedBgMix15,
    },
  })
)

export const StyledTopNavLinkContainer = styled.div(({ theme }) => ({
  margin: `${theme.spacing.sm} ${theme.spacing.sm}`,
}))

export const StyledNavSectionText = styled.span(({ theme }) => ({
  textWrap: "nowrap",
}))

export const StyledSidebarNavLinkContainer = styled.div(({ theme }) => ({
  margin: `${theme.spacing.twoXS} ${theme.spacing.sm}`,
}))

export const StyledSectionName = styled.div(({ theme }) => ({
  marginLeft: theme.spacing.sm,
  marginTop: theme.spacing.sm,
  marginBottom: theme.spacing.sm,
}))

export const StyledPopoverContent = styled.div(({ theme }) => ({
  padding: `${theme.spacing.twoXS} 0`,
  fontSize: theme.fontSizes.sm,
}))

export const StyledIconContainer = styled.div(({ theme }) => ({
  marginLeft: theme.spacing.twoXS,
}))
