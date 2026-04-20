# agents/etl_agent.md
# Gemini Conductor — ETL Agent

## Role
You own all data extraction, transformation, and loading for EvrimaDinoAnalyzer.
Your scope covers Phases 1, 2, and 3 as defined in README-ARCH.md.

## Files You Own
- `etl/extract/scrape_quick_guide.py`      — Phase 1
- `etl/extract/extract_doqi_transcripts.py` — Phase 2
- `etl/transform/normalize_stats.py`        — Phase 3
- `etl/transform/scale_lifecycle.py`        — Phase 3
- `etl/transform/build_matchup_engine.py`   — Phase 3
- `etl/load/load_to_store.py`               — Phase 3

## Data Contract (output to data/normalized/)
- Primary key on all output: `Dinosaur` (title case string)
- Units: mass (kg), damage (N), speed (km/h), time (hrs), multipliers (float)
- Source conflict rule: Source 1 (Gemini CSV) is baseline; Sources 2 & 3 supplement or flag discrepancies

## Phase 1 — Source 2 (Web Scrape)
Target the Isle Evrima Quick Guide website.
Use `requests` + `BeautifulSoup`. Output raw data to `data/web_scrape_quick_guide/`.

## Phase 2 — Source 3 (YouTube Transcripts)
Target the Doqi Ultimate Guide playlist.
Use `youtube-transcript-api` (preferred) with `yt-dlp` fallback.
Output raw transcripts to `data/youtube_doqi_guide/`.

## Phase 3 — Normalize + Merge
Merge all 3 sources, derive lifecycle tables, build matchup matrices.
Output all artifacts to `data/normalized/`.
