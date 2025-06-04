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

with st.container(width="content", border=True):
    import numpy as np
    import pandas as pd
    from st_aggrid import AgGrid  # type: ignore

    np.random.seed(0)
    df = pd.DataFrame(
        np.random.choice(100, size=(100, 4)), columns=["A", "B", "C", "D"]
    )
    AgGrid(df)

with st.container(width="content", border=True):
    import streamlit_antd_components as sac  # type: ignore

    btn = sac.buttons(
        items=["button1", "button2", "button3"],
        index=0,
        format_func="title",
        align="center",
        direction="horizontal",
        radius="lg",
        return_index=False,
    )
    st.write(f"The selected button label is: {btn}")
