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

import React, { memo, ReactElement } from "react"
import { MaskedInput } from "baseui/input"
import { useTheme } from "@emotion/react"
import { TextInput as TextInputProto } from "@streamlit/protobuf"

interface MaskedTextInputProps {
  uiValue: string
  placeholder?: string
  onBlur: () => void
  onFocus: () => void
  onChange: (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void
  onKeyPress: (
    event: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void
  disabled: boolean
  id: string
  element: TextInputProto
}

function MaskedTextInput({
  uiValue,
  placeholder,
  onBlur,
  onFocus,
  onChange,
  onKeyPress,
  disabled,
  id,
  element,
}: MaskedTextInputProps): ReactElement {
  const theme = useTheme()

  return (
    <MaskedInput
      value={uiValue}
      placeholder={placeholder}
      onBlur={onBlur}
      onFocus={onFocus}
      onChange={onChange}
      onKeyPress={onKeyPress}
      aria-label={element.label}
      disabled={disabled}
      id={id}
      type={
        element.type === TextInputProto.Type.PASSWORD ? "password" : "text"
      }
      autoComplete={element.autocomplete}
      mask={element.mask}
      overrides={{
        Input: {
          style: {
            minWidth: 0,
            "::placeholder": { opacity: "0.7" },
            lineHeight: theme.lineHeights.inputWidget,
            paddingRight: theme.spacing.sm,
            paddingLeft: theme.spacing.sm,
            paddingBottom: theme.spacing.sm,
            paddingTop: theme.spacing.sm,
          },
        },
        Root: {
          props: { "data-testid": "stTextInputRootElement" },
          style: {
            height: theme.sizes.minElementHeight,
            borderLeftWidth: theme.sizes.borderWidth,
            borderRightWidth: theme.sizes.borderWidth,
            borderTopWidth: theme.sizes.borderWidth,
            borderBottomWidth: theme.sizes.borderWidth,
          },
        },
      }}
    />
  )
}

export default memo(MaskedTextInput)
