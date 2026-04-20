# api/routes/guide.py
from fastapi import APIRouter, HTTPException
from api.models.schemas import GuideResponse
from api.database import db
from analysis.playstyle_profiler import generate_playstyle

router = APIRouter()

@router.get("/{dino}", response_model=GuideResponse, summary="Play guide for a dinosaur")
def get_guide(dino: str):
    """Return growth-stage playstyle profiles and Doqi commentary for the given species."""
    profile = db.get_dino_by_name(dino)
    if not profile:
        raise HTTPException(status_code=404, detail="Dino not found")
    
    tips = generate_playstyle(profile)
    
    return GuideResponse(
        species=dino,
        diet=str(profile.get("Diet", "Unknown") or "Unknown"),
        nest_type=str(profile.get("Nest_Type", "Unknown") or "Unknown"),
        max_eggs=int(profile.get("Max_Eggs", 0) or 0),
        can_eat_bones=str(profile.get("Can_Eat_Bones", "No") or "No"),
        vomits_from_overeating=str(profile.get("Vomits_From_Overeating", "No") or "No"),
        playstyle_tips=tips
    )
