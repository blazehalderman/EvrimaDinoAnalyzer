# agents/analysis_agent.md
# Gemini Conductor — Analysis Agent

## Role
You own the analysis engine and FastAPI backend for EvrimaDinoAnalyzer.
Your scope covers Phases 4 (analysis + API).

## Files You Own
- `analysis/matchup_calculator.py`
- `analysis/playstyle_profiler.py`
- `analysis/stat_comparator.py`
- `api/main.py`
- `api/routes/matchup.py`
- `api/routes/dinos.py`
- `api/routes/guide.py`
- `api/models/schemas.py`

## Inputs (from data/normalized/)
All analysis logic reads from normalized CSV/JSON files produced by the ETL agent.
Do not read raw source CSVs directly — always use normalized outputs.

## MVP Endpoint Contract
**POST /analyze**
- Input: `{ species, growth_pct, is_prime }`
- Output: interpolated stats + per-opponent matchup results with Engage/Caution/Flee verdicts

## Verdict Logic (to be tuned with data)
- **Engage**: you kill them in fewer hits than they need to kill you
- **Caution**: roughly equal — situational
- **Flee**: they kill you faster than you kill them

## API Conventions
- All routes return JSON.
- Use 501 Not Implemented until data is available.
- No auth required (local MVP).
- Run with: `uvicorn api.main:app --reload`
