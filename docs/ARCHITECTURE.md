# Architecture

## Pipeline

```text
Monthly PowerPoint deck
  ↓
PowerPoint extractor
  ↓
Slide records + metric records
  ↓                    ↓
Chroma vector DB        metrics.csv
  ↓                    ↓
RAG Q&A              month-over-month metric checks
  ↓
Answer with slide citations
```

## Why hybrid storage is necessary

A pure vector database is bad at numeric operations. It can find relevant text, but it is not reliable for calculating deltas, ranking KPIs, or comparing time periods.

This repo uses two stores:

1. **Chroma vector store** for semantic retrieval of slides.
2. **CSV metrics store** for extracted chart/table facts.

In production, replace CSV with Postgres, DuckDB, BigQuery, Snowflake, or your existing warehouse.

## Extraction coverage

| Source type | Support level | Notes |
|---|---:|---|
| Text boxes | Strong | Extracted from normal PowerPoint shapes |
| Native PPT tables | Strong | Converted to markdown and metric rows |
| Native PPT charts | Medium/Strong | Extracts chart title, series, category, values where supported by python-pptx |
| Screenshot charts | Weak | Requires OCR or source data |
| Embedded Excel | Future | Better handled by source file ingestion |
| Speaker notes | Future | Useful if analysts write context in notes |

## Recommended production upgrade path

1. Add sanitized sample decks for tests.
2. Replace CSV metrics store with a real database.
3. Add OCR only as a fallback, not the primary path.
4. Integrate original Excel/BI exports for chart data.
5. Add authentication and audit logs.
6. Add answer evaluation tests.
