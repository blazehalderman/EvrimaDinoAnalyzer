# etl/load/load_to_store.py
# Write normalized and derived datasets to data/normalized/ as CSV and JSON.
# SQLite query layer to be added post-MVP.

import pandas as pd
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "normalized")


def save_csv(df: pd.DataFrame, filename: str) -> str:
    """Write a DataFrame to data/normalized/<filename>.csv and return the path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    return path


def save_json(data: dict | list, filename: str) -> str:
    """Write a dict or list to data/normalized/<filename>.json and return the path."""
    import json
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


def run(normalized_df: pd.DataFrame, lifecycle_df: pd.DataFrame,
        carnivore_matrix: pd.DataFrame, herbivore_matrix: pd.DataFrame) -> None:
    """Entry point for Phase 3 load: persist all derived datasets."""
    raise NotImplementedError("Phase 3")


if __name__ == "__main__":
    run(None, None, None, None)
