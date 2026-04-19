"""
Feature Engineering Service — Phase 3

Fuses raw data from all integrations into a normalized feature vector for ML models.
"""
import numpy as np
from utils.helpers import clamp

# Indian state → approximate base land rate (₹ per acre)
STATE_BASE_RATES = {
    "Andhra Pradesh": 2_500_000, "Arunachal Pradesh": 800_000, "Assam": 1_200_000,
    "Bihar": 1_800_000, "Chhattisgarh": 1_500_000, "Goa": 15_000_000,
    "Gujarat": 4_000_000, "Haryana": 6_000_000, "Himachal Pradesh": 3_000_000,
    "Jharkhand": 1_500_000, "Karnataka": 3_500_000, "Kerala": 8_000_000,
    "Madhya Pradesh": 2_000_000, "Maharashtra": 5_000_000, "Manipur": 900_000,
    "Meghalaya": 1_000_000, "Mizoram": 800_000, "Nagaland": 900_000,
    "Odisha": 1_800_000, "Punjab": 5_500_000, "Rajasthan": 2_500_000,
    "Sikkim": 2_000_000, "Tamil Nadu": 4_500_000, "Telangana": 3_500_000,
    "Tripura": 1_000_000, "Uttar Pradesh": 3_000_000, "Uttarakhand": 2_500_000,
    "West Bengal": 3_000_000, "Delhi": 50_000_000,
}

DEFAULT_BASE_RATE = 2_500_000

# Region type multipliers
REGION_MULTIPLIERS = {"urban": 2.5, "semi-urban": 1.5, "rural": 1.0}

# Soil quality scoring weights
SOIL_QUALITY_WEIGHTS = {
    "ph_score": 0.3,
    "oc_score": 0.4,
    "texture_score": 0.3,
}

# Texture → quality score
TEXTURE_QUALITY = {
    "Loam": 90, "Silt Loam": 85, "Clay Loam": 80,
    "Silty Clay Loam": 75, "Sandy Loam": 65, "Clay": 60,
    "Silty Clay": 55, "Sandy Clay Loam": 50, "Sand": 30,
    "Loamy Sand": 35, "Sandy Clay": 45, "Silt": 70,
}


def build_feature_vector(location: dict, soil: dict, climate: dict, infra: dict) -> dict:
    """
    Build a unified feature vector from raw API data.

    Returns a dict with:
    - All normalized features (0-100 scale)
    - Raw values for display
    - Derived composite indices
    """
    # 1. Base rate from state
    state = location.get("state", "Unknown")
    base_rate = STATE_BASE_RATES.get(state, DEFAULT_BASE_RATE)
    region_type = location.get("region_type", "rural")
    region_multiplier = REGION_MULTIPLIERS.get(region_type, 1.0)

    # 2. Soil quality index (0-100)
    ph = soil.get("ph", 6.8)
    oc = soil.get("organic_carbon", 0.5)
    texture = soil.get("texture", "Loam")

    # pH sweet spot: 6.0-7.5 is ideal
    ph_score = max(0, 100 - abs(ph - 6.8) * 25)
    # Organic carbon: higher is better, cap at 3%
    oc_score = min(100, (oc / 3.0) * 100)
    texture_score = TEXTURE_QUALITY.get(texture, 60)

    soil_quality_index = round(
        ph_score * SOIL_QUALITY_WEIGHTS["ph_score"]
        + oc_score * SOIL_QUALITY_WEIGHTS["oc_score"]
        + texture_score * SOIL_QUALITY_WEIGHTS["texture_score"],
        1
    )

    # 3. Climate index (0-100)
    avg_temp = climate.get("avg_temperature", 25)
    annual_rain = climate.get("annual_rainfall", 800)

    # Temperature: ideal 20-30°C
    temp_score = max(0, 100 - abs(avg_temp - 25) * 5)
    # Rainfall: ideal 600-1500mm
    if annual_rain < 300:
        rain_score = 20
    elif annual_rain < 600:
        rain_score = 50
    elif annual_rain <= 1500:
        rain_score = 90
    elif annual_rain <= 2500:
        rain_score = 70
    else:
        rain_score = 40

    climate_index = round((temp_score + rain_score) / 2, 1)

    # 4. Infrastructure score (already computed by overpass module)
    infra_score = infra.get("infrastructure_score", 40)

    # 5. Urban index (0-100)
    urban_index = {"urban": 90, "semi-urban": 50, "rural": 15}.get(region_type, 30)

    # 6. Adjusted base rate
    adjusted_rate = base_rate * region_multiplier

    return {
        # Raw values for display
        "base_rate": base_rate,
        "region_multiplier": region_multiplier,
        "adjusted_base_rate": adjusted_rate,

        # Normalized features for ML (0-100 scale)
        "soil_quality_index": clamp(soil_quality_index, 0, 100),
        "climate_index": clamp(climate_index, 0, 100),
        "infrastructure_score": clamp(infra_score, 0, 100),
        "urban_index": urban_index,

        # Sub-scores for explainability
        "ph_score": round(ph_score, 1),
        "oc_score": round(oc_score, 1),
        "texture_score": texture_score,
        "temp_score": round(temp_score, 1),
        "rain_score": rain_score,

        # Feature array for ML models
        "feature_array": [
            adjusted_rate / 1_000_000,  # Normalize to millions
            soil_quality_index,
            climate_index,
            infra_score,
            urban_index,
        ],
    }
