from sqlalchemy.orm import Session, selectinload

from app.models.application import Application
from app.repositories import skill_repository

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
    items = (
        query.options(selectinload(Application.skill_rows))
        .order_by(Application.created_at.desc(), Application.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
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

def save_analysis(db: Session, application: Application, skill_names: list[str],
                  analysis: dict, score: float) -> Application:
    application.skill_rows = skill_repository.get_or_create_many(db, skill_names)
    application.analysis = analysis
    application.match_score = score
    db.commit()
    db.refresh(application)
    return application