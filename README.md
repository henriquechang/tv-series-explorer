# TV Series Explorer

Interactive TV series browsing with AI-powered insights.

## Tech Stack

- **Backend:** Python 3.10, FastAPI 0.128.0
- **Frontend:** React 19.2.0, TypeScript 5.9.3
- **Docker:** Compose v3.3
- **HuggingFace Inference API (with fallback)** Compose v3.3

## Quick Start (Docker)

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+ (or Docker Compose V2)

### With HuggingFace API Key (Optional)

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

### Access

| Mode | URL |
|------|-----|
| Development (frontend) | http://localhost:3000 |
| Development (backend API) | http://localhost:7777 |
| Docker | http://localhost:7777 |
