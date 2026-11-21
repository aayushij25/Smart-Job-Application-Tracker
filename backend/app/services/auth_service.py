from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories import user_repository

class EmailAlreadyRegistered(Exception):
    pass

def register_user(db: Session, email: str, password: str):
    email = email.lower()
    if user_repository.get_by_email(db, email):
        raise EmailAlreadyRegistered()
    return user_repository.create(db, email, hash_password(password))

class InvalidCredentials(Exception):
    pass

def authenticate(db: Session, email: str, password: str) -> str:
    user = user_repository.get_by_email(db, email.lower())
    if not user or not verify_password(password, user.password_hash):
        raise InvalidCredentials()
    return create_access_token(user.id)