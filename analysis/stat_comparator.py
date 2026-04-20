import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def scale_attacker_stats(attacker: Dict[str, Any], growth_pct: float, is_prime: bool, mass_df: Optional[pd.DataFrame], dmg_df: Optional[pd.DataFrame], speed_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Applies lifecycle scaling modifiers to an attacker's base stats based on growth percentage or prime status."""
    scaled = attacker.copy()
    dino_name = attacker.get("Dinosaur")

    def _interpolate_stat(df: pd.DataFrame, base_val: float) -> float:
        if df is None:
            return base_val
        
        row = df[df["Dinosaur"].str.lower() == dino_name.lower()]
        if row.empty:
            return base_val
            
        row = row.iloc[0]
        
        # Mapping of target percentages to the dataset columns
        pts = {
            25: "25_Percent_Juvi",
            50: "50_Percent_SubJuvi",
            75: "75_Percent_SubAdult",
            100: "100_Percent_Adult"
        }

        if is_prime:
            # Find the Prime Elder column dynamically
            prime_col = next((col for col in df.columns if "Prime_Elder" in col), None)
            if prime_col and pd.notna(row.get(prime_col)):
                try:
                    return float(row.get(prime_col))
                except (ValueError, TypeError):
                    pass
            # Fallback to standard base val if something fails
            return base_val
            
        # Full dynamic growth (0% to 100%)
        target_pct = max(0.0, min(100.0, float(growth_pct)))
        x_vals = [0, 25, 50, 75, 100]
        
        y_vals = []
        for x in x_vals:
            if x == 0:
                y_vals.append(0.0) # Anchor at 0 for anything under 25%
                continue
                
            col_name = pts[x]
            val = row.get(col_name)
            try:
                y_vals.append(float(val))
            except (ValueError, TypeError):
                y_vals.append(base_val)

        # Linear interpolation for growth percentages between breakpoints
        return float(np.interp(target_pct, x_vals, y_vals))

    scaled["Max_Mass_kg"] = _interpolate_stat(mass_df, attacker.get("Max_Mass_kg", 0))
    scaled["Bite_Force_N"] = _interpolate_stat(dmg_df, attacker.get("Bite_Force_N", 0))
    
    # Speed interpolations
    scaled["Sprint_kmh"] = _interpolate_stat(speed_df, attacker.get("Sprint_kmh", 0))
    scaled["Trot_kmh"] = _interpolate_stat(speed_df, attacker.get("Trot_kmh", 0))
    scaled["Ambush_kmh"] = _interpolate_stat(speed_df, attacker.get("Ambush_kmh", 0))

    return scaled
