# EvrimaDinoAnalyzer MVP 

## Current Progress (MVP Status)
The foundation of the EvrimaDinoAnalyzer is complete and functional, focusing strictly on data from *The Isle: Evrima*. 

### Completed Features
- **Data Normalization Pipeline:** ETL processes that parse, clean, and normalize disparate CSV data (HTK tables, hitboxes, stats, lifecycle scaling) into a cohesive backend database.
- **Matchup Calculator:** An algorithm that calculates combat viability (Engage, Caution, Flee) taking into account weight ratios, bite force, and mechanic-specific lethality modifiers (`M_SCORES`).
- **Verified TTK Integration:** Prioritizes verified Hits-to-Kill (HTK) data for 100% adults when available, falling back on mathematical interpolation for dynamically scaled targets.
- **Dynamic Attacker Scaling:** Integrates lifecycle percentage scaling (1-100%) and "Prime Elder" status to interpolate Mass, Damage (Bite Force), and Velocity (Sprint/Trot/Ambush).
- **Interactive UI Dashboard:** A vanilla JS frontend that fetches normalized data via FastAPI, populates matchup tables, highlights speed advantages, and features hoverable tooltips for Special Abilities/Mechanics.
- **Playstyle Guides:** Dynamically injects survival and hunting tips based on the selected dinosaur's traits.

---

## Next Objectives & Roadmap
Based on the solid MVP foundation, the following features are planned to turn this into a tier-one community tool.

### 1. Variable Opponent Growth 
*The "Can I take them?" feature.*
- **Goal:** Allow the user to scale the defender's stats alongside the attacker's.
- **Implementation:** Add an "Opponent Growth %" global slider or column-specific dropdowns to dynamically calculate matchups between two non-adult dinosaurs.

### 2. Status Effect & Stamina Simulation
*Hit-and-Run vs. Face-Tanking.*
- **Goal:** Move beyond flat lethality modifiers by mathematically simulating damage-over-time (Bleed, Bacteria, Venom) and stamina economy.
- **Implementation:** Integrate new datasets for Coagulation Rates, Stamina Pools, and Venom drain to project realistic "Time-To-Kill" instead of just raw "Hits-To-Kill".

### 3. Agility & Turn Radius Metrics
*The maneuverability advantage.*
- **Goal:** Factor in turn-radius ("Alt-Turn") into the Chase/Escape calculations.
- **Implementation:** Scrape and integrate turning radius degrees-per-second, allowing the tool to flag matchups where a slower dinosaur can still win by out-turning its opponent (e.g., Carno vs. Omniraptor).

### 4. Pack vs. Herd Matchups (1vX)
*Accounting for numbers.*
- **Goal:** Allow calculations for group combat scenarios.
- **Implementation:** Add a "Pack Size" counter that proportionally divides the "Hits for them to kill you" and multiplies attacker DPS, simulating realistic pack hunting dynamics (e.g., 3 Troodons vs 1 Stegosaurus).

### 5. UI Quality-of-Life Upgrades
*Polishing the user experience.*
- **Interactive Sorting:** Let users click table headers to sort matchups by "Speed", "Hits to Kill", or "Diet".
- **Visual Assets:** Scrape the wiki for official dinosaur portraits/icons to display alongside their names in the table for quicker visual parsing.