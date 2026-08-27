import uuid

import streamlit as st
import time
import requests

from ui.config import ui_settings

# TODO: Add login form to connect to the /token endpoint of the API
# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="STUDY Chatbot",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Load CSS
# -----------------------------------------------------------------------------
with open("src/ui/styles/main.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# University mapping with emoji flags
# -----------------------------------------------------------------------------
UNIVERSITIES = {
    "🌍 Generic": None,
    "🇮🇹 Unicam": "ita",
    "🇸🇮 Maribor": "slo",
    "🇪🇸 Valladolid": "esp",
    "🇷🇴 Bucarest": "rou",
    "🇱🇹 Vilnius": "ltu",
}

# -----------------------------------------------------------------------------
# Default state initialization
# -----------------------------------------------------------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "selected_university" not in st.session_state:
    st.session_state.selected_university = list(UNIVERSITIES.keys())[0]

TOKEN_URL = f"{ui_settings.api_url(university=UNIVERSITIES[st.session_state.selected_university])}/token"

# -----------------------------------------------------------------------------
# Authentication helpers
# -----------------------------------------------------------------------------

def is_authenticated() -> bool:
    """Return whether this Streamlit session currently has a JWT."""
    return bool(st.session_state.get("access_token"))


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate against FastAPI.

    OAuth2PasswordRequestForm expects form-encoded data, therefore we use
    data= rather than json=.
    """
    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "username": username,
                "password": password,
            },
            timeout=15,
        )
    except requests.RequestException as error:
        return False, f"Login request failed: {error}"

    if response.status_code == 200:
        try:
            token_data = response.json()
        except ValueError:
            return False, "The API returned an invalid JSON response."

        access_token = token_data.get("access_token")

        if not access_token:
            return False, "The API response did not contain an access token."

        # Store authentication only in this user's Streamlit session.
        st.session_state.access_token = access_token
        st.session_state.token_type = token_data.get("token_type", "bearer")
        st.session_state.expires_in = token_data.get("expires_in")

        return True, ""

    if response.status_code in (401, 403):
        return False, "Invalid username or password."

    return False, f"Login failed with API status {response.status_code}."


def logout() -> None:
    """Remove authentication data from the current Streamlit session."""
    st.session_state.pop("access_token", None)
    st.session_state.pop("token_type", None)
    st.session_state.pop("expires_in", None)


def authenticated_headers() -> dict[str, str]:
    """Build the Authorization header for protected API requests."""
    token_type = st.session_state.get("token_type", "bearer")
    access_token = st.session_state["access_token"]

    return {
        "Authorization": f"{token_type.capitalize()} {access_token}",
    }


def post_to_chatbot(
    *,
    university_id: str | None,
    prompt: str,
    thread_id: str,
) -> requests.Response:
    """Send a request to the chatbot API."""
    return requests.post(
        url=f"{ui_settings.api_url(university_id, ui_settings.API_ENCRYPTION)}/chat",
        headers=authenticated_headers() if ui_settings.API_ENCRYPTION else None,
        json={
            "message": prompt,
            "thread_id": thread_id,
            "university": university_id,
        },
        timeout=60,
    )

# -----------------------------------------------------------------------------
# Login gate
# -----------------------------------------------------------------------------
if not is_authenticated() and ui_settings.API_ENCRYPTION:
    st.title("🎓 HITS Chatbot")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            success, error_message = login(username, password)

            if success:
                st.rerun()
            else:
                st.error(error_message)

    st.stop()


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
            resp = post_to_chatbot(
                university_id=university_id,
                prompt=prompt,
                thread_id=st.session_state.thread_id,
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
