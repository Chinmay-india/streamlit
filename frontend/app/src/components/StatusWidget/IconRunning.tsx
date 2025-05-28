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

import React, { useEffect, useState } from "react"

import { useTheme } from "@emotion/react"
import {
  AccessibilityNew,
  AccessibleForward,
  DirectionsBike,
  DirectionsRun,
  Pool,
  Rowing,
} from "@emotion-icons/material-outlined"

import { EmotionTheme, hasLightBackgroundColor } from "@streamlit/lib"

// Create an array of icons with their names, should be changed as per requirement
const icons = [
  { component: AccessibleForward, name: "accessible-forward" },
  { component: AccessibilityNew, name: "accessibility-new" },
  { component: DirectionsBike, name: "directions-bike" },
  { component: DirectionsRun, name: "directions-run" },
  { component: Pool, name: "pool" },
  { component: Rowing, name: "rowing" },
]

type IconRunningProps = {
  size?: number
  speed?: number
  color?: string
}

const IconRunning: React.FC<IconRunningProps> = ({ speed = 200, color }) => {
  const [index, setIndex] = useState(0)
  const theme = useTheme() as EmotionTheme

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex(prev => (prev + 1) % icons.length)
    }, speed)
    return () => clearInterval(interval)
  }, [speed])

  const currentIcon = icons[index]
  const IconComponent = currentIcon.component
  // const resolvedColor =  theme.colors.gray85 || theme.colors.white
  const resolvedColor = !hasLightBackgroundColor(theme)
    ? theme.colors.white
    : theme.colors.gray85
  const ariaLabel = `Running ${currentIcon.name} icon`
  const sizeIcon = theme.sizes.appRunningMen
  return (
    <div
      style={{
        width: sizeIcon,
        height: sizeIcon,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "opacity 0.3s ease-in-out",
        border: `1px solid ${theme.colors.border}`,
      }}
      role="img"
      aria-label={ariaLabel}
    >
      <IconComponent
        size={sizeIcon}
        color={resolvedColor}
        aria-hidden="true"
      />
      {/* <IconComponent size={sizeIcon} aria-hidden="true" /> */}
    </div>
  )
}

export default IconRunning
