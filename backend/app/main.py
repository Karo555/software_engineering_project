"""Placeholder app so the backend container starts. Replaced by the scaffold in #16."""

from fastapi import FastAPI

app = FastAPI(title="Nodebook API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
