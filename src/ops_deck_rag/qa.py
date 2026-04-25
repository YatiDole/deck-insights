from __future__ import annotations

from groq import Groq

from ops_deck_rag.config import settings
from ops_deck_rag.vector_store import search_slides

SYSTEM_RULES = """
You are an operations-deck analyst. Answer only from the supplied context.
Every material claim must include source labels such as deck name and slide number.
If the context does not contain the answer, say so. Do not invent KPI values.
When chart or table data is present, prioritize the extracted values over surrounding prose.
""".strip()


def ask(question: str, month: str | None = None, business_unit: str | None = None, k: int = 5) -> str:
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

    docs = search_slides(question, month=month, business_unit=business_unit, k=k)
    context_blocks = []
    for doc in docs:
        label = doc.metadata.get("source_label", "unknown source")
        context_blocks.append(f"SOURCE: {label}\n{doc.page_content}")
    context = "\n\n---\n\n".join(context_blocks)[: settings.max_context_chars]

    prompt = f"""
{SYSTEM_RULES}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    client = Groq(api_key=settings.groq_api_key)
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_output_tokens,
    )
    return response.choices[0].message.content
