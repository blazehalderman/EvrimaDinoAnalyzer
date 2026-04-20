import pandas as pd
import os

SOURCE1_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "gemini_the_isle_dino_breakdown_stats")
SOURCE3_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "youtube_doqi_guide")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "..", "data", "normalized")

def run():
    print("Loading and normalizing all datasets...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # --- 1. NORMALIZED DINO PROFILES ---
    # Merge base stats + combat mobility + survival into one core profile table
    df_s1_base = pd.read_csv(os.path.join(SOURCE1_DIR, "Base_Adult_Stats.csv")).add_prefix("S1_").rename(columns={"S1_Dinosaur": "Dinosaur"})
    df_s3_base = pd.read_csv(os.path.join(SOURCE3_DIR, "yt_base_stats.csv"))
    df_s3_combat = pd.read_csv(os.path.join(SOURCE3_DIR, "yt_combat_mobility.csv"))
    df_s3_survival = pd.read_csv(os.path.join(SOURCE3_DIR, "yt_survival.csv"))

    merged = pd.merge(df_s1_base, df_s3_base, on="Dinosaur", how="outer")
    merged = pd.merge(merged, df_s3_combat, on="Dinosaur", how="left", suffixes=("", "_combat"))
    merged = pd.merge(merged, df_s3_survival, on="Dinosaur", how="left", suffixes=("", "_survival"))

    profiles = pd.DataFrame()
    profiles["Dinosaur"] = merged["Dinosaur"]
    profiles["Diet"] = merged["S1_Diet"]
    profiles["Max_Mass_kg"] = merged["S1_Max_Mass_kg_HP"].combine_first(merged["Weight_kg"])
    profiles["Bite_Force_N"] = merged["Bite_Force_N"].combine_first(merged["S1_Base_Attack_N"])
    profiles["Sprint_kmh"] = merged["Sprint_kmh"].combine_first(merged["S1_Sprint_kmh"])
    profiles["Trot_kmh"] = merged["Trot_kmh"]
    profiles["Ambush_kmh"] = merged["S1_Ambush_kmh"]
    profiles["Food_Drain_min"] = merged["Hunger_min"].combine_first(merged["S1_Food_Drain_min"])
    profiles["Water_Drain_min"] = merged["Thirst_min"].combine_first(merged["S1_Water_Drain_min"])
    profiles["Growth_hrs"] = merged["Growth_hrs"].combine_first(merged["S1_Grow_Time_hrs"])
    
    # From combat & mobility
    profiles["Stamina_Duration_min"] = merged["Stamina_Duration_min"]
    profiles["Stamina_Regen_Sitting_min"] = merged["Stamina_Regen_Sitting_min"]
    profiles["Stamina_Regen_Standing_min"] = merged["Stamina_Regen_Standing_min"]
    profiles["Scent_Range_m"] = merged["Scent_Range_m"]
    profiles["Turn_Radius_Note"] = merged["Turn_Radius_Note"]
    
    # From survival
    profiles["Nest_Type"] = merged["Nest_Type"]
    profiles["Max_Eggs"] = merged["Max_Eggs"]
    profiles["Can_Eat_Bones"] = merged["Can_Eat_Bones"]
    profiles["Vomits_From_Overeating"] = merged["Vomits_From_Overeating"]

    profiles.to_csv(os.path.join(OUTPUT_DIR, "dino_profiles.csv"), index=False)

    # --- 2. MECHANICS & ABILITIES ---
    # Special_Abilities_Data.csv: Dinosaur,Ability_Name,Special_Damage_N,Modifier_Effect,Mechanical_Threshold_Limit,Penalty_Condition
    # yt_mechanics.csv: Dinosaur,Mechanic_Name,Type,Trigger,Effect,Gameplay_Impact
    df_ab = pd.read_csv(os.path.join(SOURCE1_DIR, "Special_Abilities_Data.csv"))
    df_mech = pd.read_csv(os.path.join(SOURCE3_DIR, "yt_mechanics.csv"))
    
    # Standardize columns for abilities
    df_ab = df_ab.rename(columns={
        "Ability_Name": "Mechanic_Name",
        "Modifier_Effect": "Effect",
        "Mechanical_Threshold_Limit": "Trigger_Threshold",
        "Penalty_Condition": "Gameplay_Impact"
    })
    df_ab["Type"] = "Special Ability"
    
    # Standardize columns for mechanics
    df_mech = df_mech.rename(columns={
        "Trigger": "Trigger_Threshold"
    })
    df_mech["Special_Damage_N"] = None
    
    mechanics_combined = pd.concat([df_ab, df_mech], ignore_index=True)
    mechanics_combined = mechanics_combined[["Dinosaur", "Mechanic_Name", "Type", "Effect", "Trigger_Threshold", "Gameplay_Impact", "Special_Damage_N"]]
    mechanics_combined.to_csv(os.path.join(OUTPUT_DIR, "mechanics.csv"), index=False)

    # --- 3. STRAIGHT PASS-THROUGHS ---
    # These tables don't need transformation because their geometries fit straight into our database
    pass_throughs = {
        (SOURCE1_DIR, "Hitbox_Multipliers.csv"): "hitbox_multipliers.csv",
        (SOURCE1_DIR, "Lifecycle_Damage_Scaling.csv"): "lifecycle_damage_scaling.csv",
        (SOURCE1_DIR, "Lifecycle_Mass_Scaling.csv"): "lifecycle_mass_scaling.csv",
        (SOURCE1_DIR, "Lifecycle_Speed_Scaling.csv"): "lifecycle_speed_scaling.csv",
        (SOURCE3_DIR, "yt_htk_table.csv"): "htk_table.csv",
    }
    
    for (src_dir, filename), out_name in pass_throughs.items():
        pd.read_csv(os.path.join(src_dir, filename)).to_csv(os.path.join(OUTPUT_DIR, out_name), index=False)
        
    print("Normalizations Complete! Unified datasets created in data/normalized/.")

if __name__ == '__main__':
    run()
