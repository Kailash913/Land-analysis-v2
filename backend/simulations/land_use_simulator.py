"""
Land Use Simulator — compares Agriculture, Residential, and Commercial suitability.
"""


def simulate_best_land_use(features: dict, location: dict, climate: dict) -> dict:
    """
    Generate weighted suitability scores for each land use category.
    More nuanced than the classifier — shows detailed breakdown.
    """
    soil_qi = features["soil_quality_index"]
    climate_i = features["climate_index"]
    infra = features["infrastructure_score"]
    urban = features["urban_index"]

    # Agriculture suitability
    agri_score = (
        soil_qi * 0.35
        + climate_i * 0.30
        + (100 - urban) * 0.20  # Rural areas better for agriculture
        + min(infra, 60) * 0.15  # Some infra needed but not too much
    )

    # Residential suitability
    resi_score = (
        infra * 0.30
        + urban * 0.30
        + climate_i * 0.20
        + min(soil_qi, 50) * 0.10  # Marginal importance
        + 10  # Base score — can always build houses
    )

    # Commercial suitability
    comm_score = (
        infra * 0.35
        + urban * 0.40
        + climate_i * 0.10
        + (100 - soil_qi) * 0.05  # Inverse — commercial doesn't need good soil
        + 10
    )

    # Normalize to 100
    total = agri_score + resi_score + comm_score
    if total > 0:
        agri_pct = round(agri_score / total * 100, 1)
        resi_pct = round(resi_score / total * 100, 1)
        comm_pct = round(100 - agri_pct - resi_pct, 1)
    else:
        agri_pct = resi_pct = comm_pct = 33.3

    results = [
        {"use": "Agriculture", "score": round(agri_score, 1), "percentage": agri_pct},
        {"use": "Residential", "score": round(resi_score, 1), "percentage": resi_pct},
        {"use": "Commercial", "score": round(comm_score, 1), "percentage": comm_pct},
    ]
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "best_use": results[0]["use"],
        "suitability": results,
    }
