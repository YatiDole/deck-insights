from __future__ import annotations

from pydantic import BaseModel, Field


class SlideRecord(BaseModel):
    deck_id: str
    deck_name: str
    month: str
    business_unit: str | None = None
    slide_number: int
    slide_title: str | None = None
    text: str = ""
    tables_markdown: list[str] = Field(default_factory=list)
    charts_markdown: list[str] = Field(default_factory=list)

    @property
    def source_label(self) -> str:
        title = f" — {self.slide_title}" if self.slide_title else ""
        return f"{self.deck_name}, slide {self.slide_number}{title}"

    def to_document_text(self) -> str:
        sections = [
            f"Deck: {self.deck_name}",
            f"Month: {self.month}",
            f"Business unit: {self.business_unit or 'Unspecified'}",
            f"Slide: {self.slide_number}",
            f"Slide title: {self.slide_title or 'Untitled'}",
            "",
            "Slide text:",
            self.text.strip() or "[No text extracted]",
        ]
        if self.tables_markdown:
            sections.extend(["", "Extracted tables:", *self.tables_markdown])
        if self.charts_markdown:
            sections.extend(["", "Extracted charts:", *self.charts_markdown])
        return "\n".join(sections)


class MetricRecord(BaseModel):
    deck_id: str
    deck_name: str
    month: str
    business_unit: str | None = None
    slide_number: int
    slide_title: str | None = None
    chart_title: str | None = None
    table_title: str | None = None
    metric_name: str
    category: str | None = None
    series: str | None = None
    value: str | float | int | None = None
    source_type: str
