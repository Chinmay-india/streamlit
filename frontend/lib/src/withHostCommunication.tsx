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
import { Quiver } from "./dataframes/Quiver"
import ArrowTable from "./components/elements/ArrowTable"

export function withHostCommunication(WrappedComponent: React.ComponentType) {
  return function WithHostCommunication(props: any) {
    const renderElement = (element: any) => {
      switch (element.type) {
        case "arrowTable": {
          const quiver = new Quiver(element.arrowTable)
          return (
            <ArrowTable
              element={quiver}
              altText={element.arrowTable.alt_text}
            />
          )
        }
        default:
          return <WrappedComponent {...props} />
      }
    }

    return renderElement(props.element)
  }
}
