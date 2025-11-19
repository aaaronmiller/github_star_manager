#!/bin/bash
# Pre-commit hook for GitHub Star Manager
# Runs linters on staged files

set -e

echo "Running pre-commit checks..."

# Check if backend files are staged
if git diff --cached --name-only | grep -q "^backend/"; then
  echo "Linting backend..."
  cd backend && npm run lint && cd ..
fi

# Check if frontend files are staged
if git diff --cached --name-only | grep -q "^frontend/"; then
  echo "Linting frontend..."
  cd frontend && npm run lint && cd ..
fi

# Check if CLI files are staged
if git diff --cached --name-only | grep -q "^cli/.*\.py$"; then
  echo "Linting Python CLI..."
  if command -v ruff &> /dev/null; then
    ruff check cli/
  else
    echo "Warning: ruff not found. Skipping Python linting."
  fi
fi

echo "Pre-commit checks passed!"
