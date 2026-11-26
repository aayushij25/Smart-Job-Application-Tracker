from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core import config
from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories import user_repository

bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
):
    user_id = decode_access_token(credentials.credentials)
    user = user_repository.get_by_id(db, user_id) if user_id else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user 

def require_ai_access(current_user=Depends(get_current_user)):
    allowed = config.AI_ALLOWED_EMAILS
    if "*" in allowed or current_user.email in allowed:
        return current_user
    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        "AI analysis is turned off on this public demo. See the README for a walkthrough.",
    )