from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DIM = 384


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)  # loaded once, reused for every request


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, 384) float32 array, one row per text."""
    if not texts:
        return np.zeros((0, DIM), dtype=np.float32)
    return np.asarray(_model().encode(texts), dtype=np.float32)


def chunk_text(text: str, size: int = 120, overlap: int = 30) -> list[str]:
    """Sliding window over words, so each chunk fits the model's ~256-token limit."""
    words = text.split()
    chunks = []
    for start in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[start : start + size]))
        if start + size >= len(words):
            break
    return chunks


def to_bytes(matrix: np.ndarray) -> bytes:
    return matrix.astype(np.float32).tobytes()


def from_bytes(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32).reshape(-1, DIM)