# GitHub Pipeline

## Branch model

Use this structure:

- `main`: stable version only
- `develop`: integration branch if the team grows beyond one developer
- `feature/*`: new features
- `fix/*`: bug fixes
- `experiment/*`: throwaway research branches

For a small team, you can skip `develop` and merge PRs directly into `main` after CI passes.

## First-time repo setup

```bash
git init
git add .
git commit -m "Initial ops deck RAG project"
git branch -M main
git remote add origin git@github.com:YOUR_ORG/ops-deck-rag.git
git push -u origin main
```

## Every iteration

```bash
git checkout main
git pull
git checkout -b feature/descriptive-name

# make code changes
pytest
ruff check .

git add .
git commit -m "Short imperative summary"
git push -u origin feature/descriptive-name
```

Then open a pull request.

## Pull request checklist

Before merging, require:

- CI passes
- No secrets committed
- Tests added or updated
- README/docs updated if behavior changed
- Sample output included in the PR description
- Known extraction limitations documented

## Versioning

Use tags for meaningful releases:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Suggested release milestones:

- `v0.1.0`: text + native table/chart extraction
- `v0.2.0`: metrics database replaces CSV
- `v0.3.0`: source Excel/CSV ingestion
- `v0.4.0`: web UI
- `v1.0.0`: access controls, audit logs, validated extraction accuracy
