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
from streamlit.delta_generator import DeltaGenerator
from streamlit.hello.utils import show_code


def chat_demo():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        avatar_type = st.radio(
            "Avatar type", ["Default", "Emoji", "Icon"], index=0, horizontal=True
        )

        if avatar_type == "Emoji":
            cols = st.columns(2)
            ai_avatar = cols[0].selectbox(
                "Select an AI avatar",
                ["🤖", "🦜", "🐶", "🐱"],
                index=0,
            )
            user_avatar = cols[1].selectbox(
                "Select a user avatar",
                ["👤", "👨‍💻", "👩‍💻", "👨‍🎤"],
                index=0,
            )
        elif avatar_type == "Icon":
            ai_avatar = st.segmented_control(
                "Select an AI avatar",
                [
                    ":material/robot:",
                    ":material/robot_2:",
                    ":material/smart_toy:",
                    ":material/computer:",
                    ":material/settings:",
                ],
                default=[":material/robot:"],
            )
            user_avatar = st.segmented_control(
                "Select a user avatar",
                [
                    ":material/person:",
                    ":material/raven:",
                    ":material/owl:",
                    ":material/sound_detection_dog_barking:",
                    ":material/pest_control_rodent:",
                ],
                default=[":material/person:"],
            )
        else:
            ai_avatar = None
            user_avatar = None
        AVATARS = {"user": user_avatar, "ai": ai_avatar}

        if st.button("Clear chat history"):
            st.session_state.chat_history = []

    # Create a fragment function to process the chat input within a fragment.
    # This allows Streamlit to append the user input and chat response to the
    # existing content without rerunning the whoe app.
    @st.fragment
    def process_chat(chat_container: DeltaGenerator) -> None:
        """Fragment function to prompt user for chat input and additively
        display the input and response in the external container (chat_container).
        """
        if user_input := st.chat_input("Type a message"):
            # Append the user input to the chat history and display it.
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            chat_container.chat_message("user", avatar=AVATARS["user"]).markdown(
                user_input
            )

            # Parrot the user's message backwards
            ai_response_generator = (x for x in user_input[::-1])
            # Stream the AI response to the app and add it to the chat history
            # when complete.
            with chat_container.chat_message("ai", avatar=AVATARS["ai"]):
                result = st.write_stream(ai_response_generator)
            st.session_state.chat_history.append({"role": "ai", "content": result})

    # Create a container to hold the chat messages.
    chat_container = st.container(height=600)

    # Render the chat history (during a full-script run).
    for message in st.session_state.chat_history:
        with chat_container.chat_message(
            message["role"], avatar=AVATARS[message["role"]]
        ):
            st.markdown(message["content"])

    # Use the fragment to process the user input and chat responses. This works
+    # incrementally to prevent rerunning the whole app with each new message.
    process_chat(chat_container)


# Use a container to keep the "Show code" checkbox at the top of the sidebar
# and the code block at the bottom of the main body.
body = st.container()
show_code(chat_demo)
with body:
    chat_demo()
