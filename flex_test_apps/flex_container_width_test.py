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

st.title("Flex Container Width and Scale Test")
st.write("""
This app demonstrates different configurations of container widths,
button widths, and scale factors in horizontal containers.
""")

# Example 1: Horizontal container with fixed width and stretch-width contents
st.header("1. Horizontal Container with Fixed Width")
st.write(
    "The container below has a fixed width of 600px and contains buttons with stretch width."
)

fixed_width_container = st.container(
    width=600, direction="horizontal", border=True, gap="medium"
)

with fixed_width_container:
    # All buttons with stretch width
    fixed_width_container.button("Button 1", width="stretch")
    fixed_width_container.button("Button 2", width="stretch")
    fixed_width_container.button("Button 3", width="stretch")

st.write("Notice how all buttons share the available 600px width equally.")

# Example 2: Horizontal container with stretch width and fixed-width button
st.header("2. Horizontal Container with Stretch Width")
st.write(
    "The container below has stretch width (full page width) with a button of fixed width 400px."
)

stretch_width_container = st.container(
    width="stretch", direction="horizontal", border=True, gap="medium"
)

with stretch_width_container:
    # Button with fixed width
    stretch_width_container.button("Fixed Width Button (400px)", width=400)
    # Button with stretch
    stretch_width_container.button("Stretch Width Button", width="stretch")

st.write(
    "Notice how the fixed-width button maintains 400px width while the stretch button fills the rest."
)

# Example 3: Horizontal container with mixed widths and scales
st.header("3. Horizontal Container with Mixed Widths and Scales")
st.write("""
The container below has stretch width containing:
- One button with fixed width (200px)
- Two buttons with stretch width and scale=2
""")

mixed_container = st.container(
    width="stretch", direction="horizontal", border=True, gap="medium"
)

with mixed_container:
    # Fixed width button
    mixed_container.button("Fixed Width (200px)", width=200)
    # Two stretch buttons with scale=2
    mixed_container.button("Stretch + Scale 2", width="stretch", scale=2)
    mixed_container.button("Stretch + Scale 2 2", width="stretch", scale=2)

st.write("""
Observe how:
1. The fixed width button remains 200px
2. The two stretch buttons each get 2 units of the remaining space
3. Both stretch buttons have equal width since they have the same scale
""")

# Additional example - Different scales
st.header("4. Different Scale Values")
st.write("This container demonstrates different scale values (1, 2, and 3).")

scale_container = st.container(
    width="stretch", direction="horizontal", border=True, gap="medium"
)

with scale_container:
    # Three buttons with different scales
    scale_container.button("Scale 1", width="stretch", scale=1)
    scale_container.button("Scale 2", width="stretch", scale=2)
    scale_container.button("Scale 3", width="stretch", scale=3)

st.write("""
Notice the proportional widths:
- Scale 1: 1/6 of available space (1 unit out of 6 total units)
- Scale 2: 2/6 of available space (2 units out of 6 total units)
- Scale 3: 3/6 of available space (3 units out of 6 total units)
""")

# Checkbox to demonstrate dynamic resizing
st.header("5. Dynamic Layout Changes")
show_extra = st.checkbox(
    "Add extra button to see dynamic layout adjustment", value=False
)

dynamic_container = st.container(
    width="stretch", direction="horizontal", border=True, gap="medium"
)

with dynamic_container:
    dynamic_container.button("Fixed (100px)", width=100)
    dynamic_container.button("Stretch", width="stretch")
    dynamic_container.button("Stretch2", width="stretch")

    if show_extra:
        dynamic_container.button("Extra Button", width="stretch", scale=2)

st.write(
    "Check the box above to add an extra button and observe how the layout adjusts."
)

# Nested Container Example
st.header("6. Nested Containers")
st.write("""
This example demonstrates nested containers with:
- Outer container: Stretch width (full page width)
- Inner container: Fixed width (400px)
- Both containers have horizontal direction
""")

# Outer container with stretch width
outer_container = st.container(
    width="stretch", direction="horizontal", border=True, gap="medium", wrap=False
)

with outer_container:
    # A button in the outer container
    outer_container.button("Outer Container Button", width="stretch")

    # Inner container with fixed width
    inner_container = outer_container.container(
        width=400, direction="horizontal", border=True, gap="medium"
    )

    # Another button in the outer container
    outer_container.button("Another Outer Button", width="stretch")

# Add buttons to the inner container
with inner_container:
    inner_container.write("Inner Fixed-Width Container (400px)")
    inner_container.button("Inner Button 1", width="stretch")
    inner_container.button("Inner Button 2", width="stretch")

st.write("""
Observe how:
1. The outer container stretches to full page width
2. The inner container maintains a fixed width of 400px
3. Buttons in the inner container divide the 400px space
4. Buttons in the outer container (outside the inner container) divide the remaining space
""")

# Instructions
st.header("Notes")
st.info("""
- **width="stretch"** - Expands to fill available space
- **width=number** - Fixed pixel width
- **scale=number** - Proportion of available space (when width="stretch")

In horizontal containers:
1. Fixed-width elements maintain their size
2. Remaining space is distributed among stretch elements according to their scale values
3. If all stretch elements have the same scale, they get equal parts of the available space
""")
