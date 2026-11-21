from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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