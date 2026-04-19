"""
Urban vs Agricultural Conflict Analyzer.

Detects when land is classified as agricultural but lies in a densely
urbanized area. Computes conversion probability and urbanization risk.

Outputs:
  conflict_level: HIGH / MEDIUM / LOW / NONE
  urbanization_score: 0-100
  agriculture_viability: 0-100
  conversion_probability: 0-1
  warnings: list of warning messages
"""


def analyze_conflict(
    land_use: dict,
    infra: dict,
    location: dict,
    urban_features: dict,
    agri_features: dict,
) -> dict:
    """
    Analyze urban vs agricultural conflict.

    If land is inside dense city but marked agricultural,
    system warns about viability and conversion risk.
    """
    predicted_use = land_use.get("predicted_use", "Residential")
    region_type = location.get("region_type", "semi-urban")

    # Core urban indicators
    urbanization_idx = urban_features.get("urbanization_index", 50)
    poi_density = urban_features.get("poi_density", 30)
    builtup_ratio = urban_features.get("builtup_ratio", 0.3)
    dev_score = urban_features.get("development_score", 40)
    infra_score = infra.get("infrastructure_score", 40)

    # Agricultural indicators
    agri_suit = agri_features.get("agriculture_suitability_score", 50)
    water_idx = agri_features.get("water_availability_index", 50)

    # Urbanization score (0-100)
    urbanization_score = round(
        urbanization_idx * 0.35 +
        poi_density * 0.2 +
        builtup_ratio * 100 * 0.2 +
        infra_score * 0.15 +
        dev_score * 0.10,
        1,
    )

    # Agriculture viability (inverted by urbanization)
    agriculture_viability = round(
        agri_suit * 0.4 +
        water_idx * 0.3 +
        max(0, (100 - urbanization_score)) * 0.3,
        1,
    )

    # Conversion probability
    if urbanization_score >= 80:
        conversion_prob = 0.90
    elif urbanization_score >= 60:
        conversion_prob = 0.70
    elif urbanization_score >= 40:
        conversion_prob = 0.40
    elif urbanization_score >= 25:
        conversion_prob = 0.20
    else:
        conversion_prob = 0.05

    # Detect conflict
    is_agricultural = predicted_use == "Agriculture"
    is_urban_area = region_type == "urban" or urbanization_score >= 60

    warnings = []
    conflict_level = "NONE"

    if is_agricultural and is_urban_area:
        conflict_level = "HIGH"
        warnings.append("High urbanization detected in area classified as agricultural")
        warnings.append(f"Agriculture viability declining: {agriculture_viability:.0f}/100")
        warnings.append(f"Future conversion probability: {conversion_prob*100:.0f}%")
        if urbanization_score >= 80:
            warnings.append("CRITICAL: Area is heavily urbanized — agricultural use not recommended")
    elif is_agricultural and urbanization_score >= 40:
        conflict_level = "MEDIUM"
        warnings.append("Moderate urbanization detected near agricultural land")
        warnings.append(f"Semi-urban encroachment risk: {conversion_prob*100:.0f}%")
    elif not is_agricultural and urbanization_score < 30:
        conflict_level = "LOW"
        warnings.append("Non-agricultural classification in rural area — verify land records")
    # else: NONE — no conflict

    # Investment risk factors
    risk_factors = []
    if conversion_prob >= 0.6:
        risk_factors.append("High likelihood of land use conversion")
    if urbanization_score >= 70 and agri_suit > 50:
        risk_factors.append("Good soil quality being lost to urbanization")
    if builtup_ratio >= 0.6:
        risk_factors.append("Significant built-up area around land parcel")
    if poi_density >= 60:
        risk_factors.append("High commercial/institutional density nearby")

    return {
        "conflict_level": conflict_level,
        "urbanization_score": urbanization_score,
        "agriculture_viability": agriculture_viability,
        "conversion_probability": round(conversion_prob, 2),
        "warnings": warnings,
        "risk_factors": risk_factors,
        "details": {
            "region_type": region_type,
            "predicted_land_use": predicted_use,
            "builtup_ratio": builtup_ratio,
            "poi_density": poi_density,
            "development_score": dev_score,
        },
    }
