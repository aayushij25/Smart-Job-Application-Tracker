from datetime import date, datetime, timezone

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ApplicationStatus
from app.models.skill import Skill, application_skills

class Application(Base):
    __tablename__ = "applications"
    __table_args__= (Index("ix_applications_user_status", "user_id", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(
        String(20), default=ApplicationStatus.SAVED.value
    )
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    match_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    skill_rows: Mapped[list[Skill]] = relationship(secondary=application_skills)

    @property
    def skills(self) -> list[str]:
        return sorted(skill.name for skill in self.skill_rows)
    