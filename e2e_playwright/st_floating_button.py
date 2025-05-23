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

st.title("Floating Button Tests")

# Add some content to show the floating button is fixed at the bottom right
st.markdown(
    "### This is some content to demonstrate that the floating button stays fixed"
)
st.write("The floating button should appear at the bottom right of the screen")

# Test different configurations of floating buttons
# We can only have one floating button at a time, so we use checkboxes to control which one is shown

button_options = [
    "Default Button",
    "Primary Button",
    "Secondary Button",
    "Button with Icon",
    "Button with Material Icon",
    "Button with Tooltip",
    "Disabled Button",
    "Button with Callback",
]

selected_option = st.selectbox("Select floating button to display:", button_options)

# Clear the flag to allow us to create a new floating button
# Note: This is for testing purposes - users shouldn't have to do this
if "floating_button_created" in st.session_state:
    del st.session_state.floating_button_created

# Track button clicks
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
    st.session_state.click_count = 0


def on_button_click():
    st.session_state.button_clicked = True
    st.session_state.click_count += 1


# Display status of button click
if st.session_state.button_clicked:
    st.success(f"Button was clicked! Click count: {st.session_state.click_count}")

# Reset button click status
if st.button("Reset Click Status"):
    st.session_state.button_clicked = False
    st.session_state.click_count = 0

# Create the selected floating button type
if selected_option == "Default Button":
    st.floating_button("Default Floating Button")

elif selected_option == "Primary Button":
    st.floating_button("Primary Floating Button", type="primary")

elif selected_option == "Secondary Button":
    st.floating_button("Secondary Floating Button", type="secondary")

elif selected_option == "Button with Icon":
    st.floating_button("Icon Button", icon="🚀")

elif selected_option == "Button with Material Icon":
    st.floating_button("Chat", icon=":material/chat:")

elif selected_option == "Button with Tooltip":
    st.floating_button("Help", help="This is a floating action button with a tooltip")

elif selected_option == "Disabled Button":
    st.floating_button("Disabled Button", disabled=True)

elif selected_option == "Button with Callback":
    if st.floating_button("Click Me", on_click=on_button_click):
        # This should not appear since the callback is triggered before this
        st.write("Button was clicked directly!")

# Add more content to demonstrate scrolling
st.markdown("### More content to demonstrate scrolling")
for i in range(10):
    st.write(
        f"Line {i + 1} of content - The floating button should stay fixed while scrolling"
    )

st.markdown("### End of content")
