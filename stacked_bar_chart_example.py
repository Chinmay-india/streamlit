import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("Plotly Stacked Bar Chart Example")

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

# Create stacked bar chart
st.subheader("Stacked Bar Chart (should be stacked, not side-by-side)")

# Create plotly figure
fig = go.Figure()

for category in categories:
    category_data = df[df['category'] == category]
    fig.add_trace(
        go.Bar(
            x=category_data['week_label'],
            y=category_data['value'],
            name=category
        )
    )

# Update layout with explicit stack mode
fig.update_layout(
    xaxis_title='Week',
    yaxis_title='Number of Cases',
    height=400,
    margin=dict(t=10, b=20, l=20, r=20),
    barmode='stack',  # Explicitly set stack mode
    xaxis=dict(
        type='category',
        categoryorder='array',
        categoryarray=sorted(df['week_label'].unique())
    ),
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(247,247,247,0.5)'
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Display the version information
st.subheader("Debug Information")
st.write(f"Streamlit version: {st.__version__}")
st.write(f"Plotly version: {go.__version__}")

# Add a workaround section
st.subheader("Workaround with go.Figure(layout=...)")
st.write("Creating the figure with layout parameters in the constructor:")

# Create plotly figure with layout in constructor
fig2 = go.Figure(layout={
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
    fig2.add_trace(
        go.Bar(
            x=category_data['week_label'],
            y=category_data['value'],
            name=category
        )
    )

# Display the second chart
st.plotly_chart(fig2, use_container_width=True) 