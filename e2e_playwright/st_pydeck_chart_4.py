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

from typing import Any, cast

import numpy as np
import pandas as pd
import pydeck as pdk

import streamlit as st

np.random.seed(12345)

random_scatter_sf = pd.DataFrame(
    cast("Any", np.random.randn(1000, 2) / [50, 50]) + [37.76, -122.4],
    columns=["lat", "lon"],
)

"""
## Chart with width and height set

Should show a "road"-style map with random data centered in SF, and small width and
height (200x250).
"""

st.pydeck_chart(
    pdk.Deck(
        map_style="road",
        initial_view_state=pdk.ViewState(
            latitude=37.7749295, longitude=-122.4194155, zoom=12, bearing=0, pitch=30
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=random_scatter_sf,
                get_position="[lon, lat]",
                get_fill_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    ),
    width=200,
    height=250,
    use_container_width=False,
)

""

"""
## Mapbox chart

You should see a "satellite"-style map served by Mapbox with random data centered in SF.
This test requires an API key to be set. See MAPBOX_API_KEY in our Github automation.
"""

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-v9",
        map_provider="mapbox",
        tooltip={"text": "Count: {count}"},
        initial_view_state=pdk.ViewState(
            latitude=37.7749295, longitude=-122.4194155, zoom=12, bearing=0, pitch=30
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=random_scatter_sf,
                get_position="[lon, lat]",
                get_fill_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
