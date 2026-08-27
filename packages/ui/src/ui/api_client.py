import requests

from ui.auth import get_auth_headers
from ui.config import ui_settings

def post_chat(
    *,
    university_id: str | None,
    prompt: str,
    thread_id: str,
) -> requests.Response:
    """Send a request to the chatbot API."""
    return requests.post(
        url=f"{ui_settings.api_url(university_id, ui_settings.API_ENCRYPTION)}/chat",
        headers=get_auth_headers() if ui_settings.API_ENCRYPTION else None,
        json={
            "message": prompt,
            "thread_id": thread_id,
            "university": university_id,
        },
        timeout=60,
    )