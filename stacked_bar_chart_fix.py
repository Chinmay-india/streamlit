import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.title("Plotly Stacked Bar Chart Fixes")

# Create sample data
weeks = [f"Week {i}" for i in range(1, 11)]
categories = ["Category A", "Category B", "Category C"]

# Create a dataframe with random data
np.random.seed(42)
data = []
for week in weeks:
    for category in categories:
        value = np.random.randint(5, 30)
        data.append({"week_label": week, "category": category, "value": value})

df = pd.DataFrame(data)

# Display the dataframe
st.subheader("Sample Data")
st.dataframe(df)

# Fix 1: Using Plotly Express instead of Graph Objects
st.subheader("Fix 1: Using Plotly Express")
st.write("Plotly Express handles stacked bar charts more reliably:")

fig_px = px.bar(
    df,
    x="week_label",
    y="value",
    color="category",
    barmode="stack",
    labels={"week_label": "Week", "value": "Number of Cases"},
    height=400,
    category_orders={"week_label": sorted(df['week_label'].unique())}
)

fig_px.update_layout(
    margin=dict(t=10, b=20, l=20, r=20),
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(247,247,247,0.5)'
)

st.plotly_chart(fig_px, use_container_width=True)

# Fix 2: Graph Objects with layout in constructor
st.subheader("Fix 2: Graph Objects with layout in constructor")
st.write("Creating the figure with layout parameters in the constructor:")

fig_go = go.Figure(layout={
    'barmode': 'stack',
    'xaxis_title': 'Week',
    'yaxis_title': 'Number of Cases',
    'height': 400,
    'margin': dict(t=10, b=20, l=20, r=20),
    'xaxis': dict(
        type='category',
        categoryorder='array',
        categoryarray=sorted(df['week_label'].unique())
    ),
    'paper_bgcolor': 'rgba(255,255,255,0)',
    'plot_bgcolor': 'rgba(247,247,247,0.5)'
})

for category in categories:
    category_data = df[df['category'] == category]
    fig_go.add_trace(
        go.Bar(
            x=category_data['week_label'],
            y=category_data['value'],
            name=category
        )
    )

st.plotly_chart(fig_go, use_container_width=True)

# Fix 3: Using Plotly FigureWidget
st.subheader("Fix 3: Update Figure Factory")
st.write("Setting barmode when creating each trace:")

# Generate figure using Plotly's update method
fig_update = go.Figure()

for category in categories:
    category_data = df[df['category'] == category]
    fig_update.add_trace(
        go.Bar(
            x=category_data['week_label'],
            y=category_data['value'],
            name=category
        )
    )

# Set barmode through update method
fig_update.update(layout_barmode='stack')

# Add other layout updates
fig_update.update_layout(
    xaxis_title='Week',
    yaxis_title='Number of Cases',
    height=400,
    margin=dict(t=10, b=20, l=20, r=20),
    xaxis=dict(
        type='category',
        categoryorder='array',
        categoryarray=sorted(df['week_label'].unique())
    ),
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(247,247,247,0.5)'
)

st.plotly_chart(fig_update, use_container_width=True)

# Display the version information
st.subheader("Debug Information")
st.write(f"Streamlit version: {st.__version__}")
st.write(f"Plotly version: {go.__version__}")

# Add recommendations
st.subheader("Recommendations")
st.markdown("""
Based on the examples above, here are some recommendations for reliable stacked bar charts in Streamlit Cloud:

1. **Use Plotly Express** when possible (Fix 1)
2. **Set layout in the constructor** if using Graph Objects (Fix 2)
3. **Use the `update()` method** with `layout_barmode='stack'` (Fix 3)

These approaches appear to be more reliable when deployed to Streamlit Cloud.
""") 