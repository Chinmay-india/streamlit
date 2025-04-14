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


def run_font_style_test():
    st.set_page_config(initial_sidebar_state="collapsed")

    st.header("NotoSans Font Test")

    # Test normal text
    st.markdown("This is normal text in NotoSans", key="normal_text")

    # Test italic text with markdown
    st.markdown("This has *italic text* in NotoSans", key="italic_text")

    # Test mixed formatting
    st.markdown(
        "This has both **bold** and *italic* text in NotoSans", key="mixed_text"
    )

    # Test code and italic together
    st.markdown("Code `example` with *italics* mixed in", key="code_italic")

    # Empty paragraph to create space
    st.markdown("")

    # A longer paragraph with mixed text
    st.markdown(
        "This is a longer paragraph with *italic phrases* mixed in throughout the text. "
        "The NotoSans font should properly render both the normal and *italic* variants "
        "to provide a consistent typography experience in the app.",
        key="long_paragraph",
    )


if __name__ == "__main__":
    run_font_style_test()
