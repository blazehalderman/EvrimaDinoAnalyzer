# etl/transform/build_matchup_engine.py
# Compute matchup matrices: how many attackers of species A are needed to kill species B
# at each growth stage combination.  Produces carnivore and herbivore matrices.

import pandas as pd


def hits_to_kill(attacker_damage: float, defender_hp: float, hitbox_multiplier: float = 1.0) -> float:
    """Return the number of bites needed for attacker to kill defender."""
    effective_damage = attacker_damage * hitbox_multiplier
    if effective_damage <= 0:
        return float("inf")
    return defender_hp / effective_damage


def build_matrix(lifecycle_df: pd.DataFrame, attacker_filter: str, defender_filter: str) -> pd.DataFrame:
    """Build a hits-to-kill matrix for the given diet filter (Carnivore / Herbivore).

    Returns a DataFrame indexed by attacker species with defender species as columns.
    """
    raise NotImplementedError("Phase 3")


def run(lifecycle_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (carnivore_matrix, herbivore_matrix)."""
    raise NotImplementedError("Phase 3")
