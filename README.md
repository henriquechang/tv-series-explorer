# TV Series Explorer

Interactive TV series browsing with AI-powered insights and episode tracking.

## Tech Stack

- **Backend:** Python 3.10, FastAPI 0.128.0, SQLAlchemy with SQLite
- **Frontend:** React 19.2.0, TypeScript 5.9.3, Vite
- **Docker:** Multi-stage build with Nginx serving frontend
- **AI:** HuggingFace Inference API (with fallback)

## Features

- Browse TV series and seasons
- Track watched episodes
- Add comments to episodes
- AI-powered episode insights
- Persistent data storage with SQLite

## Quick Start (Docker)

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+ (or Docker Compose V2)

### Running with Docker Compose

Create a `.env` file in the project root:

```bash
HUGGINGFACE_API_KEY=hf_your_token_here
```

Then run:

```bash
docker compose up --build
```

Without the key, AI insights will use a fallback response.

> **Note:** The API key will be provided separately via email.

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- npm

### Backend

```bash
cd backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

pytest -v

uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

### Frontend

```bash
cd frontend

npm install
npm test
npm run dev
```
## Docker Architecture

The application uses a multi-stage Docker build:

1. **Frontend Build Stage:** Node.js Alpine image builds the React application
2. **Runtime Stage:** Python slim image runs both:
   - Nginx (port 80) serving the frontend and proxying API requests
   - Uvicorn (port 7777) running the FastAPI backend

The `docker-compose.yml` configures:
- **database service:** Alpine container for SQLite volume management
- **app service:** Combined frontend/backend application
- **Persistent volume:** Stores SQLite database at `/app/data`
