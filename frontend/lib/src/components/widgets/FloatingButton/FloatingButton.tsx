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

import styled from "@emotion/styled"

import { FloatingButton as FloatingButtonProto } from "@streamlit/protobuf"

import BaseButton, {
  BaseButtonKind,
  BaseButtonSize,
  BaseButtonTooltip,
  DynamicButtonLabel,
} from "~lib/components/shared/BaseButton"
import { WidgetStateManager } from "~lib/WidgetStateManager"
import { Box } from "~lib/components/shared/Base/styled-components"

export interface Props {
  disabled: boolean
  element: FloatingButtonProto
  widgetMgr: WidgetStateManager
  fragmentId?: string
}

const FloatingButtonContainer = styled(Box)`
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 999;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 2rem;
  width: auto;
  height: auto;

  /* Ensure the button is properly centered */
  display: flex;
  align-items: center;
  justify-content: center;

  /* Ensure it appears on top of most UI components */
  z-index: 100;
`

const StyledButton = styled(BaseButton)`
  width: 100%;
  height: 100%;
  padding: 0;
  border-radius: 50% !important;

  /* Override any element size concerns */
  min-height: unset;
  max-height: unset;
`

function FloatingButton(props: Props): ReactElement {
  const { disabled, element, widgetMgr, fragmentId } = props

  let kind = BaseButtonKind.PRIMARY
  if (element.type === "secondary") {
    kind = BaseButtonKind.SECONDARY
  }

  return (
    <FloatingButtonContainer
      className="stFloatingButton"
      data-testid="stFloatingButton"
    >
      <BaseButtonTooltip help={element.help} containerWidth={false}>
        <StyledButton
          kind={kind}
          size={BaseButtonSize.SMALL}
          disabled={disabled}
          onClick={() =>
            widgetMgr.setTriggerValue(element, { fromUi: true }, fragmentId)
          }
        >
          <DynamicButtonLabel icon={element.icon} label={element.label} />
        </StyledButton>
      </BaseButtonTooltip>
    </FloatingButtonContainer>
  )
}

export default memo(FloatingButton)
