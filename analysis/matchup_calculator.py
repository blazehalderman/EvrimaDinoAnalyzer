import pandas as pd
from typing import Dict, Any, List
import math

# We can rely on standard 2.6x headshot and 1.0x body, we'll code it directly into MVP calculator for simplicity, but could pull from DB if it becomes dino-specific later.
HEAD_MULTIPLIER = 2.6

# Base Mechanic Lethality Multipliers
M_SCORES = {
    # Extreme Lethality (Grapples, Instakills)
    "Aquatic Lunge": 1.7, "Lunge": 1.7, "Drop Attack": 1.6,
    "Gore / Trample": 1.6, "Grapple / Pin": 1.5, "Pounce / Pin": 1.4,
    "Pounce / Grapple": 1.4, "Pounce": 1.3,
    
    # Stun / Knockdown / Heavy Trauma / Breaks
    "Bone Crush": 1.5, "Fractures": 1.4, "Crush": 1.4,
    "Directional Tail Swing": 1.4, "High-Speed Charge": 1.3,
    "Dome Charge": 1.3, "Rear Kick / Slam": 1.3, "Flip": 1.3,
    "Horn Spar": 1.2, "Sprint Attack": 1.2,

    # Heavy Damage Over Time / Status
    "Venom Spit": 1.4, "Venom": 1.4, "Venom Pounce": 1.4,
    "Acid Spit": 1.3, "Bacteria Bite": 1.3, "Bacterial Bite": 1.3,
    
    # Evasion / Utility / Defensive
    "Flight": 1.4, "Tree Climbing": 1.3, 
    "Dodge Roll": 1.2, "Diving": 1.2, "Amphibious": 1.2,
    "Bleed Resistance": 1.2,
    "Take Off": 1.1, "Latching": 1.1,
    "Aquatic Alt-Bite": 1.1, "Watersense": 1.1, "Stance Switch / Stomp": 1.1,
    "Dropkick / Vocals": 1.1, "Sparring": 1.1, "Airbrake": 1.05, "Skimming": 1.05,
    
    # Standard (Default 1.0)
    "Prime Elder": 1.1, "Directional Attack": 1.05,
    "Standard Attack": 1.0, "Primary Attack": 1.0, "Primary Bite": 1.0
}

def calculate_matchups(attacker_data: Dict[str, Any], all_dinos: List[Dict[str, Any]], htk_table: Optional[pd.DataFrame] = None, hitbox_table: Optional[pd.DataFrame] = None, pack_size: int = 1) -> List[Dict[str, Any]]:
    """
    Calculates matchup viability for an attacker against all other dinos.
    Rule from agents/analysis_agent.md:
    Engage: attacker kills defender in fewer hits than defender kills attacker
    Caution: roughly equal hits required
    Flee: defender kills attacker in fewer hits
    
    pack_size scales the hits needed for the defender to wipe the attacking pack,
    and proportionally speeds up the "Hits To Kill Them" via group DPS.
    """
    attacker_name = attacker_data.get("Dinosaur")
    attacker_mass = float(attacker_data.get("Max_Mass_kg", 0) or 0)
    attacker_bite = float(attacker_data.get("Bite_Force_N", 0) or 0)
    
    # Get head multiplier
    head_mult = 2.6
    if hitbox_table is not None and 'Hitbox_Zone' in hitbox_table.columns:
        hits = hitbox_table[hitbox_table['Hitbox_Zone'].str.lower() == 'head']
        if not hits.empty and 'Damage_Multiplier' in hits.columns:
            head_mult = float(hits.iloc[0]['Damage_Multiplier'])
    
    matchups = []
    
    for defender in all_dinos:
        defender_name = defender.get("Dinosaur")
        
        if defender_name == attacker_name:
            continue
            
        defender_mass = float(defender.get("Max_Mass_kg", 0) or 0)
        defender_bite = float(defender.get("Bite_Force_N", 0) or 0)
        
        if attacker_bite <= 0 or defender_mass <= 0 or defender_bite <= 0 or attacker_mass <= 0:
             continue
             
        # Isle Weight Ratio Mechanic: Damage is scaled by (Attacker Weight / Defender Weight)
        attacker_weight_ratio = attacker_mass / defender_mass
        defender_weight_ratio = defender_mass / attacker_mass

        # Try to use YT verified Hits To Kill if it exists and both are strictly 100% adults
        # For simplicity, we only use the verified HTK table if the attacker is 100%
        yt_attacker_body = None
        yt_attacker_head = None
        yt_defender_body = None
        yt_defender_head = None
        
        hits_to_kill_defender_body = None
        hits_to_kill_defender_head = None
        hits_to_kill_attacker_body = None
        hits_to_kill_attacker_head = None

        if htk_table is not None and not htk_table.empty:
            # Query for Attacker vs Defender
            row_atk_vs_def = htk_table[(htk_table['Attacker'].str.lower() == attacker_name.lower()) & (htk_table['Target'].str.lower() == defender_name.lower())]
            if not row_atk_vs_def.empty:
                val_b = row_atk_vs_def.iloc[0].get("Body_Hits_To_Kill")
                val_h = row_atk_vs_def.iloc[0].get("Head_Hits_To_Kill")
                if pd.notna(val_b): yt_attacker_body = float(val_b)
                if pd.notna(val_h): yt_attacker_head = float(val_h)

            # Query for Defender vs Attacker
            row_def_vs_atk = htk_table[(htk_table['Attacker'].str.lower() == defender_name.lower()) & (htk_table['Target'].str.lower() == attacker_name.lower())]
            if not row_def_vs_atk.empty:
                val_b = row_def_vs_atk.iloc[0].get("Body_Hits_To_Kill")
                val_h = row_def_vs_atk.iloc[0].get("Head_Hits_To_Kill")
                if pd.notna(val_b): yt_defender_body = float(val_b)
                if pd.notna(val_h): yt_defender_head = float(val_h)

        # Base math fallback
        actual_attacker_dmg_body = attacker_bite * attacker_weight_ratio
        actual_defender_dmg_body = defender_bite * defender_weight_ratio
        
        # Body hits base (minimum 1.0 hit)
        if yt_attacker_body is not None:
            hits_to_kill_defender_body = max(1.0, yt_attacker_body / pack_size)
        else:
            hits_to_kill_defender_body = max(1.0, defender_mass / (actual_attacker_dmg_body * pack_size))
            
        if yt_defender_body is not None:
            hits_to_kill_attacker_body = max(1.0, yt_defender_body) * pack_size
        else:
            hits_to_kill_attacker_body = max(1.0, attacker_mass / actual_defender_dmg_body) * pack_size
        
        # Head hits (minimum 1.0 hit)
        if yt_attacker_head is not None:
            hits_to_kill_defender_head = max(1.0, yt_attacker_head / pack_size)
        else:
            hits_to_kill_defender_head = max(1.0, defender_mass / (actual_attacker_dmg_body * head_mult * pack_size))
            
        if yt_defender_head is not None:
            hits_to_kill_attacker_head = max(1.0, yt_defender_head) * pack_size
        else:
            hits_to_kill_attacker_head = max(1.0, attacker_mass / (actual_defender_dmg_body * head_mult)) * pack_size
        
        # Verdict is based strictly on standard body hits for reliability:
        base_ratio = hits_to_kill_defender_body / hits_to_kill_attacker_body
        
        # Apply special mechanics mathematical weight
        ratio_modifier = 1.0
        
        def_mechs = [m.get("Mechanic_Name", m.get("Ability_Name", "")) for m in defender.get("mechanics", [])]
        atk_mechs = [m.get("Mechanic_Name", m.get("Ability_Name", "")) for m in attacker_data.get("mechanics", [])]
        
        # Defender Defensive/Lethality Multipliers (Increases ratio -> Pulls toward Flee)
        for mech in def_mechs:
            score = M_SCORES.get(mech, 1.0)
            
            # Apply strict conditional mass checks if applicable
            if mech in ["Aquatic Lunge", "Lunge"] and attacker_mass >= 4000:
                continue # Grab fails on huge targets, ignore lethal modifier
            if mech == "Bone Crush" and attacker_mass >= (defender_mass * 0.75):
                continue # Leg break threshold fails
                
            if score > 1.0:
                # Add fractional advantage (e.g. 1.4 score = 1.4x harder to fight)
                ratio_modifier *= score
                
        # Attacker Lethality Multipliers (Decreases ratio -> Pulls toward Engage)
        for mech in atk_mechs:
            score = M_SCORES.get(mech, 1.0)

            if mech in ["Aquatic Lunge", "Lunge"] and defender_mass >= 4000:
                continue # Grab fails
            if mech == "Bone Crush" and defender_mass >= (attacker_mass * 0.75):
                continue
                
            if score > 1.0:
                # E.g. A 1.4 attacker mechanic reduces the kill difficulty by dividing
                # meaning ratio gets smaller, making it an Engage
                ratio_modifier /= score

        final_ratio = base_ratio * ratio_modifier
        
        if final_ratio < 0.8:
            verdict = "Engage"
        elif final_ratio > 1.2:
            verdict = "Flee"
        else:
            verdict = "Caution"
            
        matchups.append({
            "opponent": defender_name,
            "hits_to_kill_them_body": round(hits_to_kill_defender_body, 1),
            "hits_to_kill_them_head": math.ceil(hits_to_kill_defender_head * 10) / 10.0, # Round UP to nearest tenth
            "hits_for_them_to_kill_you_body": round(hits_to_kill_attacker_body, 1),
            "hits_for_them_to_kill_you_head": math.ceil(hits_to_kill_attacker_head * 10) / 10.0,
            "verdict": verdict,
            "speed_advantage": "Faster" if float(attacker_data.get("Sprint_kmh", 0) or 0) > float(defender.get("Sprint_kmh", 0) or 0) else "Slower",
            "opponent_mechanics": defender.get("mechanics", []),
            "opponent_diet": str(defender.get("Diet", "Unknown") or "Unknown"),
            "attacker_sprint_kmh": float(attacker_data.get("Sprint_kmh", 0) or 0),
            "defender_sprint_kmh": float(defender.get("Sprint_kmh", 0) or 0)
        })
        
    return matchups
