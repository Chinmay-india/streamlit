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

from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code


def animation_demo() -> None:
    # Interactive Streamlit elements, like this segmented control and slider,
    # return their value. If you want to user a different value than you
    # display to your users, use a dictionary to store your display labels.
    DETAILS = {
        2: "Coarse",
        8: "Medium",
        14: "Fine",
        20: "Very fine",
    }
    iterations = st.sidebar.segmented_control(
        "Level of detail", DETAILS.keys(), default=8, format_func=DETAILS.get
    )
    separation = st.sidebar.slider("Separation", 0.7, 2.0, 0.7885)

    primary_color = st.get_option("theme.primaryColor")
    secondary_color = st.get_option("theme.secondaryBackgroundColor")
    cols = st.sidebar.columns(2)
    object_color = cols[0].color_picker(
        "Animation color", primary_color if primary_color else "#FF4B4B"
    )
    background_color = cols[1].color_picker(
        "Background color", secondary_color if secondary_color else "#FFFFFF"
    )

    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    frame_text = st.sidebar.empty()
    image_frame = st.empty()

    m, n, s = 960, 640, 400
    x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))

    for frame_num, a in enumerate(np.linspace(0.0, 4 * np.pi, 100)):
        # Here were setting value for these two elements.
        progress_bar.progress(frame_num)
        frame_text.text("Frame %i/100" % (frame_num + 1))

        # Performing some fractal wizardry.
        c = separation * np.exp(1j * a)
        Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
        C = np.full((n, m), c)
        M: Any = np.full((n, m), True, dtype=bool)
        N = np.zeros((n, m))

        for i in range(iterations):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
            N[M] = i

        # Parsing the user's color choices.
        red = int("0x" + object_color[1:3], 16)
        green = int("0x" + object_color[3:5], 16)
        blue = int("0x" + object_color[5:7], 16)
        bg_red = int("0x" + background_color[1:3], 16)
        bg_green = int("0x" + background_color[3:5], 16)
        bg_blue = int("0x" + background_color[5:7], 16)

        # Create a three-dimensional array for the RGB image
        monochrome_array = 1.0 - (N / N.max())
        rgb_array = np.zeros(
            (monochrome_array.shape[0], monochrome_array.shape[1], 3), dtype=np.uint8
        )

        # Apply the foreground and background colors
        rgb_array[:, :, 0] = (
            monochrome_array * bg_red + (1 - monochrome_array) * red
        ).astype(np.uint8)
        rgb_array[:, :, 1] = (
            monochrome_array * bg_green + (1 - monochrome_array) * green
        ).astype(np.uint8)
        rgb_array[:, :, 2] = (
            monochrome_array * bg_blue + (1 - monochrome_array) * blue
        ).astype(np.uint8)

        # Update the image placeholder by calling the image() function on it.
        image_frame.image(rgb_array, use_container_width=True)

    # We clear elements by calling empty on them.
    progress_bar.empty()
    frame_text.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rerun")


st.set_page_config(page_title="Animation demo", page_icon=":material/animation:")
st.title("Animation demo")
st.write(
    """
    This app shows how you can use Streamlit to build cool animations.
    It displays an animated fractal based on the Julia Set. Use the slider
    to tune different parameters.
    """
)

# Use a container to keep the "Show code" checkbox at the top of the sidebar
# and the code block at the bottom of the main body. This also lets the code
# block render before waiting for the animation to finish.
body = st.container()
show_code(animation_demo)
with body:
    animation_demo()
