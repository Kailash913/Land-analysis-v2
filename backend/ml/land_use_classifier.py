"""
Land Use Classification — Decision Tree model.

Classifies the best land use category: Agriculture, Residential, or Commercial.
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


LABELS = ["Agriculture", "Residential", "Commercial"]


class LandUseClassifier:
    def __init__(self):
        self.model = DecisionTreeClassifier(max_depth=5, random_state=42)
        self._trained = False

    def train(self):
        """Train on synthetic dataset."""
        # Features: [soil_qi, climate_i, infra_score, urban_index]
        X = np.array([
            # Agriculture — good soil, low urban
            [85, 80, 30, 15], [90, 75, 25, 15], [80, 85, 35, 15],
            [75, 70, 40, 20], [70, 65, 30, 15], [85, 90, 20, 10],
            [60, 60, 45, 25], [65, 70, 35, 20],
            # Residential — moderate soil, high urban
            [50, 55, 70, 70], [40, 50, 75, 80], [45, 60, 65, 65],
            [55, 45, 80, 75], [35, 40, 85, 85], [60, 55, 60, 60],
            [30, 50, 70, 70], [45, 55, 75, 75],
            # Commercial — low soil, very high urban + infra
            [20, 30, 90, 95], [25, 35, 95, 90], [15, 25, 92, 95],
            [30, 40, 88, 85], [20, 30, 85, 90], [10, 20, 98, 95],
            [25, 35, 90, 90], [15, 25, 95, 95],
        ])

        y = np.array([
            0, 0, 0, 0, 0, 0, 0, 0,      # Agriculture
            1, 1, 1, 1, 1, 1, 1, 1,      # Residential
            2, 2, 2, 2, 2, 2, 2, 2,      # Commercial
        ])

        self.model.fit(X, y)
        self._trained = True

    def predict(self, features: dict) -> dict:
        """Predict best land use and return probabilities for all classes."""
        if not self._trained:
            self.train()

        arr = np.array([[
            features["soil_quality_index"],
            features["climate_index"],
            features["infrastructure_score"],
            features["urban_index"],
        ]])

        predicted = int(self.model.predict(arr)[0])
        probas = self.model.predict_proba(arr)[0]

        return {
            "predicted_use": LABELS[predicted],
            "probabilities": {
                LABELS[i]: round(float(p) * 100, 1) for i, p in enumerate(probas)
            },
            "model": "DecisionTreeClassifier",
        }
