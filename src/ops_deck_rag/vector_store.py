from __future__ import annotations

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from ops_deck_rag.config import settings
from ops_deck_rag.models import SlideRecord


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


def get_store(persist_directory: Path | None = None) -> Chroma:
    directory = persist_directory or settings.chroma_dir
    directory.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name="ops_deck_slides",
        embedding_function=get_embeddings(),
        persist_directory=str(directory),
    )


def upsert_slides(slides: list[SlideRecord], persist_directory: Path | None = None) -> int:
    store = get_store(persist_directory)
    ids = [f"{s.deck_id}:{s.slide_number}" for s in slides]
    texts = [s.to_document_text() for s in slides]
    metadatas = [
        {
            "deck_id": s.deck_id,
            "deck_name": s.deck_name,
            "month": s.month,
            "business_unit": s.business_unit or "",
            "slide_number": s.slide_number,
            "slide_title": s.slide_title or "",
            "source_label": s.source_label,
        }
        for s in slides
    ]
    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    store.persist()
    return len(slides)


def search_slides(query: str, month: str | None = None, business_unit: str | None = None, k: int = 5):
    where = {}
    if month:
        where["month"] = month
    if business_unit:
        where["business_unit"] = business_unit
    return get_store().similarity_search(query=query, k=k, filter=where or None)
