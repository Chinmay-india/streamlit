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
import pandas as pd

import streamlit as st

cells = st.grid(outer_border=True, inner_borders=True, num_cells=6, num_cols=2)

cells[0][0].write("Hello")
cells[0][1].write("World")
cells[1][0].write("Hello")
cells[1][1].write("World")
cells[2][0].write("Hello")
cells[2][1].write("World")

cells_two = st.grid(outer_border=True, inner_borders=True, num_cells=4, num_cols=2)

with cells_two[0][0]:
    st.write("Hello")
    st.write("Hello")
with cells_two[0][1]:
    st.write("World")
    st.write("World")
with cells_two[1][0]:
    st.write("Hello")
    st.write("Hello")
with cells_two[1][1]:
    st.write("World")
    st.write("World")

st.header("Grid with Images")
# Create a 2x2 grid with images
image_grid = st.grid(num_cells=4, num_cols=2, outer_border=True)

# Add different images to each cell
image_grid[0][0].image("https://static.streamlit.io/examples/cat.jpg", caption="Cat")
image_grid[0][1].image("https://static.streamlit.io/examples/dog.jpg", caption="Dog")
image_grid[1][0].image("https://static.streamlit.io/examples/owl.jpg", caption="Owl")
image_grid[1][1].image(
    "https://static.streamlit.io/examples/balloon.jpg", caption="Balloon"
)

st.header("Grid with Charts")
# Create a 2x2 grid with different chart types
chart_grid = st.grid(num_cells=4, num_cols=2, outer_border=True, inner_borders=True)

# Sample data
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
bar_data = pd.DataFrame({"Category": ["A", "B", "C", "D"], "Values": [3, 7, 2, 9]})

# Add charts to each cell
with chart_grid[0][0]:
    st.subheader("Line Chart")
    st.line_chart(chart_data)

with chart_grid[0][1]:
    st.subheader("Bar Chart")
    st.bar_chart(bar_data.set_index("Category"))

with chart_grid[1][0]:
    st.subheader("Area Chart")
    st.area_chart(chart_data)

with chart_grid[1][1]:
    st.subheader("Scatter Chart")
    st.scatter_chart(chart_data)

st.header("Large Mixed Grid (6x4)")
st.caption("Combining charts, metrics, and images in a larger grid")

# Create a 6x4 grid (24 cells)
large_grid = st.grid(num_cells=24, num_cols=4, outer_border=True, inner_borders=True)

# Sample data for various charts
time_data = pd.DataFrame(
    {
        "Date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
        "Value": np.cumsum(np.random.randn(30) * 100) + 1000,
    }
).set_index("Date")

categorical_data = pd.DataFrame(
    {
        "Category": ["Product A", "Product B", "Product C", "Product D", "Product E"],
        "Sales": [120, 87, 203, 145, 95],
        "Profit": [35, 21, 47, 32, 18],
    }
)

# Row 1: Charts
with large_grid[0][0]:
    st.subheader("Revenue Trend")
    st.line_chart(time_data)

with large_grid[0][1]:
    st.subheader("Sales by Product")
    st.bar_chart(categorical_data.set_index("Category")["Sales"])

with large_grid[0][2]:
    st.subheader("Profit by Product")
    st.bar_chart(categorical_data.set_index("Category")["Profit"])

with large_grid[0][3]:
    st.subheader("Temperature Map")
    # Create a simple heatmap-like visualization
    heatmap_data = pd.DataFrame(
        np.random.randn(10, 10) * 8 + 22,  # Random temperatures around 22°C
        columns=[f"Hour {i}" for i in range(10)],
        index=[f"Day {i}" for i in range(10)],
    )
    st.dataframe(
        heatmap_data.style.background_gradient(cmap="viridis"),
        use_container_width=True,
    )

# Row 2: Metrics
with large_grid[1][0]:
    st.metric("Revenue", "$12,345", "+8.5%")

with large_grid[1][1]:
    st.metric("Users", "1,234", "+12.3%")

with large_grid[1][2]:
    st.metric("Conversion", "4.6%", "-0.2%")

with large_grid[1][3]:
    st.metric("Avg. Session", "2m 34s", "+0.5%")

# Row 3: Images
large_grid[2][0].image("https://static.streamlit.io/examples/cat.jpg", caption="Cats")
large_grid[2][1].image("https://static.streamlit.io/examples/dog.jpg", caption="Dogs")
large_grid[2][2].image("https://static.streamlit.io/examples/owl.jpg", caption="Owls")
large_grid[2][3].image(
    "https://static.streamlit.io/examples/balloon.jpg", caption="Balloons"
)

# Row 4: Mixed Content
with large_grid[3][0]:
    st.subheader("Customer Rating")
    st.slider("Rate our service", 0, 5, 4)

with large_grid[3][1]:
    st.subheader("Product Category")
    st.selectbox("Choose category", ["Electronics", "Clothing", "Food", "Books"])

with large_grid[3][2]:
    st.subheader("Quick Poll")
    st.radio("Favorite color", ["Red", "Green", "Blue", "Purple"])

with large_grid[3][3]:
    st.subheader("Subscribe")
    st.checkbox("Receive newsletter")
    st.text_input("Email address")

# Row 5: More Charts
with large_grid[4][0]:
    st.subheader("Distribution")
    chart_data_2 = pd.DataFrame(
        np.random.normal(0, 1, size=100), columns=["Normal Distribution"]
    )
    st.area_chart(chart_data_2)

with large_grid[4][1]:
    st.subheader("Scatter Plot")
    scatter_data = pd.DataFrame(
        np.random.randn(50, 2) / [3, 3] + [0, 0], columns=["X", "Y"]
    )
    st.scatter_chart(scatter_data)

with large_grid[4][2]:
    st.subheader("Donut Chart Data")
    donut_data = pd.DataFrame(
        {"Category": ["A", "B", "C", "D"], "Value": [25, 30, 20, 25]}
    )
    st.dataframe(donut_data)

with large_grid[4][3]:
    st.subheader("Progress")
    st.progress(0.75)
    st.caption("75% Complete")

# Row 6: More Metrics and Text
with large_grid[5][0]:
    st.markdown("### Project Status")
    st.markdown("⭐ On track")
    st.markdown("⏰ Due: Dec 31, 2023")

with large_grid[5][1]:
    st.markdown("### Team Members")
    st.markdown("- Alice (Lead)")
    st.markdown("- Bob (Developer)")
    st.markdown("- Charlie (Designer)")

with large_grid[5][2]:
    st.subheader("Budget")
    st.metric("Q4 Budget", "$84,500", "-2.5%")
    st.caption("Below last quarter")

with large_grid[5][3]:
    st.subheader("Notes")
    st.text_area("Add notes", "Team meeting on Thursday")

st.header("Metrics Dashboard (4x4 Grid)")
st.caption("A grid containing only metric elements")

# Create a 4x6 grid (24 cells)
metrics_grid = st.grid(num_cells=16, num_cols=4, outer_border=True, inner_borders=True)

# Sample data for financial metrics
financial_metrics = [
    {"label": "Revenue", "value": "$82.5M", "delta": "+12.4%"},
    {"label": "Profit", "value": "$21.3M", "delta": "+7.8%"},
    {"label": "Expenses", "value": "$61.2M", "delta": "+14.1%"},
    {"label": "Cash Flow", "value": "$14.7M", "delta": "-3.2%"},
    {"label": "Assets", "value": "$341M", "delta": "+5.3%"},
    {"label": "Liabilities", "value": "$125M", "delta": "-2.1%"},
    {"label": "EBITDA", "value": "$34.1M", "delta": "+9.2%"},
    {"label": "Net Margin", "value": "25.8%", "delta": "+1.3%"},
    {"label": "ROI", "value": "18.2%", "delta": "+0.7%"},
    {"label": "ROE", "value": "22.4%", "delta": "+2.1%"},
    {"label": "Debt Ratio", "value": "0.37", "delta": "-0.04"},
    {"label": "EPS", "value": "$2.45", "delta": "+0.32"},
    {"label": "Customers", "value": "12,847", "delta": "+842"},
    {"label": "Retention", "value": "93.2%", "delta": "+1.4%"},
    {"label": "Churn", "value": "6.8%", "delta": "-1.4%"},
    {"label": "CAC", "value": "$482", "delta": "-$27"},
    {"label": "LTV", "value": "$4,128", "delta": "+$215"},
    {"label": "Conversion", "value": "3.7%", "delta": "+0.4%"},
    {"label": "Orders", "value": "8,421", "delta": "+12.7%"},
    {"label": "AOV", "value": "$103.52", "delta": "+$7.42"},
    {"label": "Units/Order", "value": "2.8", "delta": "+0.3"},
    {"label": "Stock Level", "value": "84%", "delta": "-3%"},
    {"label": "Delivery Time", "value": "2.4 days", "delta": "-0.3 days"},
    {"label": "Returns", "value": "4.2%", "delta": "-0.7%"},
]

# Add metrics to the grid
for row in range(4):
    for col in range(4):
        index = row * 6 + col
        metric = financial_metrics[index]
        with metrics_grid[row][col]:
            st.metric(
                label=metric["label"], value=metric["value"], delta=metric["delta"]
            )
