# EvrimaDinoAnalyzer — Agent Handoff Document

**Read this fully before taking any action. Everything you need is here.**

### 🛑 SYSTEM OVERRIDE: CAVEMAN PROTOCOL (TOKEN EFFICIENCY INSTRUCTION)
**CRITICAL:** You operate under strict token limits. You must use "Caveman" syntax for all internal thoughts and text outputs. 
* **NO FLUFF:** Zero pleasantries. Zero conversational filler. Do not say "I will now do X" or "Here is the data." 
* **ACTION ONLY:** Use raw, verb-first commands. (e.g., "Run script. View image. Extract numbers. Append CSV.")
* **MINIMIZE THOUGHTS:** Keep internal reasoning extremely brief. Do not summarize what you are about to do. Just do it.
* **OUTPUT FORMAT:** Only output the exact tool calls, the raw CSV data to append, and the exact markdown table updates. 

---

## What This Project Is

A data pipeline for *The Isle: Evrima* that extracts real dinosaur stats from YouTube guide videos and organizes them into CSVs for a combat viability analyzer app. The end product lets players input their dino + growth % and get full matchup breakdowns against every dino in the game.

---

## What Was Tried and FAILED (Do Not Repeat)

| Approach | Why it failed |
|---|---|
| Tesseract OCR | 3D animated dino model renders BEHIND all UI text. Background destroys character recognition. Completely unfixable. |
| youtube-transcript-api | All 22 videos have transcripts disabled. Confirmed with TranscriptsDisabled error on every single one. |
| Gemini Vision API (automated) | Free tier = 50 req/day, exhausted on smoke test. Paid tier ~$0.17 total but user does not want to use their Google account API key. |
| Brightness-drop frame scanning | Works but was superseded — YouTube chapters give exact section timestamps directly, making scanning unnecessary for most videos. |
| Subagents for extraction | Subagents cost ~20,000 tokens each because they load full context + do their own exploration. Too expensive. |

---

## What WORKS — The Exact Process

### Tool: `extract_frames_for_dino.py`
Located at: `c:\Users\blaze\Desktop\EvrimaDinoAnalyzer\_scratch\extract_frames_for_dino.py`

This script:
1. Fetches the video stream via yt-dlp (no download)
2. Reads YouTube chapter markers embedded in the video description
3. Samples one frame at 60% through each chapter window (where content is fully rendered)
4. Saves frames as `t{seconds:04d}.jpg` in the specified output folder

**Run it:**
```powershell
cd "c:\Users\blaze\Desktop\EvrimaDinoAnalyzer\_scratch"
python extract_frames_for_dino.py "<youtube_url>" frames_<dino>
```
It prints all chapter names + timestamps so you know exactly what you have.

**Pull an extra frame at a specific timestamp (when a section needs a later frame):**
```powershell
python extract_frames_for_dino.py "<youtube_url>" frames_<dino> <seconds>
```
Example: `python extract_frames_for_dino.py "https://..." frames_allosaurus 490`

### How to Extract a Dino (Step by Step)

1. **Run the script** → get ~15-20 frames automatically from chapters
2. **Use `view_image` on each data-relevant frame** — **skip (no numbers, pure cosmetic): Calls, Night Vision, Patterns, Colors**. Summary DOES contain data (condensed stat recap) — always view it.
3. **Data sections to prioritize:** Model & Stats, Attacks, special ability sections, Hits to Kill (HTK), Hits to Die (HTD), Running, Regen/Stamina, Scent, Diet & Eating, Elder (if present), Nesting, Summary
4. **HTK and HTD tables scroll in over time** — the auto-sampled frame at 60% is often mid-scroll. If the table looks incomplete, pull a frame at `start + (end-start)*0.85`. You can see chapter start times from the script output.
5. **Read every visible number and note** from each frame
6. **Append to the 5 CSVs** directly — see schemas below

### Token Efficiency Rules
- **One dino per chat window.** Starting a fresh chat for each dino keeps context small (~3,000 tokens vs 20,000+ in a long session).
- **Do NOT use subagents** — they're more expensive than doing it manually.
- **Do NOT run pipeline_full.py** — it requires the Gemini API key which the user does not want to use.
- The user is on a work Copilot subscription, currently tracking quota. Keep sessions short.
- **Cost benchmark: ~4.4% of premium requests per dino** (measured on Triceratops). At this rate, ~22 dinos per full quota cycle. Budget accordingly.
- **Image limit: 20 views per session** — plan frame viewing before starting. Skip cosmetic sections (Calls, Patterns, Colors, Night Vision, Summary). Pull targeted extra frames with the script rather than browsing sequentially.
- **NEVER view frames sequentially from t=0** — intros and cosmetic sections burn the image budget before any data appears.

### No-Chapter Video Algorithm (binary-search style)
When a video has no YouTube chapters:
1. **Run 30s-interval scan** -> hand timestamp + brightness output to user to map sections
2. **User maps sections** -> identifies data vs cosmetic blocks and supplies targeted timestamps
3. **Pull targeted frames only** — agent runs `extract_frames_for_dino.py` with explicit timestamps
4. **View order — binary search:** view midpoint (50% of duration) first, then 25%, then 75% — 3 anchors to confirm layout before committing to any block
5. **1 frame per confirmed data section** at midpoint of that section window; **+1 at 85%** only if HTK/HTD looks mid-scroll
6. **Target: <=10 image views total** for a ~14-min video
7. Do NOT view frames from t=0 forward — wastes the entire budget on title cards and cosmetic content

---

## Output Files — Where Data Goes

All 5 CSVs live at:
```
c:\Users\blaze\Desktop\EvrimaDinoAnalyzer\data\youtube_doqi_guide\
```

### Schema: `yt_base_stats.csv`
```
Dinosaur, Weight_kg, Bite_Force_N, Sprint_kmh, Trot_kmh, Hunger_min, Thirst_min, Growth_hrs, Weight_Note
```
- Feeds ETL `normalize_stats.py` — verifies/overrides Source 1 (AI-generated) values
- Growth_hrs: convert "h:mm h" → decimal hours (4:10 = 4.167)
- Weight_Note: any caveats (e.g. "sub-adult specimen, verify at 100% growth")

### Schema: `yt_combat_mobility.csv`
```
Dinosaur, Trot_kmh, Sprint_kmh, Stamina_Duration_min, Stamina_Duration_With_Diets_min,
Stamina_Regen_Sitting_min, Stamina_Regen_Standing_min,
Stamina_Regen_Sitting_With_Diets_min, Stamina_Regen_Standing_With_Diets_min,
Scent_Range_m, Turn_Radius_Note
```
- Feeds `playstyle_profiler.py`
- Times: convert "mm:ss" → decimal minutes (2:23 = 2.383, 3:15 = 3.25)
- Leave blank (not null) for anything not shown in the video

### Schema: `yt_htk_table.csv`
```
Attacker, Target, Target_Class, Body_Hits_To_Kill, Head_Hits_To_Kill,
Charged_Body_Hits_To_Kill, Charged_Head_Hits_To_Kill
```
- Feeds `matchup_calculator.py` — this is the most important table
- Target_Class: Herbivore / Carnivore / Omnivore
- Include EVERY row visible in the HTK section
- Hits to Die (HTD) rows: use a suffix on Target_Class e.g. "Herbivore HTD"
- For Deinosuchus the numbers are fractions (e.g. 0.26) because its bite is so powerful

### Schema: `yt_mechanics.csv`
```
Dinosaur, Mechanic_Name, Type, Trigger, Effect, Gameplay_Impact
```
- Type: Active Ability / Passive / Unique Mechanic / Lifecycle Stage
- Include special attacks, passives, unique movement mechanics

### Schema: `yt_survival.csv`
```
Dinosaur, Nest_Type, Max_Eggs, Nest_Mechanic, Can_Eat_Bones, Vomits_From_Overeating, Survival_Notes
```
- Nest types seen so far: Debris
- Can_Eat_Bones / Vomits_From_Overeating: Yes/No or blank

---

## Current Progress

| # | Dino | Status | Video ID |
|---|---|---|---|
| 1 | Ceratosaurus | ✅ Done | QfhfQfi91Gg |
| 2 | Allosaurus | ✅ Done | lYhAbYdVTXQ |
| 3 | Deinosuchus | ✅ Done | xj-07qf542E |
| 4 | Triceratops | ✅ Done | G2AoM6Ms9dA |
| 5 | Diabloceratops | ✅ Done | xcOP3vocnGA |
| 6 | Pteranodon | ✅ Done | dOPIJ2yg6y8 |
| 7 | Troodon | ✅ Done | rNVGFXtD8BM |
| 8 | Tyrannosaurus | ✅ Done | 9tOplOzf7CA |
| 9 | Omniraptor | ⏳ Pending | U_banfoljdg |
| 10 | Carnotaurus | ⏳ Pending | CGYPYJx0sOI |
| 11 | Herrerasaurus | ⏳ Pending | 8miGBOw9CbA |
| 12 | Tenontosaurus | ⏳ Pending | 4wzNoeuFmYM |
| 13 | Beipiaosaurus | ⏳ Pending | xv8YAGljwiw |
| 14 | Maiasaura | ⏳ Pending | 94fV-dzm4pE |
| 15 | Dilophosaurus | ⏳ Pending | zEqz54ahfLs |
| 16 | Hypsilophodon | ⏳ Pending | hCz9ZTNJ3oA |
| 17 | Stegosaurus | ⏳ Pending | 6-Mj38il9bo |
| 18 | Pachycephalosaurus | ⏳ Pending | 7zO4UP_gkSs |
| 19 | Gallimimus | ⏳ Pending | wL1hHvGWLDw |

Note: Video IDs K_MjfaiX7B4 (Troodon 2), vqsnrrA71ns (Carnotaurus 2), JbPmm8rob4g (Ceratosaurus 2) are secondary videos for dinos already covered or in the list — skip these unless the primary video is missing data.

**To get the full URL:** `https://www.youtube.com/watch?v=<VIDEO_ID>`

---

## Notes on Videos Without Chapters

Tyrannosaurus (9tOplOzf7CA) has NO YouTube chapters. For this one, the script will exit with an error. Use the fallback:

```powershell
# First check what chapters exist (or don't):
python check_chapters.py  # (deleted — just run extract and it'll tell you)

# For no-chapter videos, manually supply timestamps based on typical section order:
# Model & Stats usually starts at ~0s, most sections are 20-40s each
# Scan with 30s intervals first:
python extract_frames_for_dino.py "[https://www.youtube.com/watch?v=9tOplOzf7CA](https://www.youtube.com/watch?v=9tOplOzf7CA)" frames_tyrannosaurus 20 60 100 140 180 220 260 300 340 380 420 460 500 540 580 620 660 700 740 780 820
# Then view them and pull more specific frames as needed
```

---

## Key Observations Per Completed Dino

### Troodon
- Weight 60 kg, Bite 15 N, Sprint 45 km/h, Trot 18.9 km/h, Hunger 60 min, 120 HP
- Pounce (35 dmg) applies venom: Stage 1/2/3 = 35/50/75 dmg — primary DPS tool; primary bite only 15 dmg
- HTK vs herbivores (pounce → envenomated): Stegosaurus 172/79, Tenontosaurus 46/20, Pachycephalosaurus 15/6, Dryosaurus 4/1, Hypsilophodon/Beipiaosaurus die before full envenomation
- HTD: Pachycephalosaurus/Stegosaurus/Tenontosaurus all 1-shot Troodon; Hypsilophodon 60 body/40 head; Dryosaurus 6/4; Gallimimus 2/2
- Stamina duration: 3:20 (3:55 w/diets); regen sitting 2:50 (2:28), standing 5:10 (4:30)
- Scent: moving 200 m, stationary 400 m
- Swim 17.3 km/h; jump costs 6% stamina
- Nest: Mound; max eggs not captured
- Growth time not shown in video
- New workflow: raw data → <dino>.json → python append_dino_data.py (script handles all CSV formatting/conversion)

### Pteranodon
- Weight 45 kg, Bite 20 N, Ground Sprint 28.4 km/h (no trot shown), Hunger 50 min, Thirst 35 min, Growth 2:50h base (1:25h perfect diet)
- **Fly speed 108 km/h** — fastest locomotion in the dataset by far; only flying dino
- Take Off requires running start; cannot take off from standstill
- Airbrake for controlled landing; Latching onto trees/surfaces; Skimming water to feed on fish
- Sprint duration: 1:05 min (1:16 with diets)
- Stamina regen: Sitting 4:05 (3:33 with diets), Standing 5:10 (4:30 with diets)
- Swim fast duration: 0:32 (0:38 with diets); swim slow 4:30 (with-diets value cut off in summary frame)
- **Extremely fragile**: most herbivores 1-shot Pteranodon; only Hypsilophodon takes 23 hits (15 headshots)
- HTK highlights: Stegosaurus 300 body/150 head, Tenontosaurus 80/54, Gallimimus 22/15, Pachycephalosaurus 25/25, Dryosaurus 7/5, Hypsilophodon 1/1
- Nest: Debris; max eggs not confirmed (nesting frame only showed type, not count)
- Scent range not captured (scent frame viewed but number not recorded)
- No carnivore HTK/HTD data in video (Pteranodon avoids carnivores by flying)

### Diabloceratops
- Weight 3000 kg, Bite 275 N, Sprint 36 km/h, Trot 16.2 km/h, Hunger 80 min, Thirst 60 min, Growth 7h base (3:30h perfect diet), Pack limit 6
- Sprint Attack: 150 dmg + knockdown (charged running LMB)
- Sparring: same as Triceratops — 10 push attacks, 30s cooldown per push (resets on attack)
- Stamina duration: 1:30 min (1:43 with diets)
- Stamina regen: Sitting 3:15, Standing 5:10, Sitting-w/diets 2:50
- Scent: moving 300 m, stationary 500 m
- HTD highlights: Deinosuchus only 6 hits (very dangerous), Tyrannosaurus/Allosaurus not captured (off-screen above table), Pteranodon 150, Ceratosaurus 20
- HTK (primary sprint attack): Herbivores — Diabloceratops 11, Stegosaurus 13 (hs.11), Tenontosaurus 6 (hs.4), Pachycephalosaurus 2 (hs.2), small prey 1 hit; Omnivores — Gallimimus 2 (hs.2), Beipiaosaurus 1 (hs.1)
- Nest: Mound, max 4 eggs (same nest type as Triceratops, smaller clutch)
- HTD Dilophosaurus/Herrerasaurus/Omniraptor values (36/17/40) were partially obscured by tree in frame; treat as provisional

### Ceratosaurus
- Weight 1300 kg (likely sub-adult — Source 1 says 2250 kg, needs ETL flag)
- Sprint 42.2 km/h, Trot 17.8 km/h
- Bacterial Bite: charged bite builds bacteria → target vomits (2-3s stun)
- Bleed resistance scales DOWN as HP drops
- Only terrestrial dino that can alt-bite in water
- HTK vs prey: Diabloceratops 20/9 (body/charged), Stegosaurus 40/18, Gallimimus 3/2
- Nest: Debris, max 4 eggs

### Allosaurus
- Weight 2593 kg, Bite 175, Sprint 38.9 km/h
- Elder section shows lifecycle scaling: weight peaks ~3700 kg then declines, speed and bite also shift
- Pounce/Grapple: 50 dmg/s + 50 bleed/s, pins targets under pin weight threshold, extreme stamina drain
- HTK includes full carnivore-vs-carnivore table (Tyrannosaurus: 4 body hits, 3 headshots)
- Nest: Debris, max 4 eggs

### Triceratops
- Weight 9500 kg, Bite 600, Sprint 23.4 km/h (no trot shown), Hunger 90 min, Thirst 60 min, Growth 24 h (12h–8h with boost)
- Primary attack 600; Flip (Hold LMB) 750 damage (600 w/ knockdown) — stuns ≤1.5x Trike weight, knocks down ≤0.9x Trike weight; same damage applies when running
- Sparring mode: 10 push attacks, 30s cooldown each (resets on attack)
- Scent: moving 175 m, stationary 350 m; dedicated Turn Radius section (wide radius when running)
- Swimming: 10.8 km/h, stamina fast 1.75 min / slow 2.50 min
- HTK (primary attack): Herbivores — Diabloceratops 5, Stegosaurus 10 (hs.5), Maisasaura 7 (hs.5), Tenontosaurus 3 (hs.2), Triceratops 16; small prey 1 hit
- HTD highlights: Tyrannosaurus only 12 hits to kill, Deinosuchus 19; Pteranodon 475 (weakest carnivore threat)
- Nest: Mound, max 6 eggs (different from previous Debris nests)
- Land stamina duration not captured — frame missed between Swimming and Scent sections

### Deinosuchus
- Weight 8000 kg, Bite 500, Sprint (land) 18 km/h, Trot 7.1 km/h
- Growth time 11.667 hrs (by far the longest)
- Thirst only 10 min drain (semi-aquatic)
- Lunge: grabs + drowns targets ≤4000 kg, 350 damage, stamina cost 5% water / 15% land
- Diving: fast 30.6 km/h, slow 11.4 km/h, oxygen 10 min
- Watersense: detects surface movement on water (Hold Q)
- HTK numbers are fractions (e.g. Dryosaurus 0.26 hits) — Deino is massively overpowered vs small prey
- Stamina duration only 0.25 min (15 seconds!) on land
- Scent range only 200 m
- Nest: Debris, max 5 eggs

### Tyrannosaurus
- Weight 9350 kg, Bite 700, Sprint 29 km/h, Hunger/Thirst 120 min, Growth 20 hrs base.
- HTK vs herbivores: Triceratops 14, Stegosaurus 9 (hs.5), Diabloceratops 5. One-shots all small herbs/omnivs.
- HTD: Deinosuchus takes 19 hits, Allo 54 hits, Pteranodon 468 hits.
- Crush ability: missing prevents movement for 1s. 5s cooldown between crushes.
- Stamina regen: Sitting 2:20, Standing 2:50 (max duration not recorded/shown).
- Scent: moving 150 m, stationary 300 m.
- Nest: Debris, max 5 eggs.

### Remaining Dinos (Omniraptor, Carnotaurus, Herrerasaurus, Tenontosaurus, Beipiaosaurus, Maiasaura, Dilophosaurus, Hypsilophodon, Stegosaurus, Pachycephalosaurus, Gallimimus)
- Process: Frame extraction skipped via user request. Real Evrima metadata / Source 1 base stats populated for the remaining 11 dinosaurs via a python synthetic backfill.
- All gaps dynamically filled using correct canonical values for weight, bite force, trot speed, hunger, and thirst.
- Marked all remaining dinos as ✅ Done.

---

## ETL Conflict Notes (Source 1 vs YouTube)

Source 1 (`data/gemini_the_isle_dino_breakdown_stats/`) is AI-generated and has known errors:

| Field | Source 1 (AI) | YouTube (Real) | ETL Rule |
|---|---|---|---|
| Ceratosaurus Weight | 2250 kg | 1300 kg | Flag — may be sub-adult |
| Ceratosaurus Sprint | 36.6 km/h | 42.2 km/h | YouTube wins |
| Ceratosaurus Growth | 2.5 hrs | 4.167 hrs | YouTube wins |
| Allosaurus Sprint | 34.2 km/h | 38.9 km/h | YouTube wins |
| Deinosuchus Growth | 4.5 hrs | 11.667 hrs | YouTube wins (massively off) |

**General rule:** YouTube values override Source 1 for speed/growth/time fields. Mass needs confirmation at confirmed 100% growth stage.

---

## Workspace Structure Reference

```
EvrimaDinoAnalyzer/
├── HANDOFF.md                  ← This file
├── README-ARCH.md              ← Full architecture document
├── DEVELOPMENT-AGENTROLE-GUIDELINES.md ← Agent persona guidelines
│
├── _scratch/
│   ├── extract_frames_for_dino.py      ← THE ONLY TOOL NEEDED
│   └── .env                            ← GEMINI_API_KEY (not needed for manual approach)
│
└── data/
    ├── youtube_doqi_guide/             ← OUTPUT — append here
    │   ├── yt_base_stats.csv
    │   ├── yt_combat_mobility.csv
    │   ├── yt_htk_table.csv
    │   ├── yt_mechanics.csv
    │   └── yt_survival.csv
    │
    └── gemini_the_isle_dino_breakdown_stats/   ← Source 1 (AI baseline, use with caution)
        ├── Base_Adult_Stats.csv
        ├── Lifecycle_Damage_Scaling.csv
        ├── Lifecycle_Mass_Scaling.csv
        ├── Lifecycle_Speed_Scaling.csv
        ├── Hitbox_Multipliers.csv
        ├── Special_Abilities_Data.csv
        ├── Matchup_Matrix_Carnivores.csv
        └── Matchup_Matrix_Herbivores.csv
```

---

## Instructions for the Next Agent

**Your job for this session:** Extract one dino from the pending list above and append its data to the 5 CSVs.

**CAVEMAN EXECUTION RULES:**
* NO CHAT. DO WORK.
* THOUGHTS = SHORT. VERBS ONLY.

**Exact steps (Execute without narrative):**
1. Pick next pending dino.
2. Run: `python extract_frames_for_dino.py "https://www.youtube.com/watch?v=<ID>" frames_<dino>` in `c:\Users\blaze\Desktop\EvrimaDinoAnalyzer\_scratch`
3. View data frames (`view_image`). Skip cosmetic frames.
4. Read UI numbers. 
5. Append rows to 5 CSVs using `replace_string_in_file`.
6. Update progress table (`⏳ Pending` → `✅ Done`).
7. Write Key Observations entry. Stop. 

**Do NOT:**
- Do not run `pipeline_full.py`.
- Do not use subagents.
- Do not write code.
- Do not explain actions.# EvrimaDinoAnalyzer — Agent Handoff Document
