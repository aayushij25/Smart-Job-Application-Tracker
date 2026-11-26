from functools import lru_cache
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DIM = 384
CACHE_DIR = Path(__file__).resolve().parents[2] / ".model_cache"  # backend/.model_cache


@lru_cache(maxsize=1)
def _model() -> TextEmbedding:
    return TextEmbedding(model_name=MODEL_NAME, cache_dir=str(CACHE_DIR))


def warm_up() -> None:
    """Download and load the model. Called at build time so deploys start fast."""
    _model()


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, 384) float32 array, one row per text."""
    if not texts:
        return np.zeros((0, DIM), dtype=np.float32)
    return np.asarray(list(_model().embed(texts)), dtype=np.float32)


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