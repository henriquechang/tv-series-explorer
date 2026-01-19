from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.api.routes import shows, episodes
from app.infrastructure.api.dependencies import cleanup_clients


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await cleanup_clients()


app = FastAPI(
    title="TV Series Explorer",
    description="Interactive TV series browsing experience",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shows.router, prefix="/api")
app.include_router(episodes.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}