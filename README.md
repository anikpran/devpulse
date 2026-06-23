# DevPulse

A personal engineering dashboard that tracks your GitHub activity, calculates your commit streak, and generates an AI-powered weekly digest of your growth as a developer.

**Live demo:** https://devpulse-seven-zeta.vercel.app

---

## What it does

- **GitHub OAuth** — connect your GitHub account securely
- **Activity sync** — pulls your recent push events from the GitHub API
- **Commit streak** — calculates your current consecutive days of coding
- **AI digest** — generates a plain English weekly summary of your activity using the Claude API

---

## Tech stack

**Backend**
- Python + FastAPI
- PostgreSQL + SQLAlchemy
- Docker (local development)
- Deployed on Railway

**Frontend**
- React + Vite
- Deployed on Vercel

**Integrations**
- GitHub OAuth 2.0
- GitHub REST API
- Anthropic Claude API

---

## Architecture
- React Frontend (Vercel)
    ↓
- FastAPI Backend (Railway)
    ↓
- PostgreSQL Database (Railway)
    ↓
- GitHub API + Claude API
The backend follows a layered architecture:
- **Routers** — handle HTTP requests and responses
- **Services** — contain business logic and external API calls
- **Models** — define database tables via SQLAlchemy ORM

---

## Key technical decisions

**Why store GitHub events locally instead of calling the API on every request?**
GitHub's API has rate limits and adds latency to every page load. By syncing events to a local PostgreSQL database, queries are fast and I can run custom analytics that GitHub's API doesn't support natively.

**Why recalculate streaks from history instead of storing them statefully?**
A stateful streak counter can get out of sync if a user doesn't sync every day or connects for the first time with months of history. Recalculating from raw event data is slightly more expensive but always accurate.

**Why use a cache-aside pattern for the event store?**
Pulling events on demand and caching them locally means the dashboard loads from the database rather than waiting on GitHub's API, keeping response times fast regardless of GitHub's availability.

---

## Running locally

**Prerequisites:** Python 3.10+, Docker, Node.js

**Backend:**
```bash
git clone https://github.com/anikpran/devpulse
cd devpulse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d
uvicorn app.main:app --reload
```

**Environment variables** — create a `.env` file:
- DATABASE_URL=postgresql://devpulse:devpulse@localhost:5432/devpulse
- GITHUB_CLIENT_ID=your_github_client_id
- GITHUB_CLIENT_SECRET=your_github_client_secret
- SECRET_KEY=your_secret_key
- ANTHROPIC_API_KEY=your_anthropic_key

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/github/login` | Initiates GitHub OAuth flow |
| GET | `/github/callback` | OAuth callback, saves access token |
| POST | `/github/sync/{username}` | Syncs latest GitHub events |
| GET | `/stats/{username}` | Returns current commit streak |
| GET | `/stats/digest/{username}` | Returns AI weekly digest |

---

## Note on AI digest

The digest feature requires an Anthropic API key with available credits. The endpoint returns a graceful fallback message if credits are unavailable.