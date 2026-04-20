# analysis/matchup_calculator.py
# Core MVP logic: given a dinosaur, growth %, and prime status →
# return full combat viability breakdown against every other dino.
#
# User inputs:   species (str), growth_pct (float 1-100), is_prime (bool)
# System scope:  HP/stamina/food/water all at 100%, no environmental modifiers
# Output fields: interpolated stats, per-opponent hits-to-kill, verdict (Engage/Caution/Flee)

import pandas as pd
from dataclasses import dataclass


@dataclass
class MatchupResult:
    opponent: str
    opponent_growth_pct: float
    attacker_hits_to_kill: float   # how many bites you need to kill them
    defender_hits_to_kill: float   # how many bites they need to kill you
    verdict: str                   # "Engage" | "Caution" | "Flee"


def interpolate_stats(species: str, growth_pct: float, is_prime: bool,
                      lifecycle_df: pd.DataFrame) -> dict:
    """Return interpolated stats for the given species at the given growth percentage."""
    raise NotImplementedError("Phase 4")


def calculate_matchup(attacker_species: str, attacker_growth_pct: float, is_prime: bool,
                      lifecycle_df: pd.DataFrame) -> list[MatchupResult]:
    """Return a MatchupResult for every opponent species in the dataset."""
    raise NotImplementedError("Phase 4")


def assign_verdict(attacker_htk: float, defender_htk: float) -> str:
    """Classify the matchup as Engage, Caution, or Flee based on hits-to-kill ratio."""
    raise NotImplementedError("Phase 4")
