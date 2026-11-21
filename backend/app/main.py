from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user # noqa (no quality assurance warning - F401 imported but unused.)
from app.api import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")
app.include_router(auth.router) # connects the group of routes to the main application

# decorator
@app.get("/health")
def health():
    return {"status": "ok"}