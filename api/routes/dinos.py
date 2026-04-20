from fastapi import APIRouter, HTTPException
from api.database import db

router = APIRouter()

@router.get("")
def get_dinos():
    """Returns a list of all dinosaurs and their core normalized stats."""
    dinos = db.get_all_dinos()
    if not dinos:
        raise HTTPException(status_code=404, detail="No dinosaur data found. Normalization may have failed.")
    return {"dinosaurs": dinos}

@router.get("/{name}")
def get_dino(name: str):
    """Returns the full profile for a specific dinosaur."""
    dino = db.get_dino_by_name(name)
    if not dino:
        raise HTTPException(status_code=404, detail=f"Dinosaur '{name}' not found.")
    
    # If mechanics are loaded, attach them to the profile
    mechanics = []
    if db.mechanics is not None:
        mech_rows = db.mechanics[db.mechanics['Dinosaur'].str.lower() == name.lower()]
        mechanics = mech_rows.to_dict(orient="records")
        for m in mechanics:
            # Drop the redundant Dinosaur key in the mechanic dict
            m.pop("Dinosaur", None)
            
    dino["mechanics"] = mechanics
    return dino
