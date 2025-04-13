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

st.title("Width and Scale Parameters Test App")
st.write("""
This app demonstrates how the new `width` and `scale` parameters affect the appearance of various Streamlit widgets:
- Checkboxes and Toggles
- Radio buttons
- Color pickers
- Button group widgets (Feedback, Pills, Segmented Control)
- File Upload widgets (audio_input, camera_input, file_uploader)

Compare the different width options: 'content' (default), 'stretch', and fixed pixel width, as well as different scale values.
""")

# Section 1: Checkbox with different width options
st.header("1. Checkboxes with Different Width Options")

st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.checkbox("Default width='content'", key="cb_default")
    # Stretch width
    st.checkbox("Width='stretch'", width="stretch", key="cb_stretch")
    # Fixed pixel width
    st.checkbox("Width=300px", width=300, key="cb_300px")

# Section 2: Toggle with different width options
st.header("2. Toggles with Different Width Options")

st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.toggle("Default width='content'", key="tg_default")
    # Stretch width
    st.toggle("Width='stretch'", width="stretch", key="tg_stretch")
    # Fixed pixel width
    st.toggle("Width=300px", width=300, key="tg_300px")

# Section 3: Different scale values
st.header("3. Widgets with Different Scale Values")

st.subheader("Checkboxes with Different Scales")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.checkbox("Scale=1", scale=1, width="stretch", key="cb_scale1")
    # Scale 2
    st.checkbox("Scale=2", scale=2, width="stretch", key="cb_scale2")
    # Scale 3
    st.checkbox("Scale=3", scale=3, width="stretch", key="cb_scale3")

st.subheader("Toggles with Different Scales")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.toggle("Scale=1", scale=1, width="stretch", key="tg_scale1")
    # Scale 2
    st.toggle("Scale=2", scale=2, width="stretch", key="tg_scale2")
    # Scale 3
    st.toggle("Scale=3", scale=3, width="stretch", key="tg_scale3")

# Section 4: Combinations of width and scale
st.header("4. Combinations of Width and Scale")

st.subheader("Checkboxes with Combined Options")
st.write("Various combinations of width and scale:")
with st.container(border=True, direction="horizontal", gap="large"):
    st.checkbox("Default width & scale", key="cb_default_combo")
    st.checkbox("Stretch width", width="stretch", key="cb_stretch_default_scale")
    st.checkbox(
        "Scale=2, width=stretch", scale=2, width="stretch", key="cb_scale2_stretch"
    )

with st.container(border=True, direction="horizontal", gap="large"):
    st.checkbox("300px width", width=300, key="cb_300px_default_scale")
    st.checkbox(
        "Scale=3, width=stretch", scale=3, width="stretch", key="cb_scale3_stretch"
    )

st.subheader("Toggles with Combined Options")
st.write("Various combinations of width and scale:")
with st.container(border=True, direction="horizontal", gap="large"):
    st.toggle("Default width & scale", key="tg_default_combo")
    st.toggle("Stretch width", width="stretch", key="tg_stretch_default_scale")
    st.toggle(
        "Scale=2, width=stretch", scale=2, width="stretch", key="tg_scale2_stretch"
    )

with st.container(border=True, direction="horizontal", gap="large"):
    st.toggle("300px width", width=300, key="tg_300px_default_scale")
    st.toggle(
        "Scale=3, width=stretch", scale=3, width="stretch", key="tg_scale3_stretch"
    )

# Section 5: Container examples
st.header("5. Container Examples")

st.subheader("Checkboxes and Toggles Together")
with st.container(border=True, direction="horizontal", gap="large"):
    st.checkbox("Default checkbox", key="cb_mixed1")
    st.toggle("Default toggle", key="tg_mixed1")
    st.checkbox("Stretch checkbox", width="stretch", key="cb_mixed2")
    st.toggle("Stretch toggle", width="stretch", key="tg_mixed2")

with st.container(border=True, direction="horizontal", gap="large"):
    st.checkbox("Scale=2 checkbox", scale=2, width="stretch", key="cb_mixed3")
    st.toggle("Scale=2 toggle", scale=2, width="stretch", key="tg_mixed3")
    st.checkbox("Fixed 200px checkbox", width=200, key="cb_mixed4")
    st.toggle("Fixed 200px toggle", width=200, key="tg_mixed4")

# Section 6: Long Label Tests
st.header("6. Tests with Long Labels")

st.subheader("Checkboxes with Long Labels")
st.write("Compare how different width options affect long labels:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.checkbox(
        "This is a very long checkbox label that demonstrates how text wrapping works with the default content width setting. The label should wrap based on available space.",
        key="cb_long_default",
    )

    # Stretch width
    st.checkbox(
        "This is a very long checkbox label with width='stretch' that demonstrates how text wrapping works when the container is stretched. The wrapping behavior might differ from the default.",
        width="stretch",
        key="cb_long_stretch",
    )

    # Fixed pixel width
    st.checkbox(
        "This is a very long checkbox label with width=300px that demonstrates how text wrapping works when the container has a fixed width. The wrapping should be constrained to 300px.",
        width=300,
        key="cb_long_300px",
    )

st.write("Long labels with different scale values:")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.checkbox(
        "Scale=1: This checkbox has a long label and demonstrates the default scale with width='stretch'.",
        scale=1,
        width="stretch",
        key="cb_long_scale1",
    )

    # Scale 2
    st.checkbox(
        "Scale=2: This checkbox has a long label and demonstrates a larger scale with width='stretch'.",
        scale=2,
        width="stretch",
        key="cb_long_scale2",
    )

    # Scale 3
    st.checkbox(
        "Scale=3: This checkbox has a long label and demonstrates an even larger scale with width='stretch'.",
        scale=3,
        width="stretch",
        key="cb_long_scale3",
    )

st.subheader("Toggles with Long Labels")
st.write("Compare how different width options affect long labels:")
with st.container(border=True, direction="horizontal", gap="large", wrap=False):
    # Content width (default)
    st.toggle(
        "This is a very long toggle label that demonstrates how text wrapping works with the default content width setting. The label should wrap based on available space.",
        key="tg_long_default",
    )

    # Stretch width
    st.toggle(
        "This is a very long toggle label with width='stretch' that demonstrates how text wrapping works when the container is stretched. The wrapping behavior might differ from the default.",
        width="stretch",
        key="tg_long_stretch",
    )

    # Fixed pixel width
    st.toggle(
        "This is a very long toggle label with width=300px that demonstrates how text wrapping works when the container has a fixed width. The wrapping should be constrained to 300px.",
        width=300,
        key="tg_long_300px",
    )

st.write("Long labels with different scale values:")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.toggle(
        "Scale=1: This toggle has a long label and demonstrates the default scale with width='stretch'.",
        scale=1,
        width="stretch",
        key="tg_long_scale1",
    )

    # Scale 2
    st.toggle(
        "Scale=2: This toggle has a long label and demonstrates a larger scale with width='stretch'.",
        scale=2,
        width="stretch",
        key="tg_long_scale2",
    )

    # Scale 3
    st.toggle(
        "Scale=3: This toggle has a long label and demonstrates an even larger scale with width='stretch'.",
        scale=3,
        width="stretch",
        key="tg_long_scale3",
    )

# Section 7: Radio Button Tests
st.header("7. Radio Button Tests")

st.subheader("Radio with Different Width Options")
st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.radio(
        "Default width='content'",
        options=["Option 1", "Option 2", "Option 3"],
        key="radio_default",
    )

    # Stretch width
    st.radio(
        "Width='stretch'",
        options=["Option 1", "Option 2", "Option 3"],
        width="stretch",
        key="radio_stretch",
    )

    # Fixed pixel width
    st.radio(
        "Width=300px",
        options=["Option 1", "Option 2", "Option 3"],
        width=300,
        key="radio_300px",
    )

st.subheader("Radio with Different Scale Values")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="small"):
    # Scale 1 (default)
    st.radio(
        "Scale=1",
        options=["Option 1", "Option 2"],
        scale=1,
        width="stretch",
        key="radio_scale1",
        horizontal=True,
    )

    # Scale 2
    st.radio(
        "Scale=2",
        options=["Option 1", "Option 2"],
        scale=2,
        width="stretch",
        key="radio_scale2",
        horizontal=True,
    )

    # Scale 3
    st.radio(
        "Scale=3",
        options=["Option 1", "Option 2"],
        scale=3,
        width="stretch",
        key="radio_scale3",
        horizontal=True,
    )

st.subheader("Radio with Horizontal Layout")
st.write("Horizontal layout with different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width horizontal
    st.radio(
        "Default width='content' (horizontal)",
        options=["Option 1", "Option 2", "Option 3"],
        horizontal=True,
        key="radio_horizontal_default",
    )

    # Stretch width horizontal
    st.radio(
        "Width='stretch' (horizontal)",
        options=["Option 1", "Option 2", "Option 3"],
        horizontal=True,
        width="stretch",
        key="radio_horizontal_stretch",
    )

    # Fixed width horizontal
    st.radio(
        "Width=400px (horizontal)",
        options=["Option 1", "Option 2", "Option 3"],
        horizontal=True,
        width=400,
        key="radio_horizontal_400px",
    )

st.subheader("Radio with Long Labels")
st.write("Compare how different width options affect long labels:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.radio(
        "This is a very long radio group label that demonstrates how text wrapping works with the default content width setting.",
        options=[
            "This is a long option that demonstrates wrapping",
            "Another long option that should wrap properly when needed",
            "A third option with enough text to force wrapping behavior",
        ],
        key="radio_long_default",
    )

    # Stretch width
    st.radio(
        "This is a very long radio group label with width='stretch'.",
        options=[
            "This is a long option that demonstrates wrapping with stretch",
            "Another long option that should wrap properly when stretched",
            "A third option with enough text to force wrapping behavior",
        ],
        width="stretch",
        key="radio_long_stretch",
    )

    # Fixed pixel width
    st.radio(
        "This is a very long radio group label with width=300px.",
        options=[
            "This is a long option that demonstrates wrapping with fixed width",
            "Another long option that should wrap when width is constrained",
            "A third option with enough text to force wrapping behavior",
        ],
        width=300,
        key="radio_long_300px",
    )

# Section 8: Interactive demo
st.header("8. Interactive Demo")

# Replace columns with regular layout
width_option = st.radio(
    "Select width option:",
    ["content", "stretch", "300"],
    horizontal=True,
    key="width_selector",
)

# Convert to appropriate type for width
if width_option == "300":
    width_value = 300
else:
    width_value = width_option

scale_value = st.slider("Scale value:", 1, 5, 1, key="scale_selector")

# Force width to stretch when scale > 1
if scale_value > 1 and width_value != "stretch":
    st.info("Setting width='stretch' since scale > 1")
    width_value = "stretch"

st.subheader("Interactive Demo Result")
with st.container(border=True, direction="horizontal", gap="large"):
    interactive_cb = st.checkbox(
        f"Checkbox (width='{width_option}', scale={scale_value})",
        width=width_value,
        scale=scale_value,
        key="interactive_cb",
    )

    interactive_tg = st.toggle(
        f"Toggle (width='{width_option}', scale={scale_value})",
        width=width_value,
        scale=scale_value,
        key="interactive_tg",
    )

    interactive_radio = st.radio(
        f"Radio (width='{width_option}', scale={scale_value})",
        options=["Option A", "Option B"],
        width=width_value,
        scale=scale_value,
        key="interactive_radio",
    )

    interactive_color = st.color_picker(
        f"Color (width='{width_option}', scale={scale_value})",
        value="#2ecc71",
        width=width_value,
        scale=scale_value,
        key="interactive_color",
    )

# Section 9: Color Picker Tests
st.header("9. Color Picker Tests")

st.subheader("Color Picker with Different Width Options")
st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.color_picker(
        "Default width='content'", value="#1abc9c", key="color_picker_default"
    )

    # Stretch width
    st.color_picker(
        "Width='stretch'", value="#3498db", width="stretch", key="color_picker_stretch"
    )

    # Fixed pixel width
    st.color_picker("Width=300px", value="#9b59b6", width=300, key="color_picker_300px")

st.subheader("Color Picker with Different Scale Values")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.color_picker(
        "Scale=1", value="#e74c3c", scale=1, width="stretch", key="color_picker_scale1"
    )

    # Scale 2
    st.color_picker(
        "Scale=2", value="#f1c40f", scale=2, width="stretch", key="color_picker_scale2"
    )

    # Scale 3
    st.color_picker(
        "Scale=3", value="#2ecc71", scale=3, width="stretch", key="color_picker_scale3"
    )

st.subheader("Color Picker with Long Labels")
st.write("Compare how different width options affect long labels:")
with st.container(border=True, direction="vertical", gap="large"):
    # Content width (default)
    st.color_picker(
        "This is a very long color picker label that demonstrates how text wrapping works with the default content width setting.",
        value="#e67e22",
        key="color_picker_long_default",
    )

    # Stretch width
    st.color_picker(
        "This is a very long color picker label with width='stretch'.",
        value="#16a085",
        width="stretch",
        key="color_picker_long_stretch",
    )

    # Fixed pixel width
    st.color_picker(
        "This is a very long color picker label with width=300px.",
        value="#8e44ad",
        width=300,
        key="color_picker_long_300px",
    )

# Update sidebar to include color pickers
st.sidebar.subheader("Color Pickers")
with st.sidebar.container(gap="small"):
    st.sidebar.color_picker("Default width", value="#3498db", key="sb_color_picker1")
    st.sidebar.color_picker(
        "Stretch width", value="#e74c3c", width="stretch", key="sb_color_picker2"
    )
    st.sidebar.color_picker(
        "200px width", value="#2ecc71", width=200, key="sb_color_picker3"
    )
    st.sidebar.color_picker(
        "Scale=2", value="#f1c40f", scale=2, width="stretch", key="sb_color_picker4"
    )

# Section 10: In a sidebar
st.sidebar.header("Sidebar Tests")
st.sidebar.subheader("Checkboxes")
with st.sidebar.container(gap="small"):
    st.sidebar.checkbox("Default width", key="sb_cb1")
    st.sidebar.checkbox("Stretch width", width="stretch", key="sb_cb2")
    st.sidebar.checkbox("200px width", width=200, key="sb_cb3")
    st.sidebar.checkbox("Scale=2", scale=2, width="stretch", key="sb_cb4")

st.sidebar.subheader("Toggles")
with st.sidebar.container(gap="small"):
    st.sidebar.toggle("Default width", key="sb_tg1")
    st.sidebar.toggle("Stretch width", width="stretch", key="sb_tg2")
    st.sidebar.toggle("200px width", width=200, key="sb_tg3")
    st.sidebar.toggle("Scale=2", scale=2, width="stretch", key="sb_tg4")

st.sidebar.subheader("Radio Buttons")
with st.sidebar.container(gap="small"):
    st.sidebar.radio("Default width", options=["Option 1", "Option 2"], key="sb_radio1")
    st.sidebar.radio(
        "Stretch width",
        options=["Option 1", "Option 2"],
        width="stretch",
        key="sb_radio2",
    )
    st.sidebar.radio(
        "200px width", options=["Option 1", "Option 2"], width=200, key="sb_radio3"
    )
    st.sidebar.radio(
        "Scale=2",
        options=["Option 1", "Option 2"],
        scale=2,
        width="stretch",
        key="sb_radio4",
    )

# Section 11: Button Group Tests
st.header("11. Button Group Tests")

st.subheader("Feedback Widget Tests")
st.write("Compare different width options for feedback widgets:")

with st.container(border=True, direction="vertical", gap="large"):
    st.write("Thumbs feedback with different width options:")
    with st.container(border=True, direction="vertical", gap="large"):
        # Content width (default)
        st.feedback("thumbs", key="feedback_thumbs_default")

        # Stretch width
        st.feedback("thumbs", width="stretch", key="feedback_thumbs_stretch")

        # Fixed pixel width
        st.feedback("thumbs", width=300, key="feedback_thumbs_300px")

    st.write("Stars feedback with different width options:")
    with st.container(border=True, direction="vertical", gap="large"):
        # Content width (default)
        st.feedback("stars", key="feedback_stars_default")

        # Stretch width
        st.feedback("stars", width="stretch", key="feedback_stars_stretch")

        # Fixed pixel width
        st.feedback("stars", width=300, key="feedback_stars_300px")

    st.write("Feedback widgets with different scale values (width='stretch'):")
    with st.container(border=True, direction="vertical", gap="large"):
        # Scale 1 (default)
        st.feedback("thumbs", scale=1, width="stretch", key="feedback_scale1")

        # Scale 2
        st.feedback("thumbs", scale=2, width="stretch", key="feedback_scale2")

        # Scale 3
        st.feedback("thumbs", scale=3, width="stretch", key="feedback_scale3")

st.subheader("Pills Widget Tests")
st.write("Compare different width options for pills widgets:")

with st.container(border=True, direction="vertical", gap="large"):
    st.write("Single-select pills with different width options:")
    with st.container(border=True, direction="vertical", gap="large"):
        # Content width (default)
        st.pills(
            "Default width='content'",
            options=["Option 1", "Option 2", "Option 3"],
            key="pills_default",
        )

        # Stretch width
        st.pills(
            "Width='stretch'",
            options=["Option 1", "Option 2", "Option 3"],
            width="stretch",
            key="pills_stretch",
        )

        # Fixed pixel width
        st.pills(
            "Width=300px",
            options=["Option 1", "Option 2", "Option 3"],
            width=300,
            key="pills_300px",
        )

    st.write("Pills with different scale values (width='stretch'):")
    with st.container(border=True, direction="vertical", gap="large"):
        # Scale 1 (default)
        st.pills(
            "Scale=1",
            options=["Option 1", "Option 2"],
            scale=1,
            width="stretch",
            key="pills_scale1",
        )

        # Scale 2
        st.pills(
            "Scale=2",
            options=["Option 1", "Option 2"],
            scale=2,
            width="stretch",
            key="pills_scale2",
        )

        # Scale 3
        st.pills(
            "Scale=3",
            options=["Option 1", "Option 2"],
            scale=3,
            width="stretch",
            key="pills_scale3",
        )

st.subheader("Segmented Control Widget Tests")
st.write("Compare different width options for segmented control widgets:")

with st.container(border=True, direction="vertical", gap="large"):
    st.write("Single-select segmented control with different width options:")
    with st.container(border=True, direction="horizontal", gap="large"):
        # Content width (default)
        st.segmented_control(
            "Default width='content'",
            options=["Option 1", "Option 2", "Option 3"],
            key="segmented_default",
        )

        # Stretch width
        st.segmented_control(
            "Width='stretch'",
            options=["Option 1", "Option 2", "Option 3"],
            width="stretch",
            key="segmented_stretch",
        )

        # Fixed pixel width
        st.segmented_control(
            "Width=300px",
            options=["Option 1", "Option 2", "Option 3"],
            width=300,
            key="segmented_300px",
        )

    st.write("Segmented control with different scale values (width='stretch'):")
    with st.container(border=True, direction="horizontal", gap="large"):
        # Scale 1 (default)
        st.segmented_control(
            "Scale=1",
            options=["Option 1", "Option 2"],
            scale=1,
            width="stretch",
            key="segmented_scale1",
        )

        # Scale 2
        st.segmented_control(
            "Scale=2",
            options=["Option 1", "Option 2"],
            scale=2,
            width="stretch",
            key="segmented_scale2",
        )

        # Scale 3
        st.segmented_control(
            "Scale=3",
            options=["Option 1", "Option 2"],
            scale=3,
            width="stretch",
            key="segmented_scale3",
        )

# Update the interactive demo to include button group widgets
st.header("Interactive Demo with Button Group Widgets")
st.write("Try the same width and scale settings with a button group widget:")

st.write("Select a button group widget type:")
bg_widget_type = st.radio(
    "Widget type:",
    ["Feedback", "Pills", "Segmented Control"],
    horizontal=True,
    key="bg_widget_type_selector",
)

if bg_widget_type == "Feedback":
    with st.container(border=True, direction="horizontal", gap="large"):
        interactive_feedback = st.feedback(
            "thumbs",
            width=width_value,
            scale=scale_value,
            key="interactive_feedback",
        )
elif bg_widget_type == "Pills":
    with st.container(border=True, direction="horizontal", gap="large"):
        interactive_pills = st.pills(
            f"Pills (width='{width_value}', scale={scale_value})",
            options=["Option A", "Option B", "Option C"],
            width=width_value,
            scale=scale_value,
            key="interactive_pills",
        )
else:  # Segmented Control
    with st.container(border=True, direction="horizontal", gap="large"):
        interactive_segmented = st.segmented_control(
            f"Segmented (width='{width_value}', scale={scale_value})",
            options=["Option A", "Option B", "Option C"],
            width=width_value,
            scale=scale_value,
            key="interactive_segmented",
        )

# Section for Audio Input Test
st.header("Audio Input Tests")

st.subheader("Audio Input with Different Width Options")
st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Stretch width (default for audio_input)
    st.audio_input("Default width='stretch'", key="audio_default")

    # Fixed pixel width
    st.audio_input("Width=300px", width=300, key="audio_300px")

st.subheader("Audio Input with Different Scale Values")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.audio_input("Scale=1", scale=1, width="stretch", key="audio_scale1")

    # Scale 2
    st.audio_input("Scale=2", scale=2, width="stretch", key="audio_scale2")

    # Scale 3
    st.audio_input("Scale=3", scale=3, width="stretch", key="audio_scale3")

# Section for Camera Input Test
st.header("Camera Input Tests")

st.subheader("Camera Input with Different Width Options")
st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Stretch width (default for camera_input)
    st.camera_input("Default width='stretch'", key="camera_default")

    # Fixed pixel width
    st.camera_input("Width=300px", width=300, key="camera_300px")

st.subheader("Camera Input with Different Scale Values")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.camera_input("Scale=1", scale=1, width="stretch", key="camera_scale1")

    # Scale 2
    st.camera_input("Scale=2", scale=2, width="stretch", key="camera_scale2")

    # Scale 3
    st.camera_input("Scale=3", scale=3, width="stretch", key="camera_scale3")

# Section for File Uploader Test
st.header("File Uploader Tests")

st.subheader("File Uploader with Different Width Options")
st.write("Compare different width options:")
with st.container(border=True, direction="vertical", gap="large"):
    # Stretch width (default for file_uploader)
    st.file_uploader("Default width='stretch'", key="file_default")

    # Fixed pixel width
    st.file_uploader("Width=300px", width=300, key="file_300px")

    # Multiple files
    st.file_uploader(
        "Multiple files with width='stretch'",
        accept_multiple_files=True,
        width="stretch",
        key="file_multi_stretch",
    )

st.subheader("File Uploader with Different Scale Values")
st.write("All scaled elements use width='stretch':")
with st.container(border=True, direction="horizontal", gap="large"):
    # Scale 1 (default)
    st.file_uploader("Scale=1", scale=1, width="stretch", key="file_scale1")

    # Scale 2
    st.file_uploader("Scale=2", scale=2, width="stretch", key="file_scale2")

    # Scale 3
    st.file_uploader("Scale=3", scale=3, width="stretch", key="file_scale3")

st.subheader("File Uploader with Different Types")
st.write("Demonstrating width and scale with different file types:")
with st.container(border=True, direction="vertical", gap="large"):
    # Image files with stretched width
    st.file_uploader(
        "Image files (width='stretch')",
        type=["png", "jpg", "jpeg"],
        width="stretch",
        key="file_img_stretch",
    )

    # PDF files with fixed width
    st.file_uploader(
        "PDF files (width=300px)", type=["pdf"], width=300, key="file_pdf_300px"
    )

    # Text files with scaled size
    st.file_uploader(
        "Text files (scale=2, width='stretch')",
        type=["txt", "md"],
        scale=2,
        width="stretch",
        key="file_txt_scale2",
    )

# Update the interactive demo section to include file widgets
st.header("Interactive Demo")
st.write("Try different width and scale settings:")

# Width selection
width_option = st.radio(
    "Select width option:",
    options=["stretch", "300", "400", "500"],
    key="demo_width_option",
)

# Determine actual width
if width_option == "stretch":
    demo_width = "stretch"
else:
    demo_width = int(width_option)

# Scale selection
demo_scale = st.slider(
    "Select scale (1-5):", min_value=1, max_value=5, value=1, key="demo_scale"
)

# Ensure width is stretch if scale > 1
if demo_scale > 1 and demo_width != "stretch":
    st.warning("When scale > 1, width is automatically set to 'stretch'")
    demo_width = "stretch"

# Display demo widgets
st.subheader("Demo Widgets")
with st.container(border=True, direction="vertical", gap="large"):
    st.write(f"**Current Settings:** width='{demo_width}', scale={demo_scale}")

    # Standard widgets
    st.checkbox(
        "Demo Checkbox", width=demo_width, scale=demo_scale, key="demo_checkbox"
    )
    st.toggle("Demo Toggle", width=demo_width, scale=demo_scale, key="demo_toggle")
    st.radio(
        "Demo Radio",
        options=["A", "B", "C"],
        width=demo_width,
        scale=demo_scale,
        key="demo_radio",
    )

    # File widgets
    st.file_uploader(
        "Demo File Uploader", width=demo_width, scale=demo_scale, key="demo_file"
    )
    st.audio_input(
        "Demo Audio Input", width=demo_width, scale=demo_scale, key="demo_audio"
    )
    st.camera_input(
        "Demo Camera Input", width=demo_width, scale=demo_scale, key="demo_camera"
    )
