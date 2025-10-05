# Contributing to JDM Pulse

Thanks for your interest in contributing! Please follow these guidelines to keep the project high quality and easy to work with.

## Development setup
- Python 3.11+ for backend
- Node.js 18+ (recommended 20/22) for frontend
- On Windows, PowerShell (pwsh) works fine

## Backend (FastAPI)
- Install deps: `pip install -r backend/requirements.txt -r backend/requirements-dev.txt`
- Run dev server: `python -m uvicorn backend.app.main:app --reload`
- Tests: `pytest backend/tests -q`

## Frontend (Next.js)
- Install deps: `npm --prefix frontend ci`
- Dev: `npm --prefix frontend run dev`
- Build: `npm --prefix frontend run build`
- Lint: `npm --prefix frontend run lint`

## Pull Requests
- Fork and create a feature branch from `main`
- Keep PRs small and focused
- Add/adjust tests where applicable
- Ensure CI passes (backend + frontend workflows)

## Commit messages
- Use conventional style when possible (feat:, fix:, chore:, docs:, test:)

## Code of Conduct
- See CODE_OF_CONDUCT.md