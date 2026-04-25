#!/usr/bin/env bash
set -euo pipefail

REPO_NAME=${1:-ops-deck-rag}
VISIBILITY=${2:-private}

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is required. Install it first: https://cli.github.com/"
  exit 1
fi

git init
git add .
git commit -m "Initial ops deck RAG project"
git branch -M main
gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push
