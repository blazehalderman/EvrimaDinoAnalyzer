# EvrimaDinoAnalyzer — Architectural Overview v1.0

> **Scope:** Architecture and project structure decisions only. This document is the single source of truth for how the project is organized, how data flows, and what gets built in what order. Feature implementation details live in agent-specific prompt files managed by Gemini Conductor.

---

## Toolchain

| Tool | Role |
|---|---|
| **Gemini CLI** | Primary AI reasoning engine — data investigation, feature derivation, prompt generation, analysis logic |
| **Gemini Conductor** | Multi-agent orchestration — routes tasks to specialized agents (ETL, analysis, frontend, docs), manages prompt files and instruction sets |
| **VS Code** | IDE host |

---

## Project Purpose

**EvrimaDinoAnalyzer** is a data-driven tool for *The Isle: Evrima* that aggregates dinosaur stats from three independent sources, normalizes them into a unified model, and provides players with:

- Combined raw stat breakdowns per dinosaur
- Play guides and growth-stage expectations
- Matchup matrices (attacker vs defender, at each growth %)
- An interactive MVP tool: input your dino + growth % + prime/frail status → get a full combat viability breakdown against every dino in the game

---

## Data Sources (3 Total — 1 Collected, 2 Pending)

### Source 1 — Gemini Investigative Dataset ✅ Collected
**Location:** `data/gemini_the_isle_dino_breakdown_stats/`

| File | Contents |
|---|---|
| `Base_Adult_Stats.csv` | Diet, max mass/HP, base attack, sprint/ambush speed, grow time, food/water drain |
| `Lifecycle_Damage_Scaling.csv` | Damage at 25%, 50%, 75%, 100%, Prime (125%), Frail Elder (80%) growth |
| `Lifecycle_Mass_Scaling.csv` | Mass scaling across growth stages |
| `Lifecycle_Speed_Scaling.csv` | Speed scaling across growth stages |
| `Hitbox_Multipliers.csv` | Head (2.6x), Body (1.0x), Tail (0.13x) damage zones |
| `Special_Abilities_Data.csv` | Ability name, special damage, modifier effects, thresholds, penalties |
| `Matchup_Matrix_Carnivores.csv` | Numbers-needed-to-kill matrix (carnivore attackers vs carnivore defenders) |
| `Matchup_Matrix_Herbivores.csv` | Numbers-needed-to-kill matrix (carnivore attackers vs herbivore defenders) |

### Source 2 — The Isle Evrima Quick Guide (Web Scrape) ⏳ Pending
**Target:** The Isle Evrima Quick Guide website
**Method:** Python web scraping (`requests` + `BeautifulSoup`)
**Expected data:** Official/community-verified stat entries, mechanic descriptions, ability tooltips, growth notes
**Output target:** `data/web_scrape_quick_guide/`

### Source 3 — Doqi Ultimate Guide YouTube Playlist 🔄 In Progress (1/22 dinos)
**Target:** Doqi — Ultimate Guide — The Isle Evrima (YouTube playlist)
**Method:** Frame extraction (yt-dlp + opencv) → brightness-drop section boundary detection → direct agent vision reading
**Extraction approach:** Save frames every 8s → find frames immediately before brightness drops (section ends) → read stats directly from those frames
**Output target:** `data/youtube_doqi_guide/`

| File | Contents |
|---|---|
| `yt_base_stats.csv` | Verified in-game weight, bite force, sprint/trot speed, hunger/thirst/growth times |
| `yt_combat_mobility.csv` | Trot/sprint speed, stamina duration, stamina regen (sitting/standing), scent range |
| `yt_htk_table.csv` | Hits-to-kill matrix: Attacker vs Target, body hits, headshots, charged variants |
| `yt_mechanics.csv` | Special abilities, passives, triggers, effects — qualitative + structured |
| `yt_survival.csv` | Nest type, max eggs, diet flags, survival notes |

**⚠️ Known ETL Conflicts with Source 1 (Ceratosaurus verified):**
- `Weight_kg`: YouTube=1300 vs Source1=2250 — YouTube specimen may be sub-adult; flag for ETL
- `Sprint_kmh`: YouTube=42.2 vs Source1=36.6 — YouTube value is from dedicated Running section; likely more accurate
- `Growth_hrs`: YouTube=4.167 vs Source1=2.5 — Source 1 is AI-generated and likely wrong
- **Conflict resolution rule:** Source 3 YouTube values override Source 1 for speed/growth/time fields; Source 1 mass values held pending confirmation at 100% growth stage

---

## Project Structure

```
EvrimaDinoAnalyzer/
│
├── README-ARCH.md                  ← This file (architecture authority)
│
├── data/
│   ├── gemini_the_isle_dino_breakdown_stats/   ← Source 1 (collected)
│   ├── web_scrape_quick_guide/                 ← Source 2 (pending)
│   ├── youtube_doqi_guide/                     ← Source 3 (in progress — 1/22 dinos)
│   └── normalized/                             ← Post-ETL unified dataset
│
├── etl/
│   ├── extract/
│   │   ├── scrape_quick_guide.py               ← Source 2 extractor
│   │   └── extract_doqi_transcripts.py         ← Source 3 extractor
│   ├── transform/
│   │   ├── normalize_stats.py                  ← Merge + normalize all 3 sources
│   │   ├── scale_lifecycle.py                  ← Derive per-growth-% stat values
│   │   └── build_matchup_engine.py             ← Compute matchup matrices
│   └── load/
│       └── load_to_store.py                    ← Write normalized output (CSV/JSON/DB)
│
├── analysis/
│   ├── matchup_calculator.py                   ← Core MVP logic: input → matchup result
│   ├── playstyle_profiler.py                   ← Growth-stage behavior recommendations
│   └── stat_comparator.py                      ← Cross-dino stat comparison utilities
│
├── api/
│   ├── main.py                                 ← FastAPI app entry point
│   ├── routes/
│   │   ├── matchup.py                          ← POST /analyze — MVP endpoint
│   │   ├── dinos.py                            ← GET /dinos, GET /dinos/{name}
│   │   └── guide.py                            ← GET /guide/{dino} — play guide
│   └── models/
│       └── schemas.py                          ← Pydantic input/output schemas
│
├── frontend/
│   ├── index.html                              ← MVP UI entry point
│   ├── app.js                                  ← Form handling + API calls
│   └── styles.css
│
├── agents/                                     ← Gemini Conductor agent prompt files
│   ├── etl_agent.md
│   ├── analysis_agent.md
│   ├── frontend_agent.md
│   └── orchestrator.md
│
└── requirements.txt
```

---

## ETL Architecture

```
[Source 1: CSV Files]  ──┐
[Source 2: Web Scrape] ──┼──► Extract ──► Transform (normalize + scale) ──► Load ──► data/normalized/
[Source 3: YT Transcripts] ─┘
```

### Transform Rules
- **Primary key:** `Dinosaur` (species name, normalized to title case)
- **Growth stages:** 25%, 50%, 75%, 100%, Prime (125%), Frail Elder (80%) — all stats derived at each stage
- **Conflict resolution:** Source 1 (Gemini) is the baseline; Sources 2 and 3 supplement or flag discrepancies
- **Normalization targets:** mass (kg), damage (N), speed (km/h), time (hrs/min), multipliers (float)

---

## MVP Feature — Combat Viability Analyzer

**User inputs:**
- Dinosaur species
- Current growth percentage (1–100%)
- Prime specimen: yes/no

**System assumptions (MVP scope):**
- Health, stamina, food, water all at 100% (normal)
- No environmental modifiers

**Output:**
- Interpolated stats for the given growth % (mass, HP, damage, speed)
- For every other dino in the game:
  - Can you kill it 1v1? How many of you does it take?
  - What growth % of that dino is safe to engage vs avoid?
  - Verdict: Engage / Caution / Flee
- Prime modifier applied to all damage/stat values if selected

---

## Feature Roadmap (Post-MVP, Data-Dependent)

Features to be defined by Gemini Conductor agents once all 3 datasets are collected and normalized:

1. **Full play guide per dino** — growth timeline, food routes, threat awareness by stage
2. **Pack/herd matchup matrices** — group vs group combat scenarios
3. **Ambush vs sprint engagement calculator** — using speed differentials
4. **Special ability impact layer** — integrate hitbox, bacteria, pin, drown mechanics into matchup results
5. **Cross-dino growth comparison** — who grows fastest, most dangerous at 50%, etc.
6. **Doqi insight overlay** — expert commentary attached to data-driven outputs

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data / ETL | Python (`pandas`, `requests`, `BeautifulSoup`, `yt-dlp` or `youtube-transcript-api`) |
| Analysis engine | Python (`numpy`, `pandas`) |
| Backend API | Python — FastAPI |
| Frontend (local MVP) | Vanilla HTML/CSS/JS |
| AI orchestration | Gemini CLI + Gemini Conductor |
| Data storage (local) | CSV / JSON flat files → SQLite for query layer later |

---

## Development Phases

| Phase | Goal | Status |
|---|---|---|
| **Phase 0** | Project structure, architecture definition | ✅ Complete |
| **Phase 1** | ETL — Source 2 scraper (Quick Guide) | 🗑️ Scrapped |
| **Phase 2** | ETL — Source 3 transcript extractor (Doqi) | ✅ Complete |
| **Phase 3** | Normalize + merge all 3 sources | ✅ Complete |
| **Phase 4** | MVP analysis engine + FastAPI backend | ✅ Complete |
| **Phase 5** | MVP frontend UI | ✅ Complete |
| **Phase 6** | Feature expansion (guided by data + Conductor) | ⏳ In Progress |

---

## Gemini Conductor Orchestration Notes

- Each `agents/` file defines the scope and instructions for a specialized agent
- The `orchestrator.md` agent is the entry point — it reads this README-ARCH.md as context before delegating
- No agent makes architectural decisions — they reference this document and escalate structural changes back to this prompt
- Gemini CLI handles all data investigation, transcript parsing, and analysis reasoning tasks
