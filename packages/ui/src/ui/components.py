import streamlit as st

from ui.auth import logout
from ui.constants import UNIVERSITIES
from ui.state import reset_chat
from ui.config import ui_settings


def render_header() -> None:
    with st.container():
        st.markdown(
            '<div class="header-container">',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            st.markdown(
                '<div class="header-title">🎓 HITS Chatbot</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="header-subtitle">
            Your academic tutoring assistant
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="header-caption">
            📅 Organize your study plan • 💡 Overcome learning difficulties •
            🏛️ Navigate university services
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


def render_controls() -> None:
    st.markdown(
        '<div class="controls-container">',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(
        [2, 1.5, 0.8],
        gap="small",
    )

    with col1:
        selected_university = st.selectbox(
            "Select university:",
            options=list(UNIVERSITIES.keys()),
            index=list(UNIVERSITIES.keys()).index(
                st.session_state.selected_university
            ),
            label_visibility="collapsed",
        )

    with col2:
        new_chat_clicked = st.button(
            "New Chat",
            use_container_width=True,
        )

    logout_clicked = False
    if ui_settings.API_AUTH:
        with col3:
            logout_clicked = st.button(
                "Logout",
                use_container_width=True,
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    if selected_university != st.session_state.selected_university:
        st.session_state.selected_university = selected_university
        reset_chat()
        st.rerun()

    if new_chat_clicked:
        reset_chat()
        st.rerun()

    if logout_clicked:
        logout()
        st.rerun()
