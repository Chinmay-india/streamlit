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

import React, { ReactElement, ReactNode, useContext } from "react"

import {
  BaseButton,
  BaseButtonKind,
  DynamicIcon,
  LibContext,
} from "@streamlit/lib"
import { useAppContext } from "@streamlit/app/src/components/StreamlitContextProvider"

import {
  StyledHeader,
  StyledHeaderContent,
  StyledHeaderLeftSection,
  StyledHeaderRightSection,
  StyledHeaderToolbar,
  StyledLogoContainer,
  StyledOpenSidebarButton,
} from "./styled-components"

export interface HeaderProps {
  hasSidebar: boolean
  isSidebarOpen: boolean
  onToggleSidebar(): void
  navigation?: ReactNode
  rightContent?: ReactNode
  logoComponent?: ReactNode
  isTransparentBackground?: boolean
}

const Header = ({
  hasSidebar,
  isSidebarOpen,
  onToggleSidebar,
  navigation,
  rightContent,
  logoComponent,
  isTransparentBackground,
}: HeaderProps): ReactElement => {
  const { showToolbar } = useAppContext()
  const { activeTheme } = useContext(LibContext)

  const hasContent = navigation || rightContent

  return (
    <StyledHeader
      tabIndex={-1} // required for testing
      className="stAppHeader"
      data-testid="stHeader"
      isTransparentBackground={isTransparentBackground}
    >
      {showToolbar && hasContent ? (
        <StyledHeaderToolbar
          className="stAppToolbar"
          data-testid="stToolbar"
          theme={activeTheme.emotion}
        >
          <StyledHeaderContent>
            <StyledHeaderLeftSection>
              {logoComponent && !isSidebarOpen ? (
                <StyledLogoContainer>{logoComponent}</StyledLogoContainer>
              ) : null}
              {hasSidebar && !isSidebarOpen && (
                <StyledOpenSidebarButton>
                  <BaseButton
                    kind={BaseButtonKind.HEADER_NO_PADDING}
                    onClick={onToggleSidebar}
                    data-testid="stExpandSidebarButton"
                  >
                    <DynamicIcon
                      size="xl"
                      iconValue={":material/keyboard_double_arrow_right:"}
                      color={activeTheme.emotion.colors.fadedText60}
                    />
                  </BaseButton>
                </StyledOpenSidebarButton>
              )}
            </StyledHeaderLeftSection>
            {navigation}
            {rightContent ? (
              <StyledHeaderRightSection>
                {rightContent}
              </StyledHeaderRightSection>
            ) : null}
          </StyledHeaderContent>
        </StyledHeaderToolbar>
      ) : null}
    </StyledHeader>
  )
}

export default Header
