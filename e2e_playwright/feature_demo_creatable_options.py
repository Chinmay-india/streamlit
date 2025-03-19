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

if "rerun_count" not in st.session_state:
    st.session_state.rerun_count = 0

accept_new_options = st.checkbox(
    "Accept new options",
    help=(
        "If checked, the selectbox and multiselect will accept dynamically"
        " added options."
    ),
)

options = ("apple", "banana")
if "my_selectbox" not in st.session_state and accept_new_options:
    st.session_state.my_selectbox = "foobar"
v1 = st.selectbox(
    "selectbox 1 (default)",
    options,
    accept_new_options=accept_new_options,
    key="my_selectbox",
)
st.write("value 1:", v1)

if "my_multiselect" not in st.session_state and accept_new_options:
    st.session_state.my_multiselect = ["hello world"]
v2 = st.multiselect(
    "multiselect 1",
    options,
    accept_new_options=accept_new_options,
    key="my_multiselect",
    max_selections=2,
)
st.write("value 2:", v2)

st.session_state.rerun_count += 1
st.write("session_state", st.session_state)
