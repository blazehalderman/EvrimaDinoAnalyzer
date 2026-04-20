# api/routes/dinos.py
# GET /dinos          — list all dinosaurs
# GET /dinos/{name}   — full stat detail for one dinosaur

from fastapi import APIRouter, HTTPException
from api.models.schemas import DinoSummary, DinoDetail

router = APIRouter()


@router.get("/", response_model=list[DinoSummary], summary="List all dinosaurs")
def list_dinos() -> list[DinoSummary]:
    """Return a summary list of all dinosaurs in the normalized dataset."""
    raise HTTPException(status_code=501, detail="Phase 4 — not yet implemented")


@router.get("/{name}", response_model=DinoDetail, summary="Get dinosaur detail")
def get_dino(name: str) -> DinoDetail:
    """Return full stat detail for the specified dinosaur species."""
    raise HTTPException(status_code=501, detail="Phase 4 — not yet implemented")
