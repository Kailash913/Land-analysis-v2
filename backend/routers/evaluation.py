"""
Evaluation Router — the primary endpoint for land evaluation.

POST /api/evaluate-land
GET  /api/evaluate-land (for frontend compatibility)
POST /api/evaluate-polygon — polygon area evaluation

Pipeline:
  1. Reverse geocode → admin hierarchy
  2. Circle rate lookup (TNREGINET — SOURCE OF TRUTH)
  3. Fetch soil, climate, infrastructure, facilities
  4. 5-family ML feature engineering
  5. LightGBM circle rate prediction (learns govt valuation logic)
  6. Land type classification
  7. Urban vs Agricultural conflict analysis
  8. Crop recommendations, simulations
  9. Area-scaled valuation (polygon mode)
  10. Comprehensive insights dashboard data
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
import math

from integrations.nominatim import reverse_geocode
from integrations.soilgrids import fetch_soil_data
from integrations.open_meteo import fetch_climate_data
from integrations.overpass import fetch_infrastructure
from integrations.facility_detector import fetch_facilities
from services.circle_rate_engine import lookup_circle_rate
from services.conflict_analyzer import analyze_conflict
from services.feature_engineering import build_feature_vector
from ml.ml_features import (
    build_ml_feature_vector,
    extract_admin_features,
    extract_zoning_features,
    extract_infra_features,
    extract_urban_features,
    extract_agri_features,
)
from ml.circle_rate_predictor import circle_rate_predictor
from ml import land_use_model, crop_model, risk_model
from simulations.land_use_simulator import simulate_best_land_use
from simulations.crop_rotation import suggest_rotation
from simulations.water_analyzer import analyze_water_requirement
from database.models import Evaluation

SQFT_PER_ACRE = 43560

router = APIRouter()


class EvaluationRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class PolygonRequest(BaseModel):
    coordinates: List[List[float]] = Field(..., description="[[lat,lng], ...]")
    area_sqft: float = Field(0, ge=0)
    area_acres: float = Field(0, ge=0)
    area_sqmeters: float = Field(0, ge=0)
    perimeter_m: float = Field(0, ge=0)


@router.post("/evaluate-land")
async def evaluate_land_post(req: EvaluationRequest):
    return await _run_evaluation(req.lat, req.lng)


@router.get("/evaluate-land")
async def evaluate_land_get(lat: float, lng: float):
    return await _run_evaluation(lat, lng)


@router.get("/map-data")
async def map_data(lat: float, lng: float):
    return await _run_evaluation(lat, lng)


@router.post("/evaluate-polygon")
async def evaluate_polygon(req: PolygonRequest):
    """Evaluate a polygon area — computes centroid + area-scaled valuation."""
    if len(req.coordinates) < 3:
        return {"error": "Polygon needs at least 3 points"}

    # Compute centroid
    lats = [c[0] for c in req.coordinates]
    lngs = [c[1] for c in req.coordinates]
    centroid_lat = sum(lats) / len(lats)
    centroid_lng = sum(lngs) / len(lngs)

    result = await _run_evaluation(
        centroid_lat, centroid_lng,
        area_sqft=req.area_sqft,
        perimeter_m=req.perimeter_m,
    )

    # Add polygon-specific data
    result["polygon"] = {
        "centroid": {"lat": centroid_lat, "lng": centroid_lng},
        "vertices": len(req.coordinates),
        "area_sqft": req.area_sqft,
        "area_acres": req.area_acres,
        "area_sqmeters": req.area_sqmeters,
        "perimeter_m": req.perimeter_m,
    }

    # Area-scaled valuation
    circle_rate = result.get("real_data", {}).get("circle_rate") or 0
    ml_rate = result.get("ml_circle_rate", {}).get("predicted_circle_rate") or 0

    if req.area_sqft > 0:
        result["valuation"] = {
            "total_value_circle_rate": round(circle_rate * req.area_sqft),
            "total_value_ml_prediction": round(ml_rate * req.area_sqft),
            "area_sqft": req.area_sqft,
            "circle_rate_per_sqft": circle_rate,
            "ml_rate_per_sqft": ml_rate,
            "note": "Total Value = Area × Circle Rate",
        }
    else:
        result["valuation"] = None

    return result


async def _run_evaluation(
    lat: float, lng: float,
    area_sqft: float = 0,
    perimeter_m: float = 0,
) -> dict:
    """
    Complete evaluation pipeline:
      1. Parallel data fetch (geocode, soil, climate, infra, facilities)
      2. Circle rate lookup (TNREGINET — SOURCE OF TRUTH)
      3. ML feature engineering (5 families + spatial + geometry)
      4. LightGBM circle rate prediction
      5. Land classification + conflict analysis
      6. Crop recommendations + simulations
      7. Build comprehensive insights output
    """
    import asyncio

    # Phase 1: Parallel data fetch
    location, soil, climate, infra, facilities = await asyncio.gather(
        reverse_geocode(lat, lng),
        fetch_soil_data(lat, lng),
        fetch_climate_data(lat, lng),
        fetch_infrastructure(lat, lng),
        fetch_facilities(lat, lng),
    )

    # Phase 2: Circle rate (GOVERNMENT — SOURCE OF TRUTH)
    circle_rate = lookup_circle_rate(location)

    # Phase 3: Basic feature vector (for existing models)
    basic_features = build_feature_vector(location, soil, climate, infra)
    basic_features["_city"] = location.get("district", "")
    basic_features["_neighborhood"] = location.get("village", "") or location.get("suburb", "")

    # Phase 4: Land use classification (needed for ML features)
    land_use = land_use_model.predict(basic_features)

    # Phase 5: ML Feature Engineering (5 families)
    admin_f = extract_admin_features(location)
    zoning_f = extract_zoning_features(land_use, infra)
    infra_f = extract_infra_features(infra)
    urban_f = extract_urban_features(infra, location)
    agri_f = extract_agri_features(soil, climate)

    ml_features = build_ml_feature_vector(
        location, soil, climate, infra,
        land_use, circle_rate,
        area_sqft=area_sqft,
        perimeter_m=perimeter_m,
    )

    # Phase 6: LightGBM Circle Rate Prediction
    ml_circle_rate = circle_rate_predictor.predict(ml_features)

    # Phase 7: Other ML predictions
    crop_rec = crop_model.predict(soil, climate, location)
    risk = risk_model.predict(basic_features, soil, climate)

    # Phase 8: Urban vs Agricultural Conflict Analysis
    conflict = analyze_conflict(land_use, infra, location, urban_f, agri_f)

    # Phase 9: Simulations
    land_sim = simulate_best_land_use(basic_features, location, climate)
    top_crop = crop_rec["top_crops"][0]["crop"] if crop_rec["top_crops"] else "Wheat"
    rotation = suggest_rotation(top_crop)
    water = analyze_water_requirement(
        crop_rec["top_crops"][:3],
        climate.get("annual_rainfall", 800),
    )

    # Phase 10: Build comprehensive result
    result = {
        "coordinates": {"lat": lat, "lng": lng},
        "location": location,

        # ==========================================
        # LAND SUMMARY
        # ==========================================
        "land_summary": {
            "area_sqft": area_sqft,
            "area_acres": area_sqft / SQFT_PER_ACRE if area_sqft > 0 else 0,
            "land_type": land_use["predicted_use"],
            "land_type_confidence": round(max(land_use.get("probabilities", {}).values()) / 100, 2) if land_use.get("probabilities") else 0.5,
            "circle_rate": circle_rate.get("circle_rate"),
            "total_valuation": round(circle_rate.get("circle_rate", 0) * area_sqft) if area_sqft > 0 else None,
        },

        # ==========================================
        # CIRCLE RATE — Government (AUTHORITATIVE)
        # ==========================================
        "real_data": {
            "circle_rate": circle_rate.get("circle_rate"),
            "unit": circle_rate.get("unit", "INR/sq.ft"),
            "guideline_rate_per_sqft": circle_rate.get("circle_rate") or 0,
            "guideline_rate_per_acre": (circle_rate.get("circle_rate") or 0) * SQFT_PER_ACRE,
            "source": circle_rate.get("source", ""),
            "lookup_method": circle_rate.get("lookup_method", ""),
            "confidence_score": circle_rate.get("confidence_score", 0),
            "effective_date": circle_rate.get("effective_date", ""),
            "property_type": circle_rate.get("property_type", "residential"),
            "matched": circle_rate.get("matched", {}),
            "system_type": circle_rate.get("system_type", ""),
            "region_type_used": location.get("region_type", ""),
            "note": "Government registration data — single source of truth",
        },

        # ==========================================
        # ML CIRCLE RATE PREDICTION (learns govt logic)
        # ==========================================
        "ml_circle_rate": {
            "predicted_circle_rate": ml_circle_rate["predicted_circle_rate"],
            "unit": "INR/sq.ft",
            "confidence": ml_circle_rate["confidence"],
            "prediction_basis": ml_circle_rate["prediction_basis"],
            "model_type": ml_circle_rate["model_type"],
            "feature_importances": ml_circle_rate["feature_importances"],
            "label": "ML-predicted guideline value (learns govt valuation patterns)",
            "note": "Trained on TNREGINET data — approximates government valuation logic",
        },

        # ==========================================
        # ML FEATURES USED
        # ==========================================
        "ml_features": {
            "administrative": admin_f,
            "zoning": zoning_f,
            "infrastructure": infra_f,
            "urban_development": urban_f,
            "agricultural": agri_f,
        },

        # ==========================================
        # URBAN INTELLIGENCE
        # ==========================================
        "urban_intelligence": {
            "nearby_facilities": facilities.get("nearby_facilities", {}),
            "facility_counts": facilities.get("facility_counts", {}),
            "total_facilities": facilities.get("total_facilities", 0),
            "urban_suitability_index": facilities.get("urban_suitability_index", 0),
            "accessibility_score": facilities.get("accessibility_score", 0),
            "nearest_distances": facilities.get("nearest_distances", {}),
        },

        # ==========================================
        # AGRICULTURAL INTELLIGENCE
        # ==========================================
        "agricultural_intelligence": {
            "soil_type": soil.get("soil_type", ""),
            "soil_ph": soil.get("ph", 0),
            "organic_carbon": soil.get("organic_carbon", 0),
            "texture": soil.get("texture", ""),
            "crop_recommendations": crop_rec,
            "water_analysis": water,
            "crop_rotation": rotation,
            "agriculture_suitability": agri_f.get("agriculture_suitability_score", 0),
            "water_availability": agri_f.get("water_availability_index", 0),
        },

        # ==========================================
        # INVESTMENT INSIGHT
        # ==========================================
        "investment_insight": {
            "development_potential": urban_f.get("development_score", 0),
            "urbanization_index": urban_f.get("urbanization_index", 0),
            "conflict_analysis": conflict,
            "risk_analysis": risk,
            "land_use_comparison": land_sim,
            "zoning_risk": "HIGH" if conflict["conflict_level"] == "HIGH" else (
                "MEDIUM" if conflict["conflict_level"] == "MEDIUM" else "LOW"
            ),
        },

        # ==========================================
        # BACKWARD COMPATIBLE FIELDS
        # ==========================================
        "soil": soil,
        "climate": climate,
        "infrastructure": infra,
        "features": {
            "soil_quality_index": basic_features["soil_quality_index"],
            "climate_index": basic_features["climate_index"],
            "infrastructure_score": basic_features["infrastructure_score"],
            "urban_index": basic_features["urban_index"],
        },
        "ml_prediction": {
            "predicted_rate_per_sqft": ml_circle_rate["predicted_circle_rate"],
            "predicted_rate_per_acre": ml_circle_rate["predicted_circle_rate"] * SQFT_PER_ACRE,
            "predicted_rate_lakhs": round(ml_circle_rate["predicted_circle_rate"] * SQFT_PER_ACRE / 100000, 2),
            "model": ml_circle_rate["model_type"],
            "confidence": "high" if ml_circle_rate["confidence"] >= 0.8 else (
                "medium" if ml_circle_rate["confidence"] >= 0.5 else "low"
            ),
            "source": "TNREGINET-trained LightGBM",
            "feature_weights": ml_circle_rate["feature_importances"],
            "label": "ML Circle Rate Prediction",
            "note": "Trained on government data — learns valuation patterns, not market prices",
        },
        "predictions": {
            "land_use": land_use,
            "crop_recommendations": crop_rec,
            "risk_analysis": risk,
        },
        "simulations": {
            "land_use_comparison": land_sim,
            "crop_rotation": rotation,
            "water_analysis": water,
        },
    }

    # Phase 11: Store in MongoDB
    try:
        from database.connection import is_db_connected
        if is_db_connected():
            evaluation = Evaluation(
                latitude=lat,
                longitude=lng,
                state=location.get("state"),
                district=location.get("district"),
                region_type=location.get("region_type"),
                soil_type=soil.get("soil_type"),
                soil_ph=soil.get("ph"),
                soil_organic_carbon=soil.get("organic_carbon"),
                soil_texture=soil.get("texture"),
                avg_temperature=climate.get("avg_temperature"),
                annual_rainfall=climate.get("annual_rainfall"),
                climate_zone=climate.get("climate_zone"),
                infrastructure_score=basic_features["infrastructure_score"],
                nearest_road_km=infra.get("nearest_road_km"),
                nearest_market_km=infra.get("nearest_market_km"),
                predicted_land_rate=ml_circle_rate["predicted_circle_rate"] * SQFT_PER_ACRE,
                land_use_prediction=land_use.get("predicted_use"),
                risk_level=risk.get("risk_level"),
                recommended_crops=[c["crop"] for c in crop_rec.get("top_crops", [])],
                full_result=result,
            )
            await evaluation.insert()
            result["evaluation_id"] = str(evaluation.id)
        else:
            result["evaluation_id"] = None
    except Exception as e:
        print(f"DB save warning: {e}")
        result["evaluation_id"] = None

    return result
