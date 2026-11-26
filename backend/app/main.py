from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import applications, auth, resume as resume_routes
from app.api.errors import register_exception_handlers
from app.core.database import Base, engine
from app.models import application, resume as resume_model, skill, user # noqa (no quality assurance warning - F401 imported but unused.)
from app.core import config

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)
app.include_router(auth.router) # connects the group of routes to the main application
app.include_router(applications.router)
app.include_router(resume_routes.router)

# decorator
@app.get("/health")
def health():
    return {"status": "ok"}