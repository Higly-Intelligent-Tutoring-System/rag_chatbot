# src/api/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from .config import api_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# --- TODO: Replace these with your real user lookup/verification ---
def verify_username_password(username: str, password: str) -> bool:
    # Example: single hard-coded user for demo. Replace with DB check.
    return username == "alice" and password == "wonderland"
# -------------------------------------------------------------

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(datetime.timezone.utc) + (expires_delta or timedelta(seconds=api_settings.ACCESS_TOKEN_EXPIRE_SECONDS))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, api_settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, api_settings.SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Dependency used by endpoints to protect routes.
def get_current_user_optional(token: str = Depends(oauth2_scheme)):
    # Called only when AUTH_ENABLED==True (see dependency selector below).
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

# Public dependency that toggles authentication on/off.
def require_auth_dep(token: str = Depends(oauth2_scheme)):
    if not api_settings.AUTH_ENABLED:
        return None  # auth disabled: no-op
    return get_current_user_optional(token)
