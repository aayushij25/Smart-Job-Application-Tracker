from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.enums import ApplicationStatus

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    job_description: str | None = None
    notes: str | None = None
    applied_date: date | None = None 

class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, min_length=1, max_length=200)
    job_description: str | None = None
    notes: str | None = None
    applied_date: date | None = None

    @field_validator("company", "role")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("cannot be null")
        return value

class StatusUpdate(BaseModel):
    status: ApplicationStatus

class AnalysisOut(BaseModel):
    seniority: str | None = None
    keywords: list[str] = []
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    semantic_score: float | None = None
    skill_coverage: float | None = None

class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: ApplicationStatus
    job_description: str | None
    match_score: float | None
    notes: str | None
    applied_date: date | None
    created_at: datetime
    skills: list[str] = []
    analysis: AnalysisOut | None = None

class ApplicationList(BaseModel):
    items: list[ApplicationOut]
    total: int
    limit: int
    offset: int


