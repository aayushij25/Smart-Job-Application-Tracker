from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.repositories import user_repository

class EmailAlreadyRegistered(Exception):
    pass

def register_user(db: Session, email: str, password: str):
    email = email.lower()
    if user_repository.get_by_email(db, email):
        raise EmailAlreadyRegistered()
    return user_repository.create(db, email, hash_password(password))
