from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.resume import ResumeOut, ResumeUpdate
from app.services import resume_service

router = APIRouter(prefix="/resume", tags=["resume"])


@router.get("", response_model=ResumeOut | None)
def get_resume(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return resume_service.get_resume(db, current_user.id)


@router.put("", response_model=ResumeOut)
def save_resume(payload: ResumeUpdate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    return resume_service.save_resume(db, current_user.id, payload.text)