# api/routes/matchup.py
# POST /analyze — MVP endpoint: input dino + growth % → full combat viability report.

from fastapi import APIRouter, HTTPException
from api.models.schemas import MatchupRequest, MatchupResponse

router = APIRouter()


@router.post("/", response_model=MatchupResponse, summary="Combat viability analyzer")
def analyze_matchup(request: MatchupRequest) -> MatchupResponse:
    """Given a species, growth %, and prime status, return a full matchup breakdown
    against every other dinosaur in the dataset."""
    raise HTTPException(status_code=501, detail="Phase 4 — not yet implemented")
