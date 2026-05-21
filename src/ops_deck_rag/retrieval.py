from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ops_deck_rag.metrics_store import compare_months, load_metrics
from ops_deck_rag.vector_store import search_slides


@dataclass(frozen=True)
class RetrievalContext:
    slide_context: str
    metric_context: str

    @property
    def text(self) -> str:
        sections = []
        if self.slide_context:
            sections.append(f"SLIDE CONTEXT:\n{self.slide_context}")
        if self.metric_context:
            sections.append(f"METRIC CONTEXT:\n{self.metric_context}")
        return "\n\n---\n\n".join(sections) or "[No matching context found]"


def build_slide_context(question: str, month: str | None, business_unit: str | None, k: int) -> str:
    docs = search_slides(question, month=month, business_unit=business_unit, k=k)
    blocks = []
    for doc in docs:
        label = doc.metadata.get("source_label", "unknown source")
        blocks.append(f"SOURCE: {label}\n{doc.page_content}")
    return "\n\n---\n\n".join(blocks)


def build_metric_context(
    question: str,
    month: str | None,
    business_unit: str | None,
    max_rows: int = 25,
) -> str:
    df = load_metrics()
    if df.empty or not month:
        return ""

    metric_df = compare_months(
        metric_query=question,
        month_a=month,
        month_b=month,
        business_unit=business_unit,
    )
    if metric_df.empty:
        metric_df = df[df["month"].eq(month)].copy()
        if business_unit:
            metric_df = metric_df[metric_df["business_unit"].fillna("").eq(business_unit)]

    if metric_df.empty:
        return ""

    columns = [
        "deck_name",
        "month",
        "business_unit",
        "slide_number",
        "slide_title",
        "metric_name",
        "category",
        "series",
        "value",
        "source_type",
    ]
    available_columns = [column for column in columns if column in metric_df.columns]
    return pd.DataFrame(metric_df[available_columns].head(max_rows)).to_markdown(index=False)


def retrieve_context(
    question: str,
    month: str | None = None,
    business_unit: str | None = None,
    k: int = 5,
) -> RetrievalContext:
    return RetrievalContext(
        slide_context=build_slide_context(question, month, business_unit, k),
        metric_context=build_metric_context(question, month, business_unit),
    )
