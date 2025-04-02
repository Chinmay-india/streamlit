import streamlit as st

st.title("Streamlit Test App")

# Test toggle widget
toggle_state = st.toggle("Toggle me", value=False)
st.write(f"Toggle state: {toggle_state}")

# Test other basic widgets
st.text_input("Enter some text")
st.button("Click me")
st.checkbox("Check me")
st.slider("Select a value", 0, 100, 50) 