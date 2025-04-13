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

import altair as alt
import numpy as np
import pandas as pd

import streamlit as st

st.set_page_config(layout="wide")

st.title("Chart Width, Height, and Scale Test App")

st.markdown("""
This app demonstrates the new width, height, and scale parameters available for Streamlit charts.
All charts have `use_container_width=False` as required when using explicit width settings.

**Key concepts:**
- `width`: Can be an integer (pixels), "stretch" or "content"
- `height`: Can be an integer (pixels), "stretch" or "content"
- `scale`: Only used with `width="stretch"` to control how much space the chart takes up
""")


# Create sample data for our charts
@st.cache_data
def get_chart_data():
    np.random.seed(42)
    return pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])


chart_data = get_chart_data()

# LINE CHARTS SECTION
st.header("Line Charts")

with st.container(border=True):
    st.subheader("Fixed Width (400px)")
    st.line_chart(chart_data, width=400, height="content", use_container_width=False)

with st.container(border=True):
    st.subheader('Width="stretch" (fills container)')
    st.line_chart(
        chart_data, width="stretch", height="content", use_container_width=False
    )

with st.container(border=True):
    st.subheader('Width="content" (fits to content)')
    st.line_chart(
        chart_data, width="content", height="content", use_container_width=False
    )

# Demonstrate height options
with st.container(border=True):
    st.subheader("Fixed Height (200px)")
    st.line_chart(chart_data, width="stretch", height=200, use_container_width=False)

with st.container(border=True, height=600):
    st.subheader('Height="stretch" (fills container height)')
    st.markdown(
        "This container has a fixed height of 400px, and the chart stretches to fill it"
    )
    st.line_chart(
        chart_data, width="stretch", height="stretch", use_container_width=False
    )

# AREA CHARTS SECTION
st.header("Area Charts")

with st.container(border=True):
    st.subheader("Fixed Width (400px)")
    st.area_chart(chart_data, width=400, height="content", use_container_width=False)

with st.container(border=True):
    st.subheader('Width="stretch" (fills container)')
    st.area_chart(
        chart_data, width="stretch", height="content", use_container_width=False
    )

# BAR CHARTS SECTION
st.header("Bar Charts")

with st.container(border=True):
    st.subheader("Fixed Width (400px)")
    st.bar_chart(chart_data, width=400, height="content", use_container_width=False)

with st.container(border=True):
    st.subheader('Width="stretch" with Height=300px')
    st.bar_chart(chart_data, width="stretch", height=300, use_container_width=False)

# SCATTER CHARTS SECTION
st.header("Scatter Charts")

with st.container(border=True):
    st.subheader("Fixed Width (400px)")
    st.scatter_chart(chart_data, width=400, height="content", use_container_width=False)

with st.container(border=True):
    st.subheader('Width="content" (fits to content)')
    st.scatter_chart(
        chart_data, width="content", height="content", use_container_width=False
    )

# SCALE DEMONSTRATIONS (only with width="stretch")
st.header("Scale Parameter Demonstrations")
st.markdown(
    'The `scale` parameter can be used to adjust the relative size of charts when using `width="stretch"`'
)

with st.container(border=True):
    st.subheader("Line Chart with scale=0.5 (half size)")
    st.line_chart(
        chart_data,
        width="stretch",
        height="content",
        scale=0.5,
        use_container_width=False,
    )

with st.container(border=True):
    st.subheader("Line Chart with scale=1.0 (default)")
    st.line_chart(
        chart_data,
        width="stretch",
        height="content",
        scale=1.0,
        use_container_width=True,
    )

with st.container(border=True):
    st.subheader("Line Chart with scale=1.5 (50% larger)")
    st.line_chart(
        chart_data,
        width="stretch",
        height="content",
        scale=1.5,
        use_container_width=False,
    )

# MIXED CONTENT SECTION
st.header("Mixed Container with Chart and Text")

with st.container(border=True):
    st.subheader("Line Chart with Text Content")

    # We're not using columns as specified
    st.line_chart(
        chart_data,
        width="stretch",
        height=250,
        scale=0.6,  # Take up 60% of the container width
        use_container_width=False,
    )

    st.markdown("""
    This demonstrates how a chart with `width="stretch"` and `scale=0.6`
    will take up 60% of its container's width, leaving space for text to flow around it.

    The `height=250` parameter sets a fixed height in pixels.

    Using scale with width="stretch" allows you to control how much space the chart takes
    relative to the container size without using columns.
    """)

# COMPARISON SECTION
st.header("Direct Comparison")
st.markdown(
    'All charts below use the same settings: `width="stretch"`, `height=300`, `scale=0.8`'
)

with st.container(border=True):
    st.subheader("Line Chart")
    st.line_chart(
        chart_data, width="stretch", height=300, scale=0.8, use_container_width=False
    )

with st.container(border=True):
    st.subheader("Area Chart")
    st.area_chart(
        chart_data, width="stretch", height=300, scale=0.8, use_container_width=False
    )

with st.container(border=True):
    st.subheader("Bar Chart")
    st.bar_chart(
        chart_data, width="stretch", height=300, scale=0.8, use_container_width=False
    )

with st.container(border=True):
    st.subheader("Scatter Chart")
    st.scatter_chart(
        chart_data, width="stretch", height=300, scale=0.8, use_container_width=False
    )

# Replace the Horizontal Layout with Multiple Charts section
st.header("Horizontal Layout with Multiple Charts")
st.markdown("""
Demonstrating how to create a horizontal layout with multiple charts
using different scale values to control their relative sizes.
""")

# Create a horizontal container for the three charts
with st.container(border=True):
    st.subheader("Three Charts with Different Scale Values")

    # Use native horizontal container instead of CSS
    with st.container(direction="horizontal", wrap=False):
        # First chart - small scale (25%)
        st.line_chart(
            chart_data,
            width="stretch",
            height=250,
            scale=1,
            use_container_width=False,
        )

        # Second chart - medium scale (50%)
        st.area_chart(
            chart_data,
            width="stretch",
            height=250,
            scale=2,
            use_container_width=False,
        )


# Second horizontal example
with st.container(border=True):
    st.subheader("Another Example: Two Charts with Scale Ratio 1:2")

    # Use native horizontal container
    with st.container(direction="horizontal"):
        # First chart - 1/3 of space
        st.scatter_chart(
            chart_data,
            width="stretch",
            height=300,
            scale=0.3,
            use_container_width=False,
        )

        # Second chart - 2/3 of space
        st.line_chart(
            chart_data,
            width="stretch",
            height=300,
            scale=0.6,
            use_container_width=False,
        )

    st.caption(
        "Note: These charts are arranged in a ratio of approximately 1:2 using scale values of 0.3 and 0.6"
    )

# Replace the Dashboard-like Layout section
st.header("Dashboard-like Layout")
st.markdown("""
This example demonstrates how to create a more complex dashboard-like layout
with multiple charts of different types and sizes.
""")


# Create a function for generating a more interesting sample dataset
@st.cache_data
def get_dashboard_data():
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=30, freq="D")
    data = {
        "date": dates,
        "sales": np.random.randint(100, 500, size=30).cumsum(),
        "visitors": np.random.randint(500, 1500, size=30),
        "conversion": np.random.uniform(1, 5, size=30),
        "category": np.random.choice(["A", "B", "C", "D"], size=30),
    }
    return pd.DataFrame(data)


dashboard_data = get_dashboard_data()

with st.container(border=True):
    st.subheader("Sales Dashboard Example")

    # Header row with KPIs in a horizontal container
    with st.container(direction="horizontal"):
        # KPI 1
        with st.container():
            st.markdown("### Total Sales")
            st.markdown(f"## ${dashboard_data['sales'].iloc[-1]:,.0f}")

        # KPI 2
        with st.container():
            st.markdown("### Avg. Visitors/Day")
            st.markdown(f"## {dashboard_data['visitors'].mean():.0f}")

        # KPI 3
        with st.container():
            st.markdown("### Avg. Conversion")
            st.markdown(f"## {dashboard_data['conversion'].mean():.1f}%")

    # Main dashboard section with charts
    with st.container(direction="horizontal"):
        # Main chart area (70%)
        with st.container():
            st.markdown("**Sales Trend**")
            sales_chart = (
                alt.Chart(dashboard_data)
                .mark_area(opacity=0.6, color="#4682b4")
                .encode(
                    x=alt.X("date:T", title="Date"),
                    y=alt.Y("sales:Q", title="Cumulative Sales ($)"),
                )
                .properties(height=300)
            )

            st.altair_chart(
                sales_chart,
                width="stretch",
                height="content",
                scale=0.7,
                use_container_width=False,
            )

        # Side charts area (30%)
        with st.container():
            # First side chart
            st.markdown("**Daily Visitors**")
            visitors_chart = (
                alt.Chart(dashboard_data)
                .mark_bar(color="#82b446")
                .encode(
                    x=alt.X("date:T", title="Date"),
                    y=alt.Y("visitors:Q", title="Visitors"),
                )
                .properties(height=140)
            )

            st.altair_chart(
                visitors_chart,
                width="stretch",
                height="content",
                scale=0.3,
                use_container_width=False,
            )

            # Second side chart
            st.markdown("**Conversion by Category**")
            category_chart = (
                alt.Chart(dashboard_data)
                .mark_circle(opacity=0.7)
                .encode(
                    x=alt.X("category:N", title="Category"),
                    y=alt.Y("conversion:Q", title="Conversion (%)"),
                    size=alt.Size("visitors:Q", legend=None),
                    color=alt.Color("category:N", legend=None),
                )
                .properties(height=140)
            )

            st.altair_chart(
                category_chart,
                width="stretch",
                height="content",
                scale=0.3,
                use_container_width=False,
            )

    st.caption(
        "This example shows how to create a dashboard layout with a main chart (scale=0.7) and side charts (scale=0.3)"
    )

# Add a new section for dataframes before the final st.info message
st.header("Dataframes in Containers")
st.markdown("""
This section demonstrates how to incorporate dataframes in containers alongside charts.
""")


# Create a sample dataframe with more interesting data
@st.cache_data
def get_sales_data():
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    data = {
        "Date": dates,
        "Sales": np.random.randint(100, 500, size=10),
        "Customers": np.random.randint(50, 200, size=10),
        "Avg Order": np.random.uniform(20, 50, size=10).round(2),
        "Region": np.random.choice(["North", "South", "East", "West"], size=10),
    }
    return pd.DataFrame(data)


sales_data = get_sales_data()

# Simple dataframe in a container
with st.container(border=True):
    st.subheader("Basic Dataframe in Container")
    st.dataframe(sales_data)

# Dataframe with styling
with st.container(border=True):
    st.subheader("Styled Dataframe")
    # Create a styled dataframe
    styled_df = sales_data.style.highlight_max(
        axis=0, color="lightgreen"
    ).highlight_min(axis=0, color="#FFB6C1")
    st.dataframe(styled_df, height=250)

# Horizontal layout with dataframe and chart
with st.container(border=True):
    st.subheader("Dataframe and Chart Side by Side")

    with st.container(direction="horizontal"):
        # Left side - Dataframe
        with st.container():
            st.markdown("**Sales Data Table**")
            st.dataframe(sales_data, height=300)

        # Right side - Chart
        with st.container():
            st.markdown("**Sales Visualization**")

            # Create a chart based on the dataframe data
            sales_viz = (
                alt.Chart(sales_data)
                .mark_bar()
                .encode(
                    x=alt.X("Date:T", title="Date"),
                    y=alt.Y("Sales:Q", title="Sales"),
                    color=alt.Color("Region:N", legend=None),
                    tooltip=["Date", "Sales", "Region", "Customers"],
                )
                .properties(height=300)
            )

            st.altair_chart(
                sales_viz,
                width="stretch",
                height="content",
                scale=0.7,
                use_container_width=False,
            )

# Advanced layout with dataframe and multiple visualizations
with st.container(border=True):
    st.subheader("Dashboard with Dataframe and Multiple Charts")

    # Top section - KPIs and dataframe
    with st.container(direction="horizontal"):
        # KPIs
        with st.container():
            total_sales = sales_data["Sales"].sum()
            total_customers = sales_data["Customers"].sum()
            avg_order_value = sales_data["Avg Order"].mean()

            st.markdown(f"**Total Sales:** ${total_sales:,}")
            st.markdown(f"**Total Customers:** {total_customers:,}")
            st.markdown(f"**Avg Order Value:** ${avg_order_value:.2f}")

        # Dataframe with the raw data
        with st.container():
            st.dataframe(sales_data, height=200)

    # Bottom section - Charts
    with st.container(direction="horizontal"):
        # Sales by region chart
        with st.container():
            region_chart = (
                alt.Chart(sales_data)
                .mark_arc()
                .encode(
                    theta=alt.Theta("sum(Sales):Q"),
                    color=alt.Color("Region:N"),
                    tooltip=["Region", "sum(Sales)"],
                )
                .properties(title="Sales by Region")
            )

            st.altair_chart(
                region_chart,
                width="stretch",
                height="content",
                scale=0.4,
                use_container_width=False,
            )

        # Sales trend chart
        with st.container():
            trend_chart = (
                alt.Chart(sales_data)
                .mark_line()
                .encode(x="Date:T", y="Sales:Q", tooltip=["Date", "Sales"])
                .properties(title="Sales Trend")
            )

            st.altair_chart(
                trend_chart,
                width="stretch",
                height="content",
                scale=0.6,
                use_container_width=False,
            )

    st.caption(
        "This example shows a complete dashboard with a dataframe and multiple charts arranged in horizontal containers"
    )

st.info("""
**Chart Layout Rules:**
1. Use `use_container_width=False` when setting width explicitly
2. Only use `scale` when `width="stretch"`
3. Default height is "content" which auto-sizes to fit the chart content
""")
