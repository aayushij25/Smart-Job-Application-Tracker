from sqlalchemy.orm import Session

from app.models.resume import Resume


def get_for_user(db: Session, user_id: int) -> Resume | None:
    return db.query(Resume).filter(Resume.user_id == user_id).first()


def upsert(db: Session, user_id: int, text: str, embedding: bytes) -> Resume:
    resume = get_for_user(db, user_id)
    if resume is None:
        resume = Resume(user_id=user_id, text=text, embedding=embedding)
        db.add(resume)
    else:
        resume.text = text
        resume.embedding = embedding
    db.commit()
    db.refresh(resume)
    return resume