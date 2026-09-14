import time

import requests
import streamlit as st

from ui.api_client import post_chat
from ui.auth import logout, require_login
from ui.components import render_controls, render_header
from ui.config import ui_settings
from ui.constants import AVATARS, UNIVERSITIES
from ui.state import initialize_session_state


# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="STUDY Chatbot",
    page_icon="🎓",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------

with open("src/ui/styles/main.css") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Authentication gate
# -----------------------------------------------------------------------------

require_login() if ui_settings.API_AUTH else ""


# -----------------------------------------------------------------------------
# Application initialization
# -----------------------------------------------------------------------------

initialize_session_state()


# -----------------------------------------------------------------------------
# Main UI
# -----------------------------------------------------------------------------

render_header()
render_controls()


# -----------------------------------------------------------------------------
# Chat history
# -----------------------------------------------------------------------------

st.markdown(
    '<div class="chat-container">',
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar=AVATARS[message["role"]],
    ):
        st.markdown(message["content"])

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Chat input
# -----------------------------------------------------------------------------

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        message_placeholder = st.empty()
        assistant_response = ""

        university_id = UNIVERSITIES[
            st.session_state.selected_university
        ]

        try:
            response = post_chat(
                university_id=university_id,
                prompt=prompt,
                thread_id=st.session_state.thread_id,
            )

        except requests.RequestException as error:
            st.error(f"Request failed: {error}")

        else:
            if response.status_code == 200:
                try:
                    assistant_response = response.json().get(
                        "response",
                        "",
                    )
                except ValueError:
                    st.error("Failed to decode JSON from API response.")

            elif response.status_code == 401:
                logout()
                st.warning("Your session has expired. Please log in again.")
                st.rerun()

            else:
                st.error(
                    f"API error {response.status_code}: {response.text}"
                )

        full_response = ""

        for part in assistant_response.split("\n"):
            full_response += part + "\n"
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.03)

        message_placeholder.markdown(assistant_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )
