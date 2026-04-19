"""
Multi-Family Feature Engineering for Circle Rate ML Engine.

Combines 5 dataset families into a unified feature vector for
predicting government circle rates:
  A. Administrative & Location
  B. Land Use / Zoning
  C. Infrastructure & Accessibility
  D. Urban Development
  E. Agricultural & Environmental

Also computes Spatial Neighborhood Features and Geometry Features.
"""
import math
from typing import Optional


# ========================================================================
# A. Administrative & Location Features
# ========================================================================
# Municipality type encoding
MUNICIPALITY_TYPES = {
    "corporation": 5, "municipality": 4, "town_panchayat": 3,
    "panchayat": 2, "village_panchayat": 1, "unknown": 2,
}

# State encoding (economic tier)
STATE_TIERS = {
    "Maharashtra": 5, "Delhi": 5, "Karnataka": 4, "Tamil Nadu": 4,
    "Telangana": 4, "Gujarat": 4, "Kerala": 4, "Haryana": 4,
    "Goa": 4, "Punjab": 3, "West Bengal": 3, "Rajasthan": 3,
    "Uttar Pradesh": 3, "Madhya Pradesh": 2, "Andhra Pradesh": 3,
    "Odisha": 2, "Bihar": 2, "Jharkhand": 2, "Chhattisgarh": 2,
    "Assam": 2, "Uttarakhand": 3,
}


def extract_admin_features(location: dict) -> dict:
    """
    Extract administrative features from the reverse-geocoded location.
    Governments assign values based on administrative hierarchy.
    """
    state = location.get("state", "Unknown")
    region_type = location.get("region_type", "semi-urban")

    # Urban-rural flag
    urban_rural = {"urban": 3, "semi-urban": 2, "rural": 1}.get(region_type, 2)

    # Municipality type from region_type (approximation)
    if region_type == "urban":
        muni = "corporation" if STATE_TIERS.get(state, 2) >= 4 else "municipality"
    elif region_type == "semi-urban":
        muni = "town_panchayat"
    else:
        muni = "village_panchayat"

    return {
        "state_tier": STATE_TIERS.get(state, 2),
        "municipality_type": MUNICIPALITY_TYPES.get(muni, 2),
        "urban_rural_flag": urban_rural,
    }


# ========================================================================
# B. Land Use / Zoning Features
# ========================================================================
LAND_USE_ENCODING = {
    "Agriculture": 1, "Residential": 3, "Commercial": 5,
    "Industrial": 4, "Mixed-use": 4,
}


def extract_zoning_features(land_use_prediction: dict, infra: dict) -> dict:
    """
    Extract land-use and zoning features.
    Governments value commercial > residential > agricultural.
    """
    predicted_use = land_use_prediction.get("predicted_use", "Residential")
    probabilities = land_use_prediction.get("probabilities", {})

    commercial_prob = probabilities.get("Commercial", 0) / 100
    industrial_flag = 1 if predicted_use == "Industrial" else 0

    # FSI estimate based on land classification
    fsi_map = {"Commercial": 3.0, "Residential": 2.0, "Industrial": 1.5,
               "Mixed-use": 2.5, "Agriculture": 0.5}

    return {
        "land_use_type": LAND_USE_ENCODING.get(predicted_use, 2),
        "commercial_permission": round(commercial_prob, 2),
        "industrial_zone_flag": industrial_flag,
        "fsi_allowed": fsi_map.get(predicted_use, 1.5),
        "zoning_category": LAND_USE_ENCODING.get(predicted_use, 2),
    }


# ========================================================================
# C. Infrastructure & Accessibility Features
# ========================================================================
def extract_infra_features(infra: dict) -> dict:
    """
    Extract infrastructure proximity and connectivity features.
    Governments increase values near highways, railways, and city centers.
    """
    road_km = infra.get("nearest_road_km") or 10.0
    market_km = infra.get("nearest_market_km") or 10.0
    settlement_km = infra.get("nearest_settlement_km") or 10.0
    total_amenities = infra.get("total_amenities", 0)
    infra_score = infra.get("infrastructure_score", 40)

    # Road density proxy (amenities per 5km radius)
    road_density = min(100, total_amenities * 3)

    # Connectivity score (composite)
    connectivity = round(100 - (road_km * 5 + market_km * 3 + settlement_km * 2), 1)
    connectivity = max(0, min(100, connectivity))

    # Distance to city center proxy
    dist_city_center = settlement_km if settlement_km < 99 else 20.0

    # Categorize landmarks into facility types
    landmarks = infra.get("landmarks", [])
    has_railway = any(l.get("type") == "railway" for l in landmarks)
    has_hospital = any("hospital" in l.get("name", "").lower() or l.get("type") == "amenity" for l in landmarks)

    return {
        "distance_highway": round(road_km, 2),
        "distance_main_road": round(min(road_km, 5.0), 2),
        "road_density": road_density,
        "connectivity_score": connectivity,
        "distance_city_center": round(dist_city_center, 2),
        "infrastructure_score": infra_score,
        "has_railway": 1 if has_railway else 0,
        "has_hospital_nearby": 1 if has_hospital else 0,
    }


# ========================================================================
# D. Urban Development Features
# ========================================================================
def extract_urban_features(infra: dict, location: dict) -> dict:
    """
    Extract urban development indicators.
    Governments increase values in developed areas.
    """
    total_amenities = infra.get("total_amenities", 0)
    infra_score = infra.get("infrastructure_score", 40)
    region_type = location.get("region_type", "semi-urban")

    # Population density proxy from region type + amenity count
    if region_type == "urban":
        pop_density_base = 5000
    elif region_type == "semi-urban":
        pop_density_base = 1500
    else:
        pop_density_base = 300

    pop_density = pop_density_base + total_amenities * 100

    # POI density (points of interest per sq km — proxy)
    poi_density = min(100, total_amenities * 5)

    # Built-up ratio proxy
    builtup_ratio = {"urban": 0.7, "semi-urban": 0.4, "rural": 0.1}.get(region_type, 0.3)

    # Urbanization index (0-100)
    urbanization = round(
        infra_score * 0.4 + poi_density * 0.3 + builtup_ratio * 100 * 0.3, 1
    )

    # Development score
    dev_score = round(
        (infra_score + poi_density + urbanization) / 3, 1
    )

    return {
        "population_density": pop_density,
        "poi_density": poi_density,
        "builtup_ratio": round(builtup_ratio, 2),
        "urbanization_index": min(100, urbanization),
        "development_score": min(100, dev_score),
    }


# ========================================================================
# E. Agricultural & Environmental Features
# ========================================================================
SOIL_TYPE_ENCODING = {
    "Loam": 5, "Silt Loam": 5, "Clay Loam": 4, "Silty Clay Loam": 4,
    "Sandy Loam": 3, "Clay": 3, "Silty Clay": 3, "Sandy Clay Loam": 3,
    "Silt": 3, "Sand": 1, "Loamy Sand": 2, "Sandy Clay": 2,
}

CLIMATE_ZONES = {
    "tropical_wet": 4, "tropical_dry": 3, "subtropical": 3,
    "semi-arid": 2, "arid": 1, "temperate": 4,
}


def extract_agri_features(soil: dict, climate: dict) -> dict:
    """
    Extract agricultural and environmental features.
    Used for agricultural land valuation alignment.
    """
    texture = soil.get("texture", "Loam")
    ph = soil.get("ph", 6.8)
    oc = soil.get("organic_carbon", 0.5)

    avg_temp = climate.get("avg_temperature", 25)
    annual_rain = climate.get("annual_rainfall", 800)
    climate_zone = climate.get("climate_zone", "tropical_dry")

    # Soil quality for agriculture (0-100)
    soil_score = SOIL_TYPE_ENCODING.get(texture, 3) * 20 + max(0, 100 - abs(ph - 6.8) * 25) * 0.3

    # Water availability index (0-100)
    if annual_rain >= 1200:
        water_idx = 90
    elif annual_rain >= 800:
        water_idx = 70
    elif annual_rain >= 500:
        water_idx = 50
    elif annual_rain >= 300:
        water_idx = 30
    else:
        water_idx = 15

    # Agriculture suitability (0-100)
    agri_suit = round((soil_score * 0.4 + water_idx * 0.3 + min(100, oc * 40) * 0.3), 1)

    return {
        "soil_type_encoded": SOIL_TYPE_ENCODING.get(texture, 3),
        "rainfall_average": annual_rain,
        "temperature_zone": CLIMATE_ZONES.get(climate_zone, 3),
        "water_availability_index": water_idx,
        "agriculture_suitability_score": min(100, agri_suit),
    }


# ========================================================================
# Spatial Neighborhood Features
# ========================================================================
def extract_spatial_features(circle_rate: dict) -> dict:
    """
    Spatial neighborhood features from TNREGINET lookup.
    Government rates are spatially consistent — nearby zones have similar rates.
    """
    rate = circle_rate.get("circle_rate") or 0
    confidence = circle_rate.get("confidence_score", 0)
    base_rate = circle_rate.get("base_residential_rate") or rate

    # Simulate neighborhood averages from the matched rate
    # In production, these would come from querying nearby zones
    if rate > 0:
        avg_500m = round(rate * 0.95)  # Slightly lower avg in 500m
        avg_1km = round(rate * 0.85)   # Lower avg in 1km radius
        zone_cluster_mean = round(rate * 0.90)
    else:
        avg_500m = 0
        avg_1km = 0
        zone_cluster_mean = 0

    return {
        "avg_rate_within_500m": avg_500m,
        "avg_rate_within_1km": avg_1km,
        "nearest_zone_rate": rate,
        "zone_cluster_mean": zone_cluster_mean,
        "known_circle_rate": rate,
        "rate_confidence": confidence,
    }


# ========================================================================
# Historical Revision Features
# ========================================================================
def extract_revision_features() -> dict:
    """
    Historical revision tracking.
    Tamil Nadu revises guideline values periodically (typically every 3-5 years).
    """
    return {
        "years_since_revision": 1,  # Last revision: 2024-07-01
        "revision_growth_rate": 0.08,  # ~8% avg annual increase
        "historical_trend": 1,  # 1=increasing, 0=stable, -1=decreasing
    }


# ========================================================================
# Geometry Features (for polygon mode)
# ========================================================================
def extract_geometry_features(
    area_sqft: float = 0,
    perimeter_m: float = 0,
    road_frontage: float = 0,
    is_corner: bool = False,
) -> dict:
    """
    Features computed from user-drawn polygon.
    """
    if area_sqft > 0 and perimeter_m > 0:
        area_sqm = area_sqft * 0.0929
        # Shape regularity: perfect square = 1.0, irregular = lower
        ideal_perimeter = 4 * math.sqrt(area_sqm)
        shape_reg = min(1.0, ideal_perimeter / max(perimeter_m, 1))
    else:
        shape_reg = 0.8  # default for pin mode

    return {
        "area_sqft": area_sqft,
        "perimeter_m": perimeter_m,
        "shape_regularness": round(shape_reg, 3),
        "road_frontage_ratio": round(road_frontage, 2),
        "corner_plot_flag": 1 if is_corner else 0,
    }


# ========================================================================
# MASTER: Build Complete Feature Vector
# ========================================================================
def build_ml_feature_vector(
    location: dict,
    soil: dict,
    climate: dict,
    infra: dict,
    land_use_pred: dict,
    circle_rate: dict,
    area_sqft: float = 0,
    perimeter_m: float = 0,
) -> dict:
    """
    Build the complete ML feature vector combining all 5 families
    plus spatial, historical, and geometry features.

    Returns a dict with all features + a 'feature_array' list for model input.
    """
    admin = extract_admin_features(location)
    zoning = extract_zoning_features(land_use_pred, infra)
    infra_f = extract_infra_features(infra)
    urban = extract_urban_features(infra, location)
    agri = extract_agri_features(soil, climate)
    spatial = extract_spatial_features(circle_rate)
    revision = extract_revision_features()
    geometry = extract_geometry_features(area_sqft, perimeter_m)

    # Combine all features
    all_features = {}
    all_features.update(admin)
    all_features.update(zoning)
    all_features.update(infra_f)
    all_features.update(urban)
    all_features.update(agri)
    all_features.update(spatial)
    all_features.update(revision)
    all_features.update(geometry)

    # Build the model input vector (ordered for LightGBM)
    all_features["model_input"] = [
        admin["state_tier"],
        admin["municipality_type"],
        admin["urban_rural_flag"],
        zoning["land_use_type"],
        zoning["zoning_category"],
        zoning["fsi_allowed"],
        infra_f["distance_highway"],
        infra_f["distance_city_center"],
        infra_f["connectivity_score"],
        infra_f["infrastructure_score"],
        urban["population_density"],
        urban["poi_density"],
        urban["builtup_ratio"],
        urban["urbanization_index"],
        urban["development_score"],
        agri["soil_type_encoded"],
        agri["rainfall_average"],
        agri["water_availability_index"],
        agri["agriculture_suitability_score"],
        spatial["avg_rate_within_1km"],
        spatial["nearest_zone_rate"],
        revision["revision_growth_rate"],
    ]

    return all_features


# Feature names (matching model_input order)
FEATURE_NAMES = [
    "state_tier", "municipality_type", "urban_rural_flag",
    "land_use_type", "zoning_category", "fsi_allowed",
    "distance_highway", "distance_city_center", "connectivity_score",
    "infrastructure_score",
    "population_density", "poi_density", "builtup_ratio",
    "urbanization_index", "development_score",
    "soil_type_encoded", "rainfall_average", "water_availability_index",
    "agriculture_suitability_score",
    "avg_rate_within_1km", "nearest_zone_rate",
    "revision_growth_rate",
]
