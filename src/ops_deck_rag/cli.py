from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from ops_deck_rag.extractors import extract_deck
from ops_deck_rag.metrics_store import append_metrics, compare_months
from ops_deck_rag.qa import ask
from ops_deck_rag.vector_store import upsert_slides

app = typer.Typer(help="Ops deck RAG assistant")


@app.command()
def ingest(
    deck: Path = typer.Argument(..., exists=True, readable=True, help="Path to .pptx deck"),
    month: str = typer.Option(..., help="Deck month, e.g. 2026-04"),
    business_unit: str | None = typer.Option(None, help="Optional business unit label"),
):
    """Extract slide text, tables, and native chart data, then index them."""
    slides, metrics = extract_deck(deck, month=month, business_unit=business_unit)
    slide_count = upsert_slides(slides)
    metric_count = append_metrics(metrics)
    print(f"[green]Indexed {slide_count} slides and {metric_count} metric records.[/green]")


@app.command()
def query(
    question: str,
    month: str | None = typer.Option(None),
    business_unit: str | None = typer.Option(None),
    k: int = typer.Option(5),
):
    """Ask a question against indexed decks."""
    print(ask(question, month=month, business_unit=business_unit, k=k))


@app.command("compare")
def compare_cmd(
    metric: str = typer.Option("", help="Metric/chart/category search text"),
    month_a: str = typer.Option(...),
    month_b: str = typer.Option(...),
    business_unit: str | None = typer.Option(None),
):
    """Show raw extracted metric rows for two months before asking the LLM to interpret them."""
    df = compare_months(metric, month_a, month_b, business_unit)
    if df.empty:
        print("[yellow]No matching metric rows found.[/yellow]")
    else:
        print(df.to_markdown(index=False))
