from sqlalchemy.orm import Session

from app.models.application import Application

def create(db: Session, user_id: int, data: dict) -> Application:
    application = Application(user_id=user_id, **data)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

def get_for_user(db: Session, user_id: int, application_id: int) -> Application | None:
    return (
        db.query(Application).filter(Application.id == application_id, Application.user_id == user_id).first()
    )

def list_for_user(db: Session, user_id: int, status: str | None, limit: int, offset: int) -> tuple[list[Application], int]:
    query = db.query(Application).filter(Application.user_id == user_id)
    if status:
        query = query.filter(Application.status == status)
    total = query.count()
    items = (query.order_by(Application.created_at.desc(), Application.id.desc()).limit(limit).offset(offset).all())
    return items, total

def update(db: Session, application: Application, changes: dict) -> Application:
    for field, value in changes.items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application

def delete(db: Session, application: Application) -> None:
    db.delete(application)
    db.commit()