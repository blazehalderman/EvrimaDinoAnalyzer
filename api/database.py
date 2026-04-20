import pandas as pd
import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "normalized")

# Load datasets into memory on startup
class Database:
    def __init__(self):
        self.profiles = None
        self.mechanics = None
        self.hitboxes = None
        self.load_data()

    def load_data(self):
        profiles_path = os.path.join(DATA_DIR, "dino_profiles.csv")
        if os.path.exists(profiles_path):
            self.profiles = pd.read_csv(profiles_path)
            # Replace NaN with None for JSON serialization
            self.profiles = self.profiles.replace({np.nan: None})

        mech_path = os.path.join(DATA_DIR, "mechanics.csv")
        if os.path.exists(mech_path):
            self.mechanics = pd.read_csv(mech_path)
            self.mechanics = self.mechanics.replace({np.nan: None})

        mass_path = os.path.join(DATA_DIR, "lifecycle_mass_scaling.csv")
        if os.path.exists(mass_path):
            self.mass_scaling = pd.read_csv(mass_path)

        dmg_path = os.path.join(DATA_DIR, "lifecycle_damage_scaling.csv")
        if os.path.exists(dmg_path):
            self.dmg_scaling = pd.read_csv(dmg_path)

        speed_path = os.path.join(DATA_DIR, "lifecycle_speed_scaling.csv")
        if os.path.exists(speed_path):
            self.speed_scaling = pd.read_csv(speed_path)

        hitbox_path = os.path.join(DATA_DIR, "hitbox_multipliers.csv")
        if os.path.exists(hitbox_path):
            self.hitboxes = pd.read_csv(hitbox_path)

        htk_path = os.path.join(DATA_DIR, "htk_table.csv")
        if os.path.exists(htk_path):
            self.htk_table = pd.read_csv(htk_path)

    def get_all_dinos(self):
        if self.profiles is None:
            return []
        
        dinos = self.profiles.to_dict(orient="records")
        if self.mechanics is not None:
            for d in dinos:
                mech_rows = self.mechanics[self.mechanics['Dinosaur'].str.lower() == d['Dinosaur'].lower()]
                mechanics = mech_rows.to_dict(orient="records")
                for m in mechanics:
                    m.pop("Dinosaur", None)
                d['mechanics'] = mechanics
        return dinos

    def get_dino_by_name(self, name: str):
        if self.profiles is None:
            return None
        # Case insensitive exact match
        matches = self.profiles[self.profiles['Dinosaur'].str.lower() == name.lower()]
        if matches.empty:
            return None
            
        dino = matches.iloc[0].to_dict()
        if self.mechanics is not None:
            mech_rows = self.mechanics[self.mechanics['Dinosaur'].str.lower() == dino['Dinosaur'].lower()]
            mechanics = mech_rows.to_dict(orient="records")
            for m in mechanics:
                m.pop("Dinosaur", None)
            dino['mechanics'] = mechanics
        return dino

db = Database()
