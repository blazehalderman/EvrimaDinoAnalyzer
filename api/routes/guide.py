# api/routes/guide.py
# GET /guide/{dino} — per-dinosaur play guide with growth-stage profiles.

from fastapi import APIRouter, HTTPException
from api.models.schemas import GuideResponse

router = APIRouter()


@router.get("/{dino}", response_model=GuideResponse, summary="Play guide for a dinosaur")
def get_guide(dino: str) -> GuideResponse:
    """Return growth-stage playstyle profiles and Doqi commentary for the given species."""
    raise HTTPException(status_code=501, detail="Phase 4 — requires Source 3 data")
