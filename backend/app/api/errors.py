import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.ai.errors import AIError

from app.services.analysis_service import JobDescriptionRequired, ResumeRequired

from app.services.application_service import (
    ApplicationNotFound,
    InvalidStatusTransition,
)

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationNotFound)
    async def handle_not_found(request: Request, exc: ApplicationNotFound):
        return JSONResponse(status_code=404, content={"detail": "Application not found"})

    @app.exception_handler(InvalidStatusTransition)
    async def handle_bad_transition(request: Request, exc: InvalidStatusTransition):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ResumeRequired)
    async def handle_resume_required(request: Request, exc: ResumeRequired):
        return JSONResponse(status_code=400, content={"detail": "Add your resume first (use the Resume button)."})

    @app.exception_handler(JobDescriptionRequired)
    async def handle_jd_required(request: Request, exc: JobDescriptionRequired):
        return JSONResponse(status_code=400, content={"detail": "Add a job description and save it before analyzing."})

    @app.exception_handler(AIError)
    async def handle_ai_error(request: Request, exc: AIError):
        return JSONResponse(status_code=502, content={"detail": str(exc)})  # 502: our upstream failed