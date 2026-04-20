from fastapi import APIRouter, HTTPException
from api.database import db
from api.models.schemas import AnalyzeRequest, AnalyzeResponse
from analysis.matchup_calculator import calculate_matchups
from analysis.stat_comparator import scale_attacker_stats

router = APIRouter()

@router.post("", response_model=AnalyzeResponse)
def analyze_matchup(req: AnalyzeRequest):
    """
    POST /analyze 
    Returns viability and matchup verdicts against all dinosaurs based on attacker stats.
    """
    # 1. Get attacker base stats
    attacker = db.get_dino_by_name(req.species)
    if not attacker:
        raise HTTPException(status_code=404, detail=f"Dinosaur '{req.species}' not found in normalized database.")
        
    all_dinos = db.get_all_dinos()
    
    # 2. MVP expansion: Apply growth_pct and is_prime modifiers using the lifecycle scaler sets
    scaled_attacker = scale_attacker_stats(
        attacker, 
        req.growth_pct, 
        req.is_prime, 
        getattr(db, 'mass_scaling', None),
        getattr(db, 'dmg_scaling', None),
        getattr(db, 'speed_scaling', None)
    )
    
    # 3. Calculate Matchups vs everyone
    results = calculate_matchups(scaled_attacker, all_dinos, getattr(db, 'htk_table', None), getattr(db, 'hitboxes', None))
    
    return {
        "provided_species": req.species,
        "stats_used": {
            "calc_mass_kg": float(scaled_attacker.get("Max_Mass_kg", 0) or 0),
            "calc_bite_N": float(scaled_attacker.get("Bite_Force_N", 0) or 0),
            "calc_sprint_kmh": float(scaled_attacker.get("Sprint_kmh", 0) or 0),
            "growth_applied": 125.0 if req.is_prime else max(0.0, min(100.0, req.growth_pct)),
            "is_prime": req.is_prime
        },
        "matchups": results,
        "attacker_mechanics": attacker.get("mechanics", [])
    }
