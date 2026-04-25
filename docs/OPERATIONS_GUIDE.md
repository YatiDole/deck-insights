# Operations Guide

## Monthly runbook

1. Export the finalized monthly deck as `.pptx`.
2. Place it in `data/raw/` locally. Do not commit it.
3. Run ingestion:

```bash
ops-rag ingest data/raw/monthly_ops_deck.pptx --month 2026-04 --business-unit all
```

4. Ask smoke-test questions:

```bash
ops-rag query "Summarize the deck in 5 bullets with slide sources" --month 2026-04
ops-rag query "Which metrics got worse?" --month 2026-04
ops-rag compare --metric revenue --month-a 2026-03 --month-b 2026-04
```

5. Validate extracted chart/table values against the source deck.
6. Record extraction issues as GitHub issues.

## Quality bar

A leadership-facing answer must:

- cite deck and slide number
- distinguish actual data from interpretation
- say when data is missing
- avoid invented deltas
- use extracted chart/table values when available

## Known failure modes

- Screenshot charts may not produce numeric values.
- Some PowerPoint chart types expose incomplete data through `python-pptx`.
- Tables with merged cells may extract awkwardly.
- RAG may retrieve the right slide but still need stronger prompting for exact numeric analysis.
