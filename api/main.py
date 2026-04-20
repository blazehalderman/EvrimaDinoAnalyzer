# api/main.py
# FastAPI application entry point.
# Run with: uvicorn api.main:app --reload

from fastapi import FastAPI
from api.routes import matchup, dinos, guide

app = FastAPI(
    title="EvrimaDinoAnalyzer",
    description="Combat viability analyzer for The Isle: Evrima dinosaurs",
    version="0.1.0",
)

app.include_router(matchup.router, prefix="/analyze",  tags=["matchup"])
app.include_router(dinos.router,   prefix="/dinos",    tags=["dinos"])
app.include_router(guide.router,   prefix="/guide",    tags=["guide"])


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
