# etl/transform/normalize_stats.py
# Merge and normalize all 3 data sources into a unified dinosaur stat model.
# Primary key: Dinosaur (species name, title case)
# Conflict resolution: Source 1 (Gemini CSV) is the baseline; Sources 2 & 3 supplement.
# Normalization targets: mass (kg), damage (N), speed (km/h), time (hrs/min), multipliers (float)

import pandas as pd
import os

SOURCE1_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "gemini_the_isle_dino_breakdown_stats")
SOURCE2_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "web_scrape_quick_guide")
SOURCE3_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "youtube_doqi_guide")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "..", "data", "normalized")


def load_source1() -> pd.DataFrame:
    """Load and merge all Gemini CSVs into a single DataFrame keyed on Dinosaur."""
    raise NotImplementedError("Phase 3")


def load_source2() -> pd.DataFrame:
    """Load web-scraped Quick Guide data into a DataFrame keyed on Dinosaur."""
    raise NotImplementedError("Phase 3")


def load_source3() -> pd.DataFrame:
    """Load parsed Doqi transcript data into a DataFrame keyed on Dinosaur."""
    raise NotImplementedError("Phase 3")


def merge_sources(s1: pd.DataFrame, s2: pd.DataFrame, s3: pd.DataFrame) -> pd.DataFrame:
    """Outer-join all three sources on Dinosaur; log conflicts for review."""
    raise NotImplementedError("Phase 3")


def run() -> pd.DataFrame:
    """Entry point for Phase 3 transform: produce the unified normalized dataset."""
    raise NotImplementedError("Phase 3")


if __name__ == "__main__":
    run()
