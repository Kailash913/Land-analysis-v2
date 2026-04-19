"""
Water Requirement Analyzer — compares rainfall vs crop water demand.
"""

# Average water requirement in mm per growing season
CROP_WATER_NEEDS = {
    "Rice": 1200, "Wheat": 450, "Cotton": 700, "Sugarcane": 1500,
    "Soybean": 500, "Groundnut": 500, "Maize": 600, "Millets": 350,
    "Pulses": 400, "Tea": 1800, "Coffee": 1500, "Jute": 1000,
    "Mustard": 350, "Turmeric": 800, "Coconut": 1200,
}


def analyze_water_requirement(crops: list, annual_rainfall: float) -> dict:
    """
    Compare rainfall with crop water demands.
    Returns irrigation requirement indicator for each crop.
    """
    results = []

    for crop_info in crops:
        crop_name = crop_info.get("crop", "Unknown")
        water_need = CROP_WATER_NEEDS.get(crop_name, 600)
        deficit = water_need - annual_rainfall

        if deficit <= 0:
            status = "Rain-fed sufficient"
            irrigation_pct = 0
        elif deficit < 200:
            status = "Minimal supplemental irrigation"
            irrigation_pct = round(deficit / water_need * 100, 1)
        elif deficit < 500:
            status = "Moderate irrigation required"
            irrigation_pct = round(deficit / water_need * 100, 1)
        else:
            status = "Heavy irrigation essential"
            irrigation_pct = round(min(100, deficit / water_need * 100), 1)

        results.append({
            "crop": crop_name,
            "water_need_mm": water_need,
            "available_rainfall_mm": round(annual_rainfall),
            "deficit_mm": round(max(0, deficit)),
            "irrigation_pct": irrigation_pct,
            "status": status,
        })

    return {
        "water_analysis": results,
        "annual_rainfall_mm": round(annual_rainfall),
    }
