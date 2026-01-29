# AI PR Reviewer - Project Setup Guide

## Completed Setup Checklist

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions (N/A - no extensions required)
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## Project Overview

Full-stack AI Pull Request Reviewer with:
- **Backend**: FastAPI with LangChain + OpenAI GPT-4 integration
- **Frontend**: Next.js dashboard with Tailwind CSS
- **GitHub Integration**: GitHub Actions workflow for automatic PR analysis
- **Testing**: pytest for backend health checks

## Quick Start

### Backend Development
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example ../.env
# Add your OPENAI_API_KEY to .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```
Dashboard available at: http://localhost:3000

## Environment Configuration

Copy `.env.example` to `.env` and set required variables:
- `OPENAI_API_KEY` - Your OpenAI API key for GPT-4 access
- `GITHUB_APP_ID` - (Optional) GitHub App ID for private repos
- `GITHUB_WEBHOOK_SECRET` - (Optional) Secret for webhook signature verification

Copy `frontend/.env.local.example` to `frontend/.env.local` if customizing the API base URL.

## Key Endpoints

- `GET /health` - Health check
- `POST /review` - Analyze PR from direct input
- `POST /review/github` - Fetch and analyze PR from GitHub
- `GET /reviews` - View all past reviews
- `POST /webhook` - GitHub webhook handler

## File Locations

- Backend config: [backend/app/config.py](backend/app/config.py)
- Backend main: [backend/app/main.py](backend/app/main.py)
- Reviewer service: [backend/app/services/reviewer.py](backend/app/services/reviewer.py)
- Frontend page: [frontend/src/app/page.tsx](frontend/src/app/page.tsx)
- GitHub Action: [.github/workflows/ai-review.yml](.github/workflows/ai-review.yml)
- Readme: [README.md](README.md)

## Development Notes

- Both backend and frontend are running with hot-reload enabled
- Backend tests pass: `cd backend && pytest tests/test_health.py`
- Frontend builds successfully: `cd frontend && npm run build`
- Project structure supports both containerized and local deployment
