# Ops Deck RAG

A repo-ready Retrieval-Augmented Generation assistant for monthly operations PowerPoint decks.

It extracts and indexes:

- Slide text
- PowerPoint tables
- Native PowerPoint chart data
- Metadata: month, deck name, business unit, slide number, slide title

It supports:

- Q&A with slide citations
- Month filtering
- Business-unit filtering
- Month-over-month metric inspection
- GitHub CI for every iteration

## What this is good for

Use this when your team creates recurring monthly operations decks and wants to ask questions like:

- What changed from March to April?
- Which KPIs are below target?
- What risks were mentioned in the current month?
- Which slide discusses fulfillment backlog?
- Summarize the April deck with source slide citations.

## What this does not solve perfectly yet

This extracts native PowerPoint charts and native PowerPoint tables. If a chart or table is just an image/screenshot, extraction will be weaker. The right production solution is to connect the original Excel/CSV/BI source rather than trusting OCR.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env`:

```bash
GROQ_API_KEY=your_key_here
```

## Ingest a deck

```bash
ops-rag ingest data/raw/april_ops_deck.pptx --month 2026-04 --business-unit revenue
```

## Ask a question

```bash
ops-rag query "What were the biggest KPI movements?" --month 2026-04
```

## Compare two months

```bash
ops-rag compare --metric revenue --month-a 2026-03 --month-b 2026-04
```

## Repo workflow

Use branches and pull requests for every iteration. Do not push directly to `main`.

```bash
git checkout -b feature/chart-extraction-v1
git add .
git commit -m "Add native chart and table extraction"
git push -u origin feature/chart-extraction-v1
```

Open a PR into `main`. GitHub Actions will run linting and tests.

## Critical production warnings

1. Do not store company decks in a public repo.
2. Do not commit `.env` or API keys.
3. Validate extracted chart numbers against the source deck.
4. Add permission controls before leadership uses this.
5. Add regression tests using sanitized sample decks.
