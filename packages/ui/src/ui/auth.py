import requests
import streamlit as st

from ui.config import ui_settings


def token_url() -> str:
    """Return the FastAPI token endpoint URL."""

    return f"{ui_settings.api_url(university=None)}/token"


def is_authenticated() -> bool:
    """Check whether this Streamlit session has an access token."""

    return bool(st.session_state.get("access_token"))


def authenticate(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate against FastAPI and store the returned JWT.

    OAuth2PasswordRequestForm expects form-encoded data, so the request
    uses data= rather than json=.
    """

    try:
        response = requests.post(
            token_url(),
            data={
                "username": username,
                "password": password,
            },
            timeout=15,
        )
    except requests.RequestException as error:
        return False, f"Login request failed: {error}"

    if response.status_code in (401, 403):
        return False, "Invalid username or password."

    if response.status_code != 200:
        return False, f"Login failed with status {response.status_code}."

    try:
        token_data = response.json()
    except ValueError:
        return False, "The API returned invalid JSON."

    access_token = token_data.get("access_token")

    if not access_token:
        return False, "The API response did not contain an access token."

    st.session_state.access_token = access_token
    st.session_state.token_type = token_data.get("token_type", "bearer")
    st.session_state.expires_in = token_data.get("expires_in")

    return True, ""


def logout() -> None:
    """Log out the current Streamlit session."""

    for key in (
        "access_token",
        "token_type",
        "expires_in",
    ):
        st.session_state.pop(key, None)


def get_auth_headers() -> dict[str, str]:
    """Return headers required by protected API endpoints."""

    access_token = st.session_state.get("access_token")

    if not access_token:
        raise RuntimeError("No access token is available.")

    return {
        "Authorization": f"Bearer {access_token}",
    }


def render_login() -> bool:
    """
    Render the login form.

    Returns True if the user is authenticated, otherwise False.
    """

    if is_authenticated():
        return True

    st.title("🎓 HITS Chatbot")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            success, error_message = authenticate(
                username=username,
                password=password,
            )

            if success:
                st.rerun()
            else:
                st.error(error_message)

    return False


def require_login() -> None:
    """
    Prevent the rest of the application from rendering until login succeeds.
    """

    if not render_login():
        st.stop()
