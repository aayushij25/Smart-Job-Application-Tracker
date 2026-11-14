from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user
from app.api import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}