# etl/transform/scale_lifecycle.py
# Derive per-growth-stage stat values from the base adult stats and scaling CSVs.
# Growth stages: 25%, 50%, 75%, 100%, Prime (125%), Frail Elder (80%)

import pandas as pd

GROWTH_STAGES = [0.25, 0.50, 0.75, 1.00, 1.25, 0.80]  # 1.25 = Prime, 0.80 = Frail Elder


def interpolate_stat(base_value: float, growth_pct: float, scaling_table: pd.DataFrame) -> float:
    """Interpolate a stat value at an arbitrary growth percentage using the scaling table."""
    raise NotImplementedError("Phase 3")


def build_lifecycle_table(normalized_df: pd.DataFrame) -> pd.DataFrame:
    """Expand the normalized base stats into a full lifecycle table with one row per
    (Dinosaur, growth_stage) combination covering all stats."""
    raise NotImplementedError("Phase 3")


def run(normalized_df: pd.DataFrame) -> pd.DataFrame:
    """Entry point: return the full lifecycle DataFrame."""
    raise NotImplementedError("Phase 3")
