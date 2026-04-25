from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
    chroma_dir: Path = Path(os.getenv("CHROMA_DIR", "data/chroma"))
    metrics_dir: Path = Path(os.getenv("METRICS_DIR", "data/metrics"))
    max_context_chars: int = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))
    max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", "700"))


settings = Settings()
