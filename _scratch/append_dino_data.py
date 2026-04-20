"""
append_dino_data.py
Usage: python append_dino_data.py <dino.json>

Reads structured raw JSON and appends to all 5 CSVs.
All time conversions (mm:ss -> decimal min, h:mm -> decimal hrs) handled here.
Nulls become empty strings. Script never filters or judges data value.
"""
import json, csv, sys, os, re

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'youtube_doqi_guide')

def mmss_to_min(s):
    """'3:20' -> 3.333  |  already-float passthrough  |  None/'' -> ''"""
    if s is None or s == '': return ''
    m = re.match(r'^(\d+):(\d{2})$', str(s).strip())
    if m:
        return round(int(m.group(1)) + int(m.group(2)) / 60, 3)
    return s  # already numeric or annotated string

def hhmm_to_hrs(s):
    """'2:30' -> 2.5  |  '4:10' -> 4.167  |  already-float passthrough  |  None/'' -> ''"""
    if s is None or s == '': return ''
    m = re.match(r'^(\d+):(\d{2})$', str(s).strip())
    if m:
        return round(int(m.group(1)) + int(m.group(2)) / 60, 3)
    return s

def v(x):
    return '' if x is None else x

def append_row(filename, row, fieldnames):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        csv.DictWriter(f, fieldnames=fieldnames).writerow(row)

if len(sys.argv) < 2:
    print("Usage: python append_dino_data.py <dino.json>")
    sys.exit(1)

with open(sys.argv[1], encoding='utf-8') as f:
    d = json.load(f)

dino = d['dinosaur']
print(f"Appending {dino} to all 5 CSVs...")

# ── yt_base_stats.csv ─────────────────────────────────────────────────────────
bs = d.get('base_stats', {})
growth_raw = bs.get('growth_hrs_raw')
growth_val = hhmm_to_hrs(growth_raw) if growth_raw else v(bs.get('growth_hrs'))
append_row('yt_base_stats.csv', {
    'Dinosaur':    dino,
    'Weight_kg':   v(bs.get('weight_kg')),
    'Bite_Force_N':v(bs.get('bite_force_n')),
    'Sprint_kmh':  v(bs.get('sprint_kmh')),
    'Trot_kmh':    v(bs.get('trot_kmh')),
    'Hunger_min':  v(bs.get('hunger_min')),
    'Thirst_min':  v(bs.get('thirst_min')),
    'Growth_hrs':  growth_val,
    'Weight_Note': v(bs.get('weight_note')),
}, ['Dinosaur','Weight_kg','Bite_Force_N','Sprint_kmh','Trot_kmh',
    'Hunger_min','Thirst_min','Growth_hrs','Weight_Note'])

# ── yt_combat_mobility.csv ────────────────────────────────────────────────────
cm = d.get('combat_mobility', {})
append_row('yt_combat_mobility.csv', {
    'Dinosaur':                              dino,
    'Trot_kmh':                              v(cm.get('trot_kmh', bs.get('trot_kmh'))),
    'Sprint_kmh':                            v(cm.get('sprint_kmh', bs.get('sprint_kmh'))),
    'Stamina_Duration_min':                  mmss_to_min(cm.get('stamina_duration_mmss')),
    'Stamina_Duration_With_Diets_min':       mmss_to_min(cm.get('stamina_duration_diets_mmss')),
    'Stamina_Regen_Sitting_min':             mmss_to_min(cm.get('stamina_regen_sitting_mmss')),
    'Stamina_Regen_Standing_min':            mmss_to_min(cm.get('stamina_regen_standing_mmss')),
    'Stamina_Regen_Sitting_With_Diets_min':  mmss_to_min(cm.get('stamina_regen_sitting_diets_mmss')),
    'Stamina_Regen_Standing_With_Diets_min': mmss_to_min(cm.get('stamina_regen_standing_diets_mmss')),
    'Scent_Range_m':                         v(cm.get('scent_range_m')),
    'Turn_Radius_Note':                      v(cm.get('turn_radius_note')),
}, ['Dinosaur','Trot_kmh','Sprint_kmh','Stamina_Duration_min','Stamina_Duration_With_Diets_min',
    'Stamina_Regen_Sitting_min','Stamina_Regen_Standing_min',
    'Stamina_Regen_Sitting_With_Diets_min','Stamina_Regen_Standing_With_Diets_min',
    'Scent_Range_m','Turn_Radius_Note'])

# ── yt_htk_table.csv ──────────────────────────────────────────────────────────
HTK_FIELDS = ['Attacker','Target','Target_Class','Body_Hits_To_Kill','Head_Hits_To_Kill',
              'Charged_Body_Hits_To_Kill','Charged_Head_Hits_To_Kill']

for row in d.get('htk', []):
    append_row('yt_htk_table.csv', {
        'Attacker':               dino,
        'Target':                 row['target'],
        'Target_Class':           row['target_class'],
        'Body_Hits_To_Kill':      v(row.get('body')),
        'Head_Hits_To_Kill':      v(row.get('head')),
        'Charged_Body_Hits_To_Kill':  v(row.get('charged_body')),
        'Charged_Head_Hits_To_Kill':  v(row.get('charged_head')),
    }, HTK_FIELDS)

for row in d.get('htd', []):
    append_row('yt_htk_table.csv', {
        'Attacker':               row['attacker'],
        'Target':                 dino,
        'Target_Class':           row['target_class'] + ' HTD',
        'Body_Hits_To_Kill':      v(row.get('body')),
        'Head_Hits_To_Kill':      v(row.get('head')),
        'Charged_Body_Hits_To_Kill':  v(row.get('charged_body')),
        'Charged_Head_Hits_To_Kill':  v(row.get('charged_head')),
    }, HTK_FIELDS)

# ── yt_mechanics.csv ──────────────────────────────────────────────────────────
for m in d.get('mechanics', []):
    append_row('yt_mechanics.csv', {
        'Dinosaur':        dino,
        'Mechanic_Name':   m['name'],
        'Type':            m['type'],
        'Trigger':         v(m.get('trigger')),
        'Effect':          v(m.get('effect')),
        'Gameplay_Impact': v(m.get('impact')),
    }, ['Dinosaur','Mechanic_Name','Type','Trigger','Effect','Gameplay_Impact'])

# ── yt_survival.csv ───────────────────────────────────────────────────────────
sv = d.get('survival', {})
append_row('yt_survival.csv', {
    'Dinosaur':              dino,
    'Nest_Type':             v(sv.get('nest_type')),
    'Max_Eggs':              v(sv.get('max_eggs')),
    'Nest_Mechanic':         v(sv.get('nest_mechanic')),
    'Can_Eat_Bones':         v(sv.get('can_eat_bones')),
    'Vomits_From_Overeating':v(sv.get('vomits_from_overeating')),
    'Survival_Notes':        v(sv.get('notes')),
}, ['Dinosaur','Nest_Type','Max_Eggs','Nest_Mechanic','Can_Eat_Bones',
    'Vomits_From_Overeating','Survival_Notes'])

print(f"Done. {dino} appended to all 5 CSVs.")
