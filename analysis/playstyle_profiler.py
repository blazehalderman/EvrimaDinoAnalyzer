# analysis/playstyle_profiler.py

def generate_playstyle(profile: dict) -> list:
    tips = []
    diet = str(profile.get("Diet", "Unknown")).lower()
    mass = float(profile.get("Max_Mass_kg", 0) or 0)
    sprint = float(profile.get("Sprint_kmh", 0) or 0)
    mechs = [m.get("Mechanic_Name", m.get("Ability_Name", "")) for m in profile.get("mechanics", [])]

    if "carnivore" in diet:
        tips.append("Carnivore playstyle: Rely on hunting and scavenging. Stick near AI spawn zones when growing.")
    elif "herbivore" in diet:
        tips.append("Herbivore playstyle: Migrate constantly for varied diets. Keep an eye out for herds.")
    elif "omnivore" in diet:
        tips.append("Omnivore playstyle: Forage roots and hunt small AI. Very versatile.")

    if "Flight" in mechs:
        tips.append("Airborne mobility: You can easily escape terrestrial threats. Use height for scouting.")
    elif sprint > 45:
        tips.append("High mobility: Use your speed to hit-and-run or evade larger predators. Do not face-tank.")
    elif mass > 3000:
        tips.append("Heavyweight: You are a direct brawler. You dictate territory, but beware groups and stamina drain.")

    if "Bone Crush" in mechs or "Fractures" in mechs:
        tips.append("Bone breaker: Focus on crippling targets first to negate their escape options.")
    
    if "Grapple / Pin" in mechs or "Pounce / Pin" in mechs:
        tips.append("Pouncer: Manage your stamina carefully before latching to ensure you can finish the kill or escape.")

    return tips
