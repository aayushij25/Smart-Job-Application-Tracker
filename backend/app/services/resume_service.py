from sqlalchemy.orm import Session

from app.ai import embeddings
from app.repositories import resume_repository


def get_resume(db: Session, user_id: int):
    return resume_repository.get_for_user(db, user_id)


def save_resume(db: Session, user_id: int, text: str):
    # Embed once on write, so Analyze never has to re-embed the resume
    vectors = embeddings.embed(embeddings.chunk_text(text))
    return resume_repository.upsert(db, user_id, text, embeddings.to_bytes(vectors))