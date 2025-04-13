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

st.set_page_config(layout="wide")

st.title("Metric Width and Scale Test App")

st.markdown("""
This app demonstrates the new width and scale parameters available for Streamlit metrics.

**Key concepts:**
- `width`: Can be an integer (pixels), "stretch" or "content"
- `scale`: Used with `width="stretch"` to control how much space the metric takes up in horizontal layouts
""")

# BASIC METRICS SECTION
st.header("Basic Metrics")

with st.container(border=True):
    st.subheader("Default Width (content)")
    st.metric(label="Default Width", value="42", delta="2")

with st.container(border=True):
    st.subheader("Fixed Width (400px)")
    st.metric(label="Fixed Width", value="42", delta="2", width=400)

with st.container(border=True):
    st.subheader('Width="stretch" (fills container)')
    st.metric(label="Stretch Width", value="42", delta="2", width="stretch")

# METRICS WITH BORDERS
st.header("Metrics with Borders")

with st.container(border=True):
    st.subheader("Metrics with borders and different widths")

    st.metric(
        label="Content Width", value="$1,234", delta="4%", border=True, width="content"
    )
    st.metric(
        label="Fixed Width (300px)", value="$1,234", delta="4%", border=True, width=300
    )
    st.metric(
        label="Stretch Width", value="$1,234", delta="4%", border=True, width="stretch"
    )

# HORIZONTAL LAYOUT SECTION
st.header("Metrics in Horizontal Layouts")

with st.container(border=True):
    st.subheader("Equal Scale in Horizontal Layout")

    with st.container(direction="horizontal"):
        st.metric(
            label="Metric 1",
            value="33%",
            delta="3%",
            border=True,
            width="stretch",
            scale=1.0,
        )
        st.metric(
            label="Metric 2",
            value="66%",
            delta="6%",
            border=True,
            width="stretch",
            scale=2.0,
        )
        st.metric(
            label="Metric 3",
            value="99%",
            delta="9%",
            border=True,
            width="stretch",
            scale=3.0,
        )

with st.container(border=True):
    st.subheader("Different Scales in Horizontal Layout")

    with st.container(direction="horizontal"):
        st.metric(
            label="Small Scale (0.2)",
            value="20%",
            delta="2%",
            border=True,
            width="stretch",
            scale=0.2,
        )
        st.metric(
            label="Medium Scale (0.3)",
            value="30%",
            delta="3%",
            border=True,
            width="stretch",
            scale=0.3,
        )
        st.metric(
            label="Large Scale (0.5)",
            value="50%",
            delta="5%",
            border=True,
            width="stretch",
            scale=0.5,
        )

# MIXED CONTENT SECTION
st.header("Mixed Content in Horizontal Layout")

with st.container(border=True):
    st.subheader("Metrics and Text in Horizontal Layout")

    with st.container(direction="horizontal"):
        with st.container(direction="vertical", scale=1, width="stretch"):
            # Metrics on the left
            st.metric(
                label="Revenue",
                value="$12,345",
                delta="+8.5%",
                delta_color="normal",
                border=True,
                width="stretch",
                scale=0.3,
            )
            st.metric(
                label="Users",
                value="1,024",
                delta="+12%",
                delta_color="normal",
                border=True,
                width="stretch",
                scale=0.3,
            )

        # Content in the middle
        st.markdown(
            """
        ### Performance Summary

        This section demonstrates how metrics can be mixed with other content
        in a horizontal layout. The metric on the left uses `scale=0.3` and the
        metric on the right uses `scale=0.3` as well.

        Using the `width="stretch"` and `scale` parameters allows you to control
        how much space each element takes up in the layout.
        """,
            scale=4,
            width="stretch",
        )

# DASHBOARD EXAMPLE
st.header("Dashboard Example")

# First row - KPIs
with st.container(border=True):
    with st.container(direction="horizontal"):
        st.metric(
            label="Revenue",
            value="$48,273",
            delta="+12.7%",
            border=True,
            width="stretch",
            scale=1.0,
        )
        st.metric(
            label="Users",
            value="3,489",
            delta="+8.1%",
            border=True,
            width="stretch",
            scale=1.0,
        )
        st.metric(
            label="Conversion",
            value="4.6%",
            delta="+0.4%",
            border=True,
            width="stretch",
            scale=1.0,
        )
        st.metric(
            label="Avg. Order",
            value="$52.32",
            delta="+2.1%",
            border=True,
            width="stretch",
            scale=1.0,
        )

# Second row - Main stats with mixed sizes
with st.container(border=True):
    with st.container(direction="horizontal"):
        # Smaller metric for less important data
        st.metric(
            label="Sessions",
            value="12,847",
            delta="+5.2%",
            border=True,
            width="stretch",
            scale=0.2,
        )

        # Medium sized metrics for secondary KPIs
        st.metric(
            label="Page Views",
            value="43,291",
            delta="+7.8%",
            border=True,
            width="stretch",
            scale=0.3,
        )

        # Largest metric for primary KPI
        st.metric(
            label="Customer Satisfaction",
            value="94%",
            delta="+2%",
            delta_color="normal",
            border=True,
            width="stretch",
            scale=0.5,
        )

st.info("""
**Metric Layout Rules:**
1. Use `width="content"` for metrics that should size to their content
2. Use `width="stretch"` with appropriate `scale` values for metrics in horizontal layouts
3. Add `border=True` to create metric cards with clear boundaries
""")
