from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, LargeBinary, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _now():
    return datetime.now(timezone.utc)


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)  # one resume per user
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)