from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(min_length=50, max_length=20000)


class ResumeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    updated_at: datetime