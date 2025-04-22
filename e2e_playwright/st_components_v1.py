# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import streamlit.components.v1 as components

html = r"<h1>Hello, Streamlit!</h1>"
components.html(html, width=200, height=500, scrolling=False)

src = "http://not.a.real.url"
components.iframe(src, width=200, height=500, scrolling=True)

# Set a query parameter to ensure that it doesn't affect the path of the custom component,
# since that would trigger a reload if the query param changes
st.query_params["hello"] = "world"

url = "http://not.a.real.url"
test_component = components.declare_component("test_component", url=url)

test_component(key="component_1")


def get_html_content(title: str):
    return f"""<div>This is an html component! {title}</div>
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="200" fill="#e0e0e0"/>
  <text x="300" y="100" font-family="Arial" font-size="24" text-anchor="middle">600x200</text>
</svg>
<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="300" height="200" fill="#e0e0e0"/>
  <text x="150" y="100" font-family="Arial" font-size="24" text-anchor="middle">300x200</text>
</svg>
"""


# By default, this should take up the full height of the content
st.components.v1.html(
    get_html_content(
        "This should take up the full height of the content. There should not be a scrollbar because we are properly calculating the height at runtime."
    )
)

# This should take up 150px
st.components.v1.html(
    get_html_content("This should take up 150px. There should not be a scrollbar."),
    height=150,
)

# This should take up 150px and have a scrollbar
st.components.v1.html(
    get_html_content(
        "This should take up 150px. There should be a scrollbar because Scrolling=True"
    ),
    height=150,
    scrolling=True,
)

# This should take up the full height of the content (same as if we didn't
# specify height)
st.components.v1.html(
    get_html_content(
        "This should take up the full height of the content. There should not be a scrollbar because we are properly calculating the height at runtime."
    ),
    height="content",
)

# This should take up the full height of the content and there should not be a
# visible scrollbar because the height is properly calculated to the full height
# of the content
st.components.v1.html(
    get_html_content(
        "This should take up the full height of the content. There should not be a scrollbar because we are properly calculating the height at runtime."
    ),
    height="content",
    scrolling=True,
)
