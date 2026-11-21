from fastapi import FastAPI
from app.api import applications, auth
from app.api.errors import register_exception_handlers
from app.core.database import Base, engine
from app.models import user # noqa (no quality assurance warning - F401 imported but unused.)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")
register_exception_handlers(app)
app.include_router(auth.router) # connects the group of routes to the main application
app.include_router(applications.router)

# decorator
@app.get("/health")
def health():
    return {"status": "ok"}