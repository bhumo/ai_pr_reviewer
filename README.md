# AI PR Reviewer

An automated pull request review assistant powered by LangChain and OpenAI GPT-4. Analyzes GitHub PRs for bugs, code smells, and style violations, integrated as a GitHub Action.

## Project Structure

```
.
├── backend/                          # FastAPI service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                 # Settings & environment variables
│   │   ├── main.py                   # FastAPI app & endpoints
│   │   ├── models.py                 # Pydantic models
│   │   └── services/
│   │       ├── github.py             # GitHub integration
│   │       └── reviewer.py           # LangChain-based PR analysis
│   ├── tests/
│   │   └── test_health.py
│   └── requirements.txt
│
├── frontend/                         # Next.js dashboard
│   ├── src/
│   │   └── app/
│   │       ├── layout.tsx
│   │       └── page.tsx              # Dashboard UI
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
│
├── .github/
│   ├── workflows/
│   │   └── ai-review.yml             # GitHub Action workflow
│   └── copilot-instructions.md
│
├── .env.example                      # Backend config template
└── README.md
```

## Features

- **Automated PR Analysis**: Analyzes code for bugs, code smells, style violations
- **LLM Integration**: Uses OpenAI GPT-4 via LangChain
- **GitHub Webhook Support**: Processes PRs via webhook
- **Dashboard**: Modern Next.js frontend with Tailwind CSS
- **GitHub Actions**: Integrated workflow that triggers reviews automatically
- **REST API**: FastAPI backend with full CORS support
- **Guardrails**: LLM-safe prompts, size limits, signature verification, and stubbed reviews when keys are missing

## Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key
- GitHub token (optional, for private repos)

## Setup

### Backend

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp ../.env.example ../.env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=sk-...
   ```

3. **Run the server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`. 
- Health check: `GET /health`
- API docs: `GET /docs`

### Frontend

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.local.example .env.local
   # Update NEXT_PUBLIC_API_BASE if needed
   ```

3. **Run the dev server**:
   ```bash
   npm run dev
   ```

The dashboard will be available at `http://localhost:3000`.

## API Endpoints

### Health Check
- `GET /health` - Service status

### PR Review
- `POST /review` - Analyze PR from direct input
  ```json
  {
    "repo_full_name": "owner/repo",
    "pr_number": 1,
    "title": "Feature: Add auth",
    "body": "...",
    "files": [{"filename": "auth.py", "patch": "..."}],
    "author": "user",
    "url": "..."
  }
  ```

- `POST /review/github` - Fetch and analyze PR from GitHub
  ```json
  {
    "repo_full_name": "owner/repo",
    "pr_number": 1,
    "access_token": "ghp_..."
  }
  ```

- `GET /reviews` - Get all past reviews

### GitHub Webhook
- `POST /webhook` - Handle GitHub events (pulls in PR data automatically)

## GitHub Action Setup

1. Add secrets to your repository:
   - `BACKEND_URL`: Your backend deployment URL

2. The workflow automatically triggers on PR opens/updates and sends data to your backend for analysis.

## Configuration

### Environment Variables

Create `.env` in the project root:

```
OPENAI_API_KEY=sk-...
GITHUB_APP_ID=12345
GITHUB_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...
GITHUB_WEBHOOK_SECRET=your-secret
BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
OPENAI_MODEL=gpt-4o-mini
REVIEW_HISTORY_SIZE=50
MAX_REVIEW_FILES=20
MAX_PATCH_CHARS=20000
LLM_TIMEOUT_SECONDS=30
ALLOW_STUB_REVIEWS=true
```

## Testing

Run backend tests:
```bash
cd backend
pip install pytest
pytest tests/
```

## Development

The project uses:
- **Backend**: FastAPI, LangChain, OpenAI, PyGithub
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **CI/CD**: GitHub Actions

## Deployment

### Backend Deployment (example with Render/Heroku)
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend Deployment (example with Vercel)
```bash
cd frontend
npm run build
npm start
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT
