# analysis/playstyle_profiler.py
# Growth-stage behavior recommendations per dinosaur.
# Combines lifecycle stats with Doqi guide commentary (Source 3) to produce
# actionable play advice at each growth stage.

import pandas as pd


def get_stage_profile(species: str, growth_pct: float,
                      lifecycle_df: pd.DataFrame, guide_df: pd.DataFrame) -> dict:
    """Return a playstyle profile dict for the given species and growth stage.

    Expected keys: safe_prey, threats, recommended_behavior, food_priority, notes
    """
    raise NotImplementedError("Phase 4 — requires Source 3 data")


def build_full_profile(species: str,
                       lifecycle_df: pd.DataFrame,
                       guide_df: pd.DataFrame) -> list[dict]:
    """Return profiles for all growth stages (25, 50, 75, 100, Prime, Frail Elder)."""
    raise NotImplementedError("Phase 4")
