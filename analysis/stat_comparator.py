# analysis/stat_comparator.py
# Cross-dinosaur stat comparison utilities.
# Supports ranking, filtering, and head-to-head comparisons across the normalized dataset.

import pandas as pd


def rank_by_stat(normalized_df: pd.DataFrame, stat_column: str,
                 ascending: bool = False) -> pd.DataFrame:
    """Return the dataset sorted by the given stat column."""
    return normalized_df.sort_values(stat_column, ascending=ascending).reset_index(drop=True)


def head_to_head(species_a: str, species_b: str,
                 normalized_df: pd.DataFrame) -> dict:
    """Return a side-by-side stat comparison between two species."""
    raise NotImplementedError("Phase 4")


def top_n(normalized_df: pd.DataFrame, stat_column: str, n: int = 5) -> pd.DataFrame:
    """Return the top N dinosaurs for a given stat."""
    return rank_by_stat(normalized_df, stat_column).head(n)


def filter_by_diet(normalized_df: pd.DataFrame, diet: str) -> pd.DataFrame:
    """Filter the dataset to Carnivore or Herbivore entries."""
    return normalized_df[normalized_df["Diet"].str.lower() == diet.lower()].copy()
