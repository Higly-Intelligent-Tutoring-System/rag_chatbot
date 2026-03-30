import streamlit as st
import time
import requests

# Page Configuration
st.set_page_config(
    page_title="STUDY Chatbot",
    page_icon="🎓",
    layout="centered"
)

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
        assistant_response = requests.post(
            url="http://0.0.0.0:8000/chat", 
            json={
                "message": prompt,
                "thread_id": "streamlit-test",
            }).json()["response"]
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})