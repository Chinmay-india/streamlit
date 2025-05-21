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

from pathlib import Path

import streamlit as st

dir_path = Path(__file__).parent

st.set_page_config(page_title="Hello", page_icon=":material/waving_hand:")
st.title("Welcome to Streamlit! 👋")
st.write(
    """
    Streamlit is an open-source app framework built specifically for
    machine learning and data science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    """
)
st.page_link(
    dir_path / "dataframe_demo.py",
    label="Go to the first demo",
    icon=":material/play_circle:",
)

st.header("Want to learn more?")
st.link_button(
    "Check out `streamlit.io`", "https://streamlit.io", icon=":material/open_in_new:"
)
st.link_button(
    "Jump into our documentation",
    "https://docs.streamlit.io",
    icon=":material/open_in_new:",
)
st.link_button(
    "Ask a question in our community forums",
    "https://discuss.streamlit.io",
    icon=":material/open_in_new:",
)

st.subheader("Other demos")
st.write(
    """
    - Use Streamlit with Snowflake to build [apps for your business](https://github.com/Snowflake-Labs/snowflake-demo-streamlit).
    - Use a neural net to analyze the Udacity's [image dataset for self-driving cars](https://github.com/streamlit/demo-self-driving).
    - Explore a New York City [rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups).
    - Explore the many apps created by the [Streamlit community](https://share.streamlit.io/explore?sort=most+viewed&category=favorites).
    """
)
