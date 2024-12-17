# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
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
from __future__ import annotations

import streamlit as st

st.page_link(
    "pages/14_page_with_query_params_printout.py",
    query_params={"navigation": "from page link on page 1"},
    label="Go to page 14",
)

if st.button("Go to page 14"):
    st.switch_page(
        "pages/14_page_with_query_params_printout.py",
        query_params={"navigation": "from switch page on page 1"},
    )

st.button(
    "Go to page 14 with callback",
    on_click=lambda: st.switch_page(
        "pages/14_page_with_query_params_printout.py",
        query_params={"navigation": "from switch page callback on page 1"},
    ),
)
