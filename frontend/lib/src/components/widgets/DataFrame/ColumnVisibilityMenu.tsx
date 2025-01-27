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

import React, { ReactElement } from "react"

import { useTheme } from "@emotion/react"
import { PLACEMENT, TRIGGER_TYPE, Popover as UIPopover } from "baseui/popover"
import { Visibility } from "@emotion-icons/material-outlined"
import {
  LABEL_PLACEMENT,
  STYLE_TYPE,
  Checkbox as UICheckbox,
} from "baseui/checkbox"
import { transparentize } from "color2k"

import { hasLightBackgroundColor } from "~lib/theme"

import { BaseColumn } from "./columns"

const NAMELESS_INDEX_NAME = "(index)"
export interface ColumnVisibilityMenuProps {
  columns: BaseColumn[]
  hideColumn: (columnId: string) => void
  showColumn: (columnId: string) => void
  children: React.ReactNode
  isOpen: boolean
  onClose: () => void
}

const ColumnVisibilityMenu: React.FC<ColumnVisibilityMenuProps> = ({
  columns,
  hideColumn,
  showColumn,
  children,
  isOpen,
  onClose,
}): ReactElement => {
  const theme = useTheme()

  return (
    <div data-testid="stPopover" className="stPopover">
      <UIPopover
        triggerType={TRIGGER_TYPE.click}
        placement={PLACEMENT.bottomRight}
        autoFocus={true}
        focusLock={true}
        content={() => (
          <div
            style={{
              paddingTop: theme.spacing.xs,
              paddingBottom: theme.spacing.xs,
            }}
          >
            {columns.map(column => (
              <UICheckbox
                key={column.id}
                checked={column.isHidden !== true}
                onChange={(e: React.ChangeEvent<HTMLInputElement>): void => {
                  if (e.target.checked) {
                    showColumn(column.id)
                  } else {
                    hideColumn(column.id)
                  }
                }}
                aria-label={column.title}
                checkmarkType={STYLE_TYPE.default}
                labelPlacement={LABEL_PLACEMENT.right}
                overrides={{
                  Root: {
                    style: ({
                      $isFocusVisible,
                    }: {
                      $isFocusVisible: boolean
                    }) => ({
                      marginBottom: theme.spacing.none,
                      marginTop: theme.spacing.none,
                      paddingLeft: theme.spacing.sm,
                      paddingRight: theme.spacing.sm,
                      paddingTop: theme.spacing.twoXS,
                      paddingBottom: theme.spacing.twoXS,
                      backgroundColor: $isFocusVisible
                        ? theme.colors.darkenedBgMix25
                        : "",
                      display: "flex",
                      alignItems: "start",
                    }),
                  },
                  Checkmark: {
                    style: ({
                      $isFocusVisible,
                      $checked,
                    }: {
                      $isFocusVisible: boolean
                      $checked: boolean
                    }) => {
                      const borderColor = $checked
                        ? theme.colors.primary
                        : theme.colors.fadedText40

                      return {
                        outline: 0,
                        width: theme.sizes.checkbox,
                        height: theme.sizes.checkbox,
                        marginTop: theme.spacing.twoXS,
                        marginLeft: 0,
                        marginBottom: 0,
                        boxShadow:
                          $isFocusVisible && $checked
                            ? `0 0 0 0.2rem ${transparentize(
                                theme.colors.primary,
                                0.5
                              )}`
                            : "",
                        // This is painfully verbose, but baseweb seems to internally
                        // use the long-hand version, which means we can't use the
                        // shorthand names here as if we do we'll end up with warn
                        // logs spamming us every time a checkbox is rendered.
                        borderLeftWidth: theme.sizes.borderWidth,
                        borderRightWidth: theme.sizes.borderWidth,
                        borderTopWidth: theme.sizes.borderWidth,
                        borderBottomWidth: theme.sizes.borderWidth,
                        borderLeftColor: borderColor,
                        borderRightColor: borderColor,
                        borderTopColor: borderColor,
                        borderBottomColor: borderColor,
                      }
                    },
                  },
                  Label: {
                    style: {
                      lineHeight: theme.lineHeights.small,
                      paddingLeft: theme.spacing.sm,
                      position: "relative",
                      color: theme.colors.bodyText,
                      fontSize: theme.fontSizes.sm,
                      fontWeight: theme.fontWeights.normal,
                    },
                  },
                }}
              >
                {!column.title && column.isIndex
                  ? NAMELESS_INDEX_NAME
                  : column.title}
              </UICheckbox>
            ))}
          </div>
        )}
        isOpen={isOpen}
        onClickOutside={onClose}
        onClick={() => (isOpen ? onClose() : undefined)}
        onEsc={onClose}
        ignoreBoundary={false}
        overrides={{
          Body: {
            props: {
              "data-testid": "stDataFrameColumnVisibilityMenu",
            },
            style: {
              // This is annoying, but a bunch of warnings get logged when the
              // shorthand version `borderRadius` is used here since the long
              // names are used by BaseWeb and mixing the two is apparently
              // bad :(
              borderTopLeftRadius: theme.radii.md,
              borderTopRightRadius: theme.radii.md,
              borderBottomLeftRadius: theme.radii.md,
              borderBottomRightRadius: theme.radii.md,

              paddingTop: "0 !important",
              paddingBottom: "0 !important",
              paddingLeft: "0 !important",
              paddingRight: "0 !important",

              backgroundColor: "transparent",
              border: `${theme.sizes.borderWidth} solid ${theme.colors.borderColor}`,
            },
          },
          Inner: {
            style: {
              backgroundColor: hasLightBackgroundColor(theme)
                ? theme.colors.bgColor
                : theme.colors.secondaryBg,
              color: theme.colors.bodyText,
              fontSize: theme.fontSizes.sm,
              fontWeight: theme.fontWeights.normal,
              minWidth: "7rem",
              maxWidth: "15rem",
              maxHeight: "15rem",
              overflow: "auto",
              // See the long comment about `borderRadius`. The same applies here
              // to `padding`.
              paddingTop: "0 !important",
              paddingBottom: "0 !important",
              paddingLeft: "0 !important",
              paddingRight: "0 !important",
            },
          },
        }}
      >
        {<div>{children}</div>}
      </UIPopover>
    </div>
  )
}

export default ColumnVisibilityMenu
