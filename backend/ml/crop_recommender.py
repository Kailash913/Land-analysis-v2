"""
Crop Recommendation — Decision Tree + rule-based hybrid.

Recommends crops based on soil, climate, and region.
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Comprehensive crop database
CROP_DATABASE = {
    "Rice": {"min_rain": 1000, "max_rain": 3000, "min_temp": 20, "max_temp": 35, "ideal_ph": (5.5, 7.0), "season": "Kharif (Jun-Oct)", "water_need": "High"},
    "Wheat": {"min_rain": 400, "max_rain": 1000, "min_temp": 10, "max_temp": 25, "ideal_ph": (6.0, 7.5), "season": "Rabi (Nov-Mar)", "water_need": "Moderate"},
    "Cotton": {"min_rain": 500, "max_rain": 1500, "min_temp": 20, "max_temp": 35, "ideal_ph": (6.0, 8.0), "season": "Kharif (Jun-Oct)", "water_need": "Moderate"},
    "Sugarcane": {"min_rain": 800, "max_rain": 2500, "min_temp": 20, "max_temp": 38, "ideal_ph": (5.5, 7.5), "season": "Year-round", "water_need": "Very High"},
    "Soybean": {"min_rain": 600, "max_rain": 1200, "min_temp": 20, "max_temp": 35, "ideal_ph": (6.0, 7.0), "season": "Kharif (Jun-Oct)", "water_need": "Moderate"},
    "Groundnut": {"min_rain": 500, "max_rain": 1200, "min_temp": 20, "max_temp": 35, "ideal_ph": (5.5, 7.0), "season": "Kharif (Jun-Oct)", "water_need": "Low"},
    "Maize": {"min_rain": 500, "max_rain": 1500, "min_temp": 18, "max_temp": 32, "ideal_ph": (5.5, 7.5), "season": "Kharif / Rabi", "water_need": "Moderate"},
    "Millets": {"min_rain": 300, "max_rain": 800, "min_temp": 22, "max_temp": 38, "ideal_ph": (5.5, 7.5), "season": "Kharif (Jun-Oct)", "water_need": "Low"},
    "Pulses": {"min_rain": 400, "max_rain": 900, "min_temp": 15, "max_temp": 30, "ideal_ph": (6.0, 7.5), "season": "Rabi (Nov-Mar)", "water_need": "Low"},
    "Tea": {"min_rain": 1500, "max_rain": 3000, "min_temp": 15, "max_temp": 28, "ideal_ph": (4.5, 5.5), "season": "Year-round", "water_need": "High"},
    "Coffee": {"min_rain": 1000, "max_rain": 2500, "min_temp": 15, "max_temp": 28, "ideal_ph": (5.0, 6.5), "season": "Year-round", "water_need": "High"},
    "Jute": {"min_rain": 1200, "max_rain": 2500, "min_temp": 24, "max_temp": 37, "ideal_ph": (5.5, 7.0), "season": "Kharif (Mar-Jul)", "water_need": "High"},
    "Mustard": {"min_rain": 300, "max_rain": 700, "min_temp": 10, "max_temp": 25, "ideal_ph": (6.0, 7.5), "season": "Rabi (Oct-Feb)", "water_need": "Low"},
    "Turmeric": {"min_rain": 800, "max_rain": 2000, "min_temp": 20, "max_temp": 35, "ideal_ph": (5.5, 7.0), "season": "Kharif (Jun-Jan)", "water_need": "Moderate"},
    "Coconut": {"min_rain": 1000, "max_rain": 3000, "min_temp": 22, "max_temp": 35, "ideal_ph": (5.5, 7.0), "season": "Year-round", "water_need": "High"},
}


class CropRecommender:
    def __init__(self):
        self._trained = False

    def train(self):
        """No explicit ML training — uses rule-based + scoring hybrid."""
        self._trained = True

    def predict(self, soil: dict, climate: dict, location: dict) -> dict:
        """
        Recommend top crops based on soil pH, rainfall, temperature, region.
        Returns ranked list with suitability scores.
        """
        ph = soil.get("ph", 6.8)
        rainfall = climate.get("annual_rainfall", 800)
        avg_temp = climate.get("avg_temperature", 25)
        state = location.get("state", "Unknown")

        recommendations = []

        for crop_name, profile in CROP_DATABASE.items():
            score = 0
            reasons = []

            # Rainfall match (0-30 points)
            if profile["min_rain"] <= rainfall <= profile["max_rain"]:
                score += 30
                reasons.append("Rainfall suitable")
            elif abs(rainfall - profile["min_rain"]) < 200 or abs(rainfall - profile["max_rain"]) < 200:
                score += 15
                reasons.append("Rainfall marginally suitable")

            # Temperature match (0-30 points)
            if profile["min_temp"] <= avg_temp <= profile["max_temp"]:
                score += 30
                reasons.append("Temperature ideal")
            elif abs(avg_temp - profile["min_temp"]) < 3 or abs(avg_temp - profile["max_temp"]) < 3:
                score += 15
                reasons.append("Temperature marginal")

            # pH match (0-25 points)
            ph_min, ph_max = profile["ideal_ph"]
            if ph_min <= ph <= ph_max:
                score += 25
                reasons.append("Soil pH optimal")
            elif abs(ph - ph_min) < 0.5 or abs(ph - ph_max) < 0.5:
                score += 12
                reasons.append("Soil pH acceptable")

            # Regional bonus (0-15 points)
            regional_bonus = _get_regional_bonus(crop_name, state)
            score += regional_bonus
            if regional_bonus > 0:
                reasons.append("Regional tradition")

            if score >= 40:
                recommendations.append({
                    "crop": crop_name,
                    "suitability_pct": min(100, score),
                    "season": profile["season"],
                    "water_need": profile["water_need"],
                    "reasons": reasons,
                })

        # Sort by suitability and take top 5
        recommendations.sort(key=lambda x: x["suitability_pct"], reverse=True)
        return {
            "top_crops": recommendations[:5],
            "total_suitable": len(recommendations),
            "model": "RuleBasedHybrid",
        }


def _get_regional_bonus(crop: str, state: str) -> int:
    """Give bonus points for crops traditionally grown in a state."""
    REGIONAL_CROPS = {
        "Tamil Nadu": ["Rice", "Sugarcane", "Coconut", "Turmeric", "Cotton"],
        "Punjab": ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize"],
        "Maharashtra": ["Cotton", "Soybean", "Sugarcane", "Groundnut", "Pulses"],
        "Kerala": ["Coconut", "Rice", "Tea", "Coffee", "Rubber"],
        "Karnataka": ["Coffee", "Rice", "Sugarcane", "Maize", "Cotton"],
        "West Bengal": ["Rice", "Jute", "Tea", "Pulses", "Maize"],
        "Rajasthan": ["Mustard", "Millets", "Pulses", "Groundnut", "Wheat"],
        "Gujarat": ["Cotton", "Groundnut", "Wheat", "Sugarcane", "Millets"],
        "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane", "Pulses", "Mustard"],
        "Madhya Pradesh": ["Soybean", "Wheat", "Pulses", "Cotton", "Maize"],
        "Andhra Pradesh": ["Rice", "Cotton", "Groundnut", "Turmeric", "Sugarcane"],
        "Telangana": ["Rice", "Cotton", "Maize", "Turmeric", "Soybean"],
        "Bihar": ["Rice", "Wheat", "Maize", "Pulses", "Sugarcane"],
        "Assam": ["Tea", "Rice", "Jute", "Sugarcane", "Maize"],
        "Haryana": ["Wheat", "Rice", "Sugarcane", "Cotton", "Mustard"],
        "Odisha": ["Rice", "Groundnut", "Pulses", "Sugarcane", "Jute"],
    }
    if state in REGIONAL_CROPS and crop in REGIONAL_CROPS[state]:
        return 15
    return 0
