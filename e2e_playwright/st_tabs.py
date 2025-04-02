import streamlit as st

# Initialize session state for tab selection
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Tab 1"  # Set default tab

tab_names = ["Tab 1", "Tab 2", "Tab 3"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        if tab_names[i] == "Tab 1":
            st.write("tab1")
            st.text_input("Text input")
        elif tab_names[i] == "Tab 2":
            st.write("tab2")
            st.number_input("Number input")
        elif tab_names[i] == "Tab 3":
            st.write("tab3")
            st.date_input("Date input")

with st.expander("Expander", expanded=True):
    many_tabs = st.tabs([f"Tab {i}" for i in range(25)])

sidebar_tab1, sidebar_tab2 = st.sidebar.tabs(["Foo", "Bar"])
sidebar_tab1.write("I am in the sidebar")
sidebar_tab2.write("I'm also in the sidebar")

st.tabs(
    [
        "**Bold Text**",
        "*Italicized*",
        "~Strikethough~",
        "`Code Block`",
        "🐶",
        ":joy:",
        ":material/check_circle: Icon",
    ]
)

tabs = st.tabs(["HTML Tab 1", "HTML Tab 2", "HTML Tab 3"])

for i, tab in enumerate(tabs):
    tab.html(f"<h1>Hello</h1><p>This is HTML tab {i + 1}</p>")
