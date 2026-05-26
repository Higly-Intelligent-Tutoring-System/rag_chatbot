import uuid

import streamlit as st
import time
import requests

from ui.config import ui_settings

# Page Configuration
st.set_page_config(
    page_title="STUDY Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Ensure a random thread_id by default
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Place the New Conversation button below the header/introduction (left-aligned)
if st.button("New Conversation"):
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Let's get started on your study journey. What do you need help with? 👇"}]
    st.session_state.thread_id = str(uuid.uuid4())


# Branded Header & Introduction
st.title("🎓 HITS Chatbot")
st.markdown("""
**Welcome! I am your academic tutoring assistant.**  
I am here to help you:
*   📅 **Organize your study plan**
*   💡 **Overcome common learning difficulties**
*   🏛️ **Navigate university services and information**
""")
st.caption("How can I assist you with your academic journey today?")

# Define custom avatars
avatars = {
    "assistant": "🎓",
    "user": "🧑‍🎓"
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Let's get started on your study journey. What do you need help with? 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Present yourself and your functions"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            resp = requests.post(
                url=f"{ui_settings.api_url()}/chat",
                json={
                    "message": prompt,
                    "thread_id": st.session_state.thread_id,
                },
                timeout=60,
            )
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            assistant_response = ""
        else:
            if resp.status_code == 200:
                # decode JSON safely
                try:
                    assistant_response = resp.json().get("response", "")
                except ValueError:
                    st.error("Failed to decode JSON from API response.")
                    assistant_response = ""
            else:
                st.error(f"API error {resp.status_code}: {resp.text}")
                assistant_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})