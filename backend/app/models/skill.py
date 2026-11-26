from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

# Join table: one application has many skills, one skill belongs to many applications
application_skills = Table(
    "application_skills",
    Base.metadata,
    Column("application_id", ForeignKey("applications.id"), primary_key=True),
    Column("skills_id", ForeignKey("skills.id"), primary_key=True),
)


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)