import uuid

import streamlit as st

from ui.constants import UNIVERSITIES, WELCOME_MESSAGE


def initialize_session_state() -> None:
    """Initialize values required by the application."""

    st.session_state.setdefault(
        "thread_id",
        str(uuid.uuid4()),
    )

    st.session_state.setdefault(
        "selected_university",
        list(UNIVERSITIES.keys())[0],
    )

    st.session_state.setdefault(
        "messages",
        [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
            }
        ],
    )


def reset_chat() -> None:
    """Start a new conversation."""

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ]

    st.session_state.thread_id = str(uuid.uuid4())
