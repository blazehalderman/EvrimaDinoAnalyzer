# api/models/schemas.py
# Pydantic input/output schemas for all API endpoints.

from pydantic import BaseModel, Field


class MatchupRequest(BaseModel):
    species: str = Field(..., description="Dinosaur species name (e.g. 'Carnotaurus')")
    growth_pct: float = Field(..., ge=1.0, le=100.0, description="Current growth percentage (1–100)")
    is_prime: bool = Field(False, description="Apply Prime specimen stat bonus (+25%)")


class OpponentResult(BaseModel):
    opponent: str
    opponent_growth_pct: float
    attacker_hits_to_kill: float
    defender_hits_to_kill: float
    verdict: str  # "Engage" | "Caution" | "Flee"


class MatchupResponse(BaseModel):
    species: str
    growth_pct: float
    is_prime: bool
    interpolated_stats: dict
    matchups: list[OpponentResult]


class DinoSummary(BaseModel):
    name: str
    diet: str
    max_mass_kg: float
    max_hp: float
    base_damage: float


class DinoDetail(DinoSummary):
    sprint_speed_kmh: float
    ambush_speed_kmh: float
    grow_time_hrs: float
    special_abilities: list[str]


class GuideResponse(BaseModel):
    species: str
    growth_profiles: list[dict]
