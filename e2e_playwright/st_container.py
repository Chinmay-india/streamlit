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

import pandas as pd
import plotly.express as px

import streamlit as st

container = st.container(key="first container")

st.write("Line 1")
container.write("Line 2")
with container:
    "Line 3"
st.write("Line 4")

# Ensure widget states persist when React nodes shift
if st.button("Step 2: Press me"):
    st.header("Pressed!")
c = st.container()
if c.checkbox("Step 1: Check me"):
    c.title("Checked!")

with st.container(border=True):
    st.markdown(
        "This is inside a container with a border. And it doesn't overflow "
        "the borders if the text requires multiple lines."
    )
    st.button("Stretch full width", use_container_width=True)

with st.container(height=200):
    st.markdown("This is inside a scrolling container.")
    st.text_input("Widget in scroll container")

    for i in range(10):
        st.markdown(f"Message {i}")

empty_container = st.container(height=100)

if st.button("Add message"):
    empty_container.chat_message("user").write("Hello world")

with st.container(height=200):
    for i in range(10):
        st.chat_message("user").write(f"Message {i}")

with st.container(background_color="red", height=200, key="red_container"):
    st.markdown("This is inside a container with a red background.")
    st.text_input("Widget in red container")

with st.container(background_color="blue", height=200, key="blue_container"):
    st.markdown(
        "This is inside a container with a blue background. Chart with transparent background."
    )
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    fig = px.line(df, x="x", y="y")
    # This is what we need to do to make the background transparent
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
