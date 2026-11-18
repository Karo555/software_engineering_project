"""Placeholder app so the backend container starts. Replaced by the scaffold in #16."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    get_settings()  # fail at start-up if a required setting is missing or invalid
    yield


app = FastAPI(title="Nodebook API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
