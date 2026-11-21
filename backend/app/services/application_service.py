from datetime import date
from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus as S
from app.repositories import application_repository as repo

ALLOWED_TRANSITIONS: dict[S, set[S]] = {
    S.SAVED: {S.APPLIED},
    S.APPLIED: {S.INTERVIEW, S.REJECTED},
    S.INTERVIEW: {S.OFFER, S.REJECTED},
    S.OFFER: set(),
    S.REJECTED: set(),
}

class ApplicationNotFound(Exception):
    pass

class InvalidStatusTransition(Exception):
    def __init__(self, current: S, target: S):
        super().__init__(f"Cannot move from '{current.value}' to '{target.value}'")

def create_application(db: Session, user_id: int, data: dict):
    return repo.create(db, user_id, data)

def get_application(db: Session, user_id: int, application_id: int):
    application = repo.get_for_user(db, user_id, application_id)
    if application is None:
        raise ApplicationNotFound()
    return application

def list_applications(db: Session, user_id: int, status: S | None, limit: int, offset: int):
    return repo.list_for_user(db, user_id, status.value if status else None, limit, offset)

def update_application(db: Session, user_id: int, application_id: int, changes: dict):
    application = get_application(db, user_id, application_id)
    return repo.update(db, application, changes)

def change_status(db: Session, user_id: int, application_id: int, new_status: S):
    application = get_application(db, user_id, application_id)
    current = S(application.status)
    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise InvalidStatusTransition(current, new_status)

    changes = {"status": new_status.value}
    if new_status == S.APPLIED and application.applied_date is None:
        changes["applied_date"] = date.today()
    return repo.update(db, application, changes)

def delete_application(db: Session, user_id: int, application_id: int):
    application = get_application(db, user_id, application_id)
    repo.delete(db, application)