from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import dinos, matchup, guide

app = FastAPI(
    title="EvrimaDinoAnalyzer API",
    description="MVP API providing normalized data and matchup logic for The Isle: Evrima.",
    version="1.0"
)

# Allow frontend fetching
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, including file:// (null)
    allow_credentials=False, # Must be False if using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dinos.router, prefix="/api/dinos", tags=["Dinosaurs"])
app.include_router(matchup.router, prefix="/analyze", tags=["Matchups"])
app.include_router(guide.router, prefix="/guide", tags=["Guides"])

# Serve frontend static files — relative to CWD (project root on Render)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
