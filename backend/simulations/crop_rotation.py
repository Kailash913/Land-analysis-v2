"""
Crop Rotation Engine — rule-based crop sequence recommendations.
"""

# Crop rotation sequences for soil sustainability
ROTATION_SEQUENCES = {
    "Rice": ["Wheat", "Pulses", "Rice"],
    "Wheat": ["Soybean", "Maize", "Wheat"],
    "Cotton": ["Wheat", "Groundnut", "Cotton"],
    "Sugarcane": ["Pulses", "Wheat", "Sugarcane"],
    "Soybean": ["Wheat", "Maize", "Soybean"],
    "Groundnut": ["Wheat", "Millets", "Groundnut"],
    "Maize": ["Pulses", "Wheat", "Maize"],
    "Millets": ["Pulses", "Groundnut", "Millets"],
    "Pulses": ["Rice", "Wheat", "Pulses"],
    "Mustard": ["Rice", "Pulses", "Mustard"],
}


def suggest_rotation(primary_crop: str) -> dict:
    """
    Suggest a 3-year rotation plan based on the primary crop.
    """
    sequence = ROTATION_SEQUENCES.get(primary_crop, ["Pulses", "Wheat", primary_crop])

    plan = []
    for i, crop in enumerate(sequence):
        plan.append({
            "year": i + 1,
            "season": "Kharif" if i % 2 == 0 else "Rabi",
            "crop": crop,
            "benefit": _get_rotation_benefit(crop, primary_crop),
        })

    return {
        "primary_crop": primary_crop,
        "rotation_plan": plan,
        "rationale": f"Rotating with legumes/cereals helps restore nitrogen and break pest cycles for {primary_crop}.",
    }


def _get_rotation_benefit(crop: str, primary: str) -> str:
    if crop in ("Pulses", "Soybean", "Groundnut"):
        return "Nitrogen fixation — restores soil fertility"
    elif crop in ("Wheat", "Rice"):
        return "Cereal crop — utilizes different nutrients"
    elif crop in ("Millets", "Maize"):
        return "Deep rooting — breaks soil compaction"
    elif crop == primary:
        return "Primary crop — main revenue season"
    else:
        return "Diversification — reduces pest buildup"
