from sqlalchemy.orm import Session

from app.ai import embeddings
from app.ai.extraction import extract_job_info
from app.repositories import application_repository as app_repo
from app.repositories import resume_repository
from app.services import matching
from app.services.application_service import get_application


class ResumeRequired(Exception):
    pass


class JobDescriptionRequired(Exception):
    pass


def analyze_application(db: Session, user_id: int, application_id: int):
    application = get_application(db, user_id, application_id)
    if not (application.job_description or "").strip():
        raise JobDescriptionRequired()
    resume = resume_repository.get_for_user(db, user_id)
    if resume is None:
        raise ResumeRequired()

    job = extract_job_info(application.job_description)
    matched, missing, coverage = matching.skill_coverage(job.skills, resume.text)

    job_vectors = embeddings.embed(embeddings.chunk_text(application.job_description))
    semantic = matching.semantic_score(job_vectors, embeddings.from_bytes(resume.embedding))

    analysis = {
        "seniority": job.seniority,
        "keywords": job.keywords,
        "matched_skills": matched,
        "missing_skills": missing,
        "semantic_score": round(semantic, 3),
        "skill_coverage": None if coverage is None else round(coverage, 3),
    }
    skill_names = sorted({matching.normalize_skill(s) for s in job.skills})
    return app_repo.save_analysis(
        db, application, skill_names, analysis, matching.combine(semantic, coverage)
    )