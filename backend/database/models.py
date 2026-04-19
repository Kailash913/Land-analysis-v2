"""
Beanie document models for MongoDB.
"""
import datetime
from typing import Optional, List, Dict, Any
from beanie import Document
from pydantic import Field


class Evaluation(Document):
    """Stores completed land evaluations."""
    latitude: float
    longitude: float
    state: Optional[str] = None
    district: Optional[str] = None
    region_type: Optional[str] = None

    # Environmental
    soil_type: Optional[str] = None
    soil_ph: Optional[float] = None
    soil_organic_carbon: Optional[float] = None
    soil_texture: Optional[str] = None
    avg_temperature: Optional[float] = None
    annual_rainfall: Optional[float] = None
    climate_zone: Optional[str] = None

    # Infrastructure
    infrastructure_score: Optional[float] = None
    nearest_road_km: Optional[float] = None
    nearest_market_km: Optional[float] = None

    # ML predictions
    predicted_land_rate: Optional[float] = None
    land_use_prediction: Optional[str] = None
    risk_level: Optional[str] = None
    recommended_crops: Optional[List[str]] = None

    # Full result
    full_result: Optional[Dict[str, Any]] = None

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Settings:
        name = "evaluations"


class AdminUser(Document):
    """Admin users for protected endpoints."""
    username: str
    password_hash: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Settings:
        name = "admin_users"


class LandRateDataset(Document):
    """Uploaded CSV dataset for base land rates by region."""
    state: Optional[str] = None
    district: Optional[str] = None
    base_rate_per_acre: Optional[float] = None
    year: Optional[int] = None
    source: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Settings:
        name = "land_rate_dataset"
