"""
Risk Analysis — Logistic Regression model.

Evaluates investment risk: Low / Medium / High.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression


RISK_LEVELS = ["Low", "Medium", "High"]

# Risk factor descriptions
RISK_FACTORS_MAP = {
    "low_rainfall": "Insufficient rainfall for agriculture",
    "high_rainfall": "Flood risk due to excessive rainfall",
    "poor_soil": "Soil quality below optimal threshold",
    "low_infrastructure": "Limited road/market access",
    "extreme_temp": "Temperature outside ideal range",
    "data_incomplete": "Some data points unavailable",
    "arid_zone": "Arid/desert climate zone",
    "urban_pressure": "High urbanization may affect land use",
}


class RiskAnalyzer:
    def __init__(self):
        self.model = LogisticRegression(max_iter=500, random_state=42)
        self._trained = False

    def train(self):
        """Train on synthetic risk dataset."""
        # Features: [rainfall_var, infra_distance, soil_qi, climate_i, urban_i]
        # rainfall_var: deviation from ideal (800mm)
        X = np.array([
            # Low risk — good everything
            [10, 20, 80, 80, 40], [5, 15, 85, 75, 30], [15, 25, 75, 85, 50],
            [8, 10, 90, 70, 20], [12, 18, 82, 78, 35], [6, 12, 88, 82, 25],
            [10, 22, 78, 76, 45], [7, 14, 86, 80, 30],
            # Medium risk — mixed signals
            [30, 50, 55, 55, 50], [40, 45, 50, 60, 60], [25, 55, 60, 45, 40],
            [35, 60, 45, 50, 55], [20, 40, 65, 40, 45], [45, 35, 40, 55, 65],
            [28, 48, 58, 48, 50], [38, 52, 48, 52, 58],
            # High risk — poor conditions
            [60, 80, 20, 20, 15], [70, 90, 15, 15, 10], [55, 75, 25, 30, 20],
            [80, 85, 10, 10, 5], [65, 70, 30, 25, 15], [75, 95, 12, 18, 8],
            [58, 78, 22, 22, 18], [72, 88, 14, 14, 12],
        ])

        y = np.array([
            0, 0, 0, 0, 0, 0, 0, 0,  # Low
            1, 1, 1, 1, 1, 1, 1, 1,  # Medium
            2, 2, 2, 2, 2, 2, 2, 2,  # High
        ])

        self.model.fit(X, y)
        self._trained = True

    def predict(self, features: dict, soil: dict, climate: dict) -> dict:
        """Analyze risk and return level + contributing factors."""
        if not self._trained:
            self.train()

        rainfall = climate.get("annual_rainfall", 800)
        soil_qi = features["soil_quality_index"]
        climate_i = features["climate_index"]
        infra = features["infrastructure_score"]
        urban = features["urban_index"]

        # Rainfall variability from ideal
        rainfall_var = abs(rainfall - 900) / 30  # normalize

        arr = np.array([[rainfall_var, 100 - infra, soil_qi, climate_i, urban]])
        predicted = int(self.model.predict(arr)[0])
        probas = self.model.predict_proba(arr)[0]

        # Determine contributing risk factors
        risk_factors = []
        if rainfall < 400:
            risk_factors.append(RISK_FACTORS_MAP["low_rainfall"])
        if rainfall > 2500:
            risk_factors.append(RISK_FACTORS_MAP["high_rainfall"])
        if soil_qi < 40:
            risk_factors.append(RISK_FACTORS_MAP["poor_soil"])
        if infra < 30:
            risk_factors.append(RISK_FACTORS_MAP["low_infrastructure"])
        if climate_i < 35:
            risk_factors.append(RISK_FACTORS_MAP["extreme_temp"])
        if climate.get("climate_zone", "").startswith("Arid"):
            risk_factors.append(RISK_FACTORS_MAP["arid_zone"])
        if urban > 80:
            risk_factors.append(RISK_FACTORS_MAP["urban_pressure"])
        if not risk_factors:
            risk_factors.append("No significant risk factors identified")

        # Risk score 0-100
        risk_score = round(probas[1] * 30 + probas[2] * 70 + (10 if len(risk_factors) > 2 else 0), 1)
        risk_score = min(100, risk_score)

        return {
            "risk_level": RISK_LEVELS[predicted],
            "risk_score": risk_score,
            "probabilities": {
                RISK_LEVELS[i]: round(float(p) * 100, 1) for i, p in enumerate(probas)
            },
            "risk_factors": risk_factors,
            "model": "LogisticRegression",
        }
