import re

import numpy as np

ALIASES = {
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "gcp": "google cloud",
}


def normalize_skill(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip().lower())
    return ALIASES.get(key, key)


def _surface_forms(skill: str) -> set[str]:
    return {skill} | {alias for alias, canon in ALIASES.items() if canon == skill}


def appears_in(skill: str, text: str) -> bool:
    """Whole-word match, so 'java' does not match 'javascript' and 'c++' still works."""
    lowered = text.lower()
    for form in _surface_forms(skill):
        pattern = r"(?<![a-z0-9])" + re.escape(form) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            return True
    return False


def skill_coverage(job_skills: list[str], resume_text: str):
    """Which required skills does the resume mention? Returns (matched, missing, coverage)."""
    required = {normalize_skill(s) for s in job_skills if s.strip()}
    matched = {s for s in required if appears_in(s, resume_text)}
    missing = required - matched
    coverage = len(matched) / len(required) if required else None
    return sorted(matched), sorted(missing), coverage


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """cos(theta) = (a . b) / (|a| |b|). Written by hand on purpose."""
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def cosine_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Cosine similarity of every row of a with every row of b: (n x d), (m x d) -> (n x m)."""
    a_unit = a / np.maximum(np.linalg.norm(a, axis=1, keepdims=True), 1e-12)
    b_unit = b / np.maximum(np.linalg.norm(b, axis=1, keepdims=True), 1e-12)
    return a_unit @ b_unit.T


def semantic_score(job_vecs: np.ndarray, resume_vecs: np.ndarray,
                   low: float = 0.15, high: float = 0.65) -> float:
    """For each chunk of the job, find its best-matching resume chunk, then average.

    Raw cosine for this model rarely goes above ~0.7 even for good matches, so we
    stretch [low, high] onto [0, 1]. Both numbers are guesses you will tune.
    """
    if len(job_vecs) == 0 or len(resume_vecs) == 0:
        return 0.0
    sims = cosine_matrix(job_vecs, resume_vecs)
    raw = float(sims.max(axis=1).mean())
    return float(np.clip((raw - low) / (high - low), 0.0, 1.0))


def combine(semantic: float, coverage: float | None) -> float:
    if coverage is None:  # the job listed no skills, so rely on meaning alone
        return round(semantic, 3)
    return round(0.6 * semantic + 0.4 * coverage, 3)