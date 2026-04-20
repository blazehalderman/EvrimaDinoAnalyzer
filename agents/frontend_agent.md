# agents/frontend_agent.md
# Gemini Conductor — Frontend Agent

## Role
You own the MVP frontend UI for EvrimaDinoAnalyzer.
Your scope covers Phase 5.

## Files You Own
- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

## Tech Stack
Vanilla HTML/CSS/JS — no frameworks, no build step.
Open `frontend/index.html` directly in a browser or serve with a simple static server.

## API Integration
The frontend calls the FastAPI backend at `http://localhost:8000`.
- `GET  /dinos`       → populate species dropdown
- `POST /analyze`     → submit matchup request, render results table

## UX Requirements (MVP)
1. Species selector (populated from API)
2. Growth % input (1–100)
3. Prime toggle
4. Submit → results table with Engage/Caution/Flee colour coding

## Design Notes
- Dark theme (matching game aesthetic)
- Verdict colours: Engage = green, Caution = yellow, Flee = red
- Mobile responsive is a post-MVP concern
