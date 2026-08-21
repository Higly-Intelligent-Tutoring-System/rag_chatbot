import uuid

import streamlit as st
import time
import requests

from ui.config import ui_settings

# Page Configuration
st.set_page_config(
    page_title="STUDY Chatbot",
    page_icon="🎓",
    layout="wide"
)

# Load CSS from file
with open("src/ui/styles/main.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# University mapping with emoji flags
UNIVERSITIES = {
    "🇮🇹 Unicam": "ita",
    "🇸🇮 Maribor": "slo",
    "🇪🇸 Valladolid": "esp",
    "🇷🇴 Bucarest": "rou",
    "🇱🇹 Vilnius": "ltu",
}

# Ensure a random thread_id by default
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Initialize selected university
if "selected_university" not in st.session_state:
    st.session_state.selected_university = list(UNIVERSITIES.keys())[0]

# Header Section
with st.container():
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="header-title">🎓 HITS Chatbot</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-subtitle">
    Your academic tutoring assistant
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-caption">
    📅 Organize your study plan • 💡 Overcome learning difficulties • 🏛️ Navigate university services
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Controls Section
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1.5, 0.3], gap="small")

with col1:
    selected_university = st.selectbox(
        "Select university:",
        options=list(UNIVERSITIES.keys()),
        index=list(UNIVERSITIES.keys()).index(st.session_state.selected_university),
        label_visibility="collapsed"
    )

# Check if selection changed and clear conversation if it did
if selected_university != st.session_state.selected_university:
    st.session_state.selected_university = selected_university
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Let's get started on your study journey. What do you need help with? 👇"}]
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()

with col2:
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! Let's get started on your study journey. What do you need help with? 👇"}]
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Define custom avatars
avatars = {
    "assistant": "🎓",
    "user": "🧑‍🎓"
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Let's get started on your study journey. What do you need help with? 👇"}]

# Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get the university identifier for the API call
        university_id = UNIVERSITIES[st.session_state.selected_university]
        
        try:
            resp = requests.post(
                url=f"{ui_settings.api_url(university=university_id)}/chat",
                json={
                    "message": prompt,
                    "thread_id": st.session_state.thread_id,
                    "university": university_id,
                },
                timeout=60,
            )
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            assistant_response = ""
        else:
            if resp.status_code == 200:
                try:
                    assistant_response = resp.json().get("response", "")
                except ValueError:
                    st.error("Failed to decode JSON from API response.")
                    assistant_response = ""
            else:
                st.error(f"API error {resp.status_code}: {resp.text}")
                assistant_response = ""

        # Simulate stream of response with milliseconds delay
        parts = assistant_response.split("\n")
        full_response = ""
        for part in parts:
            full_response += part + "\n"
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.03)

        message_placeholder.markdown(assistant_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
