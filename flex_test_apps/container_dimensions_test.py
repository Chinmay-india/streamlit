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

import numpy as np

import streamlit as st

# Title and description
st.title("Container Dimensions Test App")
st.write("""
This app demonstrates different combinations of width and height settings for containers.
Try different settings to see how containers adjust their dimensions.
""")

# Interactive controls
st.header("Interactive Demo")

with st.expander("Container Settings", expanded=True):
    # Height options
    height_option = st.radio("Height", options=["content", "stretch", "fixed"], index=0)

    if height_option == "fixed":
        height_value = st.slider("Height (pixels)", 50, 500, 200)
    else:
        height_value = height_option

    # Width options
    width_option = st.radio("Width", options=["stretch", "content", "fixed"], index=0)

    if width_option == "fixed":
        width_value = st.slider("Width (pixels)", 50, 1000, 300)
    else:
        width_value = width_option

    border = st.checkbox("Show border", value=True)
    content_amount = st.slider("Content amount", 1, 20, 5)


# Function to create demo content
def create_content(container, amount):
    container.write("### Container Content")
    container.write(f"This container has {'auto' if amount > 10 else amount} items.")

    # Add varying amounts of content
    if amount <= 10:
        for i in range(amount):
            container.write(f"Item {i + 1}")
    else:
        # For large content, add a chart and long text
        container.write("Here's a chart:")
        chart_data = np.random.randn(20, 3)
        container.line_chart(chart_data)

        container.write("And some long text:")
        container.markdown("Lorem ipsum dolor sit amet. " * 50)


# Main demonstration
st.header("Container Demo")

# Apply settings based on user selection
if height_option == "fixed":
    container_height = height_value
else:
    container_height = height_value  # "content" or "stretch"

if width_option == "fixed":
    container_width = width_value
else:
    container_width = width_option  # "stretch" or "content"

st.write(
    f"Container settings: width=`{container_width}`, height=`{container_height}`, border=`{border}`"
)

# Create the demonstration container
demo_container = st.container(
    height=container_height, width=container_width, border=border
)

create_content(demo_container, content_amount)

# Show examples vertically
st.header("Container Examples")

# Width options with content height
st.subheader("Width = 'stretch'")
st.write("This container expands to fill the available horizontal space.")
create_content(st.container(width="stretch", height="content", border=True), 3)

st.subheader("Width = 'content'")
st.write("This container adjusts to fit its content horizontally.")
create_content(st.container(width="content", height="content", border=True), 3)

st.subheader("Width = 200 (pixels)")
st.write("This container has a fixed width of 200 pixels.")
create_content(st.container(width=200, height="content", border=True), 3)

# Height options with stretch width
st.subheader("Height = 'content'")
st.write("This container adjusts to fit its content vertically.")
create_content(st.container(height="content", width="stretch", border=True), 3)

st.subheader("Height = 'stretch'")
st.write("This container expands to fill the available vertical space.")
create_content(st.container(height="stretch", width="stretch", border=True), 3)

st.subheader("Height = 200 (pixels)")
st.write(
    "This container has a fixed height of 200 pixels and enables scrolling for overflow."
)
create_content(st.container(height=200, width="stretch", border=True), 3)

# Mixed combinations
st.subheader("Height = 'content' & Width = 'content'")
st.write("This container adjusts to fit its content in both dimensions.")
create_content(st.container(height="content", width="content", border=True), 2)

st.subheader("Height = 'stretch' & Width = 'stretch'")
st.write("This container expands to fill available space in both dimensions.")
create_content(st.container(height="stretch", width="stretch", border=True), 2)

st.subheader("Height = 150 (pixels) & Width = 150 (pixels)")
st.write("This container has fixed dimensions of 150 × 150 pixels.")
create_content(st.container(height=150, width=150, border=True), 2)

# Directional containers with scale examples
st.header("Direction and Scale Examples")

# Row example (horizontal)
st.subheader("Horizontal Direction (Row)")
st.write(
    "This example shows a row-like container (direction='horizontal') with inner containers using different scale values."
)

outer_row = st.container(
    direction="horizontal", height="content", width="stretch", border=True, gap="medium"
)

with outer_row:
    # Scale 1 container
    inner1 = outer_row.container(width="stretch", scale=1, border=True)
    inner1.write("### Scale = 1")
    inner1.write("This container takes 1 unit of space")

    # Scale 2 container
    inner2 = outer_row.container(width="stretch", scale=2, border=True)
    inner2.write("### Scale = 2")
    inner2.write("This container takes 2 units of space (twice as wide as scale=1)")

    # Scale 3 container
    inner3 = outer_row.container(width="stretch", scale=3, border=True)
    inner3.write("### Scale = 3")
    inner3.write(
        "This container takes 3 units of space (three times as wide as scale=1)"
    )

# Column example (vertical)
st.subheader("Vertical Direction (Column)")
st.write(
    "This example shows a column-like container (direction='vertical') with inner containers using different scale values."
)

outer_column = st.container(
    direction="vertical",
    height=1000,  # Fixed height to show scaling effect
    width="stretch",
    border=True,
    gap="medium",
)

with outer_column:
    # Scale 1 container
    inner1 = outer_column.container(
        width="stretch", height="stretch", scale=1, border=True
    )
    inner1.write("### Scale = 1")
    inner1.write("This container takes 1 unit of space")

    # Scale 2 container
    inner2 = outer_column.container(
        width="stretch", height="stretch", scale=2, border=True
    )
    inner2.write("### Scale = 2")
    inner2.write("This container takes 2 units of space (twice as tall as scale=1)")

    # Scale 3 container
    inner3 = outer_column.container(
        width="stretch", height="stretch", scale=3, border=True
    )
    inner3.write("### Scale = 3")
    inner3.write(
        "This container takes 3 units of space (three times as tall as scale=1)"
    )

# Complex nested layout example
st.header("Complex Nested Layout")
st.write(
    "This example shows a complex layout with multiple levels of nesting, directions, and scale values."
)

outer = st.container(
    height=600, width="stretch", border=True, direction="vertical", gap="medium"
)

with outer:
    # Top row
    top_row = outer.container(
        direction="horizontal",
        height="stretch",
        width="stretch",
        scale=2,
        border=True,
        gap="medium",
    )

    with top_row:
        # Left section in top row
        left = top_row.container(
            width="stretch", height="stretch", scale=1, border=True
        )
        left.write("Left (scale=1)")
        create_content(left, 2)

        # Right section in top row
        right = top_row.container(
            width="stretch", height="stretch", scale=2, border=True
        )
        right.write("Right (scale=2)")
        create_content(right, 2)

    # Bottom row
    bottom_row = outer.container(
        direction="horizontal",
        height="stretch",
        width="stretch",
        scale=1,
        border=True,
        gap="medium",
    )

    with bottom_row:
        # Create three equal sections
        for i in range(3):
            section = bottom_row.container(
                width="stretch", height="stretch", scale=1, border=True
            )
            section.write(f"Section {i + 1} (scale=1)")
            create_content(section, 1)

# Nested containers example
st.header("Nested Containers Example")
st.write(
    "This example shows a container with fixed height containing other containers."
)

outer_container = st.container(height=400, width="stretch", border=True)

with outer_container:
    outer_container.write("### Outer Container (height=400, width='stretch')")

    # First inner container
    outer_container.write("#### Inner Container 1 (height='stretch', width='stretch')")
    inner_container1 = outer_container.container(
        height="stretch", width="stretch", border=True
    )
    create_content(inner_container1, 3)

    # Second inner container
    outer_container.write("#### Inner Container 2 (height=200, width='content')")
    inner_container2 = outer_container.container(
        height=200, width="content", border=True
    )
    create_content(inner_container2, 5)

# Alternative to nested columns using horizontal containers
st.header("Alternative to Columns")
st.write(
    "This example shows how to create a column-like layout using containers with direction='horizontal'"
)

# Two-section layout
st.subheader("Two-section layout")
two_sections = st.container(
    direction="horizontal", width="stretch", border=True, gap="medium"
)

with two_sections:
    # Left section
    left_section = two_sections.container(width="stretch", scale=1, border=True)
    left_section.write("### Left Section")
    create_content(left_section, 2)

    # Right section
    right_section = two_sections.container(width="stretch", scale=1, border=True)
    right_section.write("### Right Section")
    create_content(right_section, 2)

# Three-section layout
st.subheader("Three-section layout")
three_sections = st.container(
    direction="horizontal", width="stretch", border=True, gap="medium"
)

with three_sections:
    # Create three equal sections
    for i in range(3):
        section = three_sections.container(width="stretch", scale=1, border=True)
        section.write(f"### Section {i + 1}")
        create_content(section, 1)

# Tips and notes
st.header("Notes")
st.info("""
- **content**: Adjusts to fit the content
- **stretch**: Expands to fill available space
- **fixed pixel value**: Uses a specific size and enables scrolling for overflow

Best practices:
- Use 'content' height for most containers
- Use 'stretch' width for responsive layouts
- Use fixed heights sparingly, especially on mobile devices
- When using fixed height, consider adding a border for visual clarity
""")
