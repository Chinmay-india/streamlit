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

// Import icons from @emotion-icons/material-outlined
import { AccessibleForward } from "@emotion-icons/material-outlined"
import { AccessibilityNew } from "@emotion-icons/material-outlined"
import { DirectionsBike } from "@emotion-icons/material-outlined"
import { DirectionsRun } from "@emotion-icons/material-outlined"
import { Pool } from "@emotion-icons/material-outlined"
import { Rowing } from "@emotion-icons/material-outlined"

const icons = [
  AccessibleForward,
  AccessibilityNew,
  DirectionsBike,
  DirectionsRun,
  Pool,
  Rowing,
]

const IconRunning = ({ size = 64, speed = 600, color = "#1976d2" }) => {
  const [index, setIndex] = useState(0)
  // Speed adjustment here
  useEffect(() => {
    const interval = setInterval(() => {
      setIndex(prev => (prev + 1) % icons.length)
    }, speed)
    return () => clearInterval(interval)
  }, [speed])

  const IconComponent = icons[index]

  //Customizetions
  return (
    <div
      style={{
        width: size,
        height: size,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "opacity 0.3s ease-in-out",
      }}
    >
      <IconComponent size={size} color={color} />
    </div>
  )
}

export default IconRunning
