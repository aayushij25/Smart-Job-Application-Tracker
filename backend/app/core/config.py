import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_FALLBACK_MODEL = os.getenv("LLM_FALLBACK_MODEL")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_tracker.db")
AI_ALLOWED_EMAILS = {
    e.strip().lower() for e in os.getenv("AI_ALLOWED_EMAILS", "").split(",") if e.strip()
}