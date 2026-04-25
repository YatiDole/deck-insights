from __future__ import annotations

from pathlib import Path

import pandas as pd

from ops_deck_rag.config import settings
from ops_deck_rag.models import MetricRecord


def metrics_path(metrics_dir: Path | None = None) -> Path:
    directory = metrics_dir or settings.metrics_dir
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "metrics.csv"


def append_metrics(metrics: list[MetricRecord], metrics_dir: Path | None = None) -> int:
    path = metrics_path(metrics_dir)
    if not metrics:
        return 0
    df = pd.DataFrame([m.model_dump() for m in metrics])
    if path.exists():
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True)
        df = df.drop_duplicates(
            subset=["deck_id", "slide_number", "source_type", "chart_title", "table_title", "series", "category", "value"],
            keep="last",
        )
    df.to_csv(path, index=False)
    return len(metrics)


def load_metrics(metrics_dir: Path | None = None) -> pd.DataFrame:
    path = metrics_path(metrics_dir)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def compare_months(metric_query: str, month_a: str, month_b: str, business_unit: str | None = None) -> pd.DataFrame:
    df = load_metrics()
    if df.empty:
        return df
    mask = df["month"].isin([month_a, month_b])
    if business_unit:
        mask &= df["business_unit"].fillna("").eq(business_unit)
    if metric_query:
        q = metric_query.lower()
        mask &= (
            df["metric_name"].fillna("").str.lower().str.contains(q)
            | df["chart_title"].fillna("").str.lower().str.contains(q)
            | df["series"].fillna("").str.lower().str.contains(q)
            | df["category"].fillna("").str.lower().str.contains(q)
        )
    return df.loc[mask].copy()
