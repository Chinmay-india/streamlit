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
import { AppContext } from "@streamlit/app/src/components/AppContext"
import {
  BaseButton,
  BaseButtonKind,
  DynamicIcon,
  LibContext,
} from "@streamlit/lib"
import {
  StyledHeader,
  StyledHeaderToolbar,
  StyledOpenSidebarButton,
  StyledHeaderContent,
  StyledHeaderLeftSection,
  StyledHeaderRightSection,
  StyledLogoContainer,
} from "./styled-components"
import { useAppContext } from "@streamlit/app/src/components/StreamlitContextProvider"
export interface HeaderProps {
  isStale?: boolean
  hasSidebar: boolean
  isSidebarOpen: boolean
  onToggleSidebar(): void
  navigation?: ReactNode
  rightContent?: ReactNode
  logoComponent?: ReactNode
}

const Header = ({
  isStale,
  hasSidebar,
  isSidebarOpen,
  onToggleSidebar,
  navigation,
  rightContent,
  logoComponent,
}: HeaderProps): ReactElement => {
  const { wideMode, embedded, showColoredLine } = useAppContext()
  const { activeTheme } = useContext(LibContext)

  // const showHeader = !embedded || showToolbar || showColoredLine
  const showHeader = true
  // const hasContent = navigation || rightContent
  const hasContent = true
  const showToolbar = true

  console.log({ isSidebarOpen, navigation, rightContent })

  return (
    <StyledHeader
      showHeader={showHeader}
      isWideMode={wideMode}
      tabIndex={-1} // required for testing
      isStale={isStale}
      className="stAppHeader"
      data-testid="stHeader"
    >
      {showToolbar && hasContent && (
        <StyledHeaderToolbar
          className="stAppToolbar"
          data-testid="stToolbar"
          theme={activeTheme.emotion}
        >
          <StyledHeaderContent>
            <StyledHeaderLeftSection>
              {logoComponent && !isSidebarOpen && (
                <StyledLogoContainer>{logoComponent}</StyledLogoContainer>
              )}
              {hasSidebar && !isSidebarOpen && (
                <StyledOpenSidebarButton>
                  <BaseButton
                    kind={BaseButtonKind.HEADER_NO_PADDING}
                    onClick={onToggleSidebar}
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
            {rightContent && (
              <StyledHeaderRightSection>
                {rightContent}
              </StyledHeaderRightSection>
            )}
          </StyledHeaderContent>
        </StyledHeaderToolbar>
      )}
    </StyledHeader>
  )
}

export default Header
