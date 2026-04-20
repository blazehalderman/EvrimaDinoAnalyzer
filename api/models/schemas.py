from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    species: str
    growth_pct: float = 100.0
    is_prime: bool = False

class MatchupResult(BaseModel):
    opponent: str
    hits_to_kill_them_body: float
    hits_to_kill_them_head: float
    hits_for_them_to_kill_you_body: float
    hits_for_them_to_kill_you_head: float
    verdict: str  # Engage, Caution, Flee
    speed_advantage: str
    opponent_mechanics: list[dict] = []
    opponent_diet: str = "Unknown"
    attacker_sprint_kmh: float = 0.0
    defender_sprint_kmh: float = 0.0

class AnalyzeResponse(BaseModel):
    provided_species: str
    stats_used: dict
    matchups: list[MatchupResult]
    attacker_mechanics: list[dict] = []

class GuideResponse(BaseModel):
    species: str
    diet: str
    nest_type: str = "Unknown"
    max_eggs: int = 0
    can_eat_bones: str = "No"
    vomits_from_overeating: str = "No"
    playstyle_tips: list[str] = []
