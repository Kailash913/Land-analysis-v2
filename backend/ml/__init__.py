"""
ML package — preloads all models on startup.
"""
from ml.land_rate_predictor import LandRatePredictor
from ml.land_use_classifier import LandUseClassifier
from ml.crop_recommender import CropRecommender
from ml.risk_analyzer import RiskAnalyzer

# Singleton instances
land_rate_model = LandRatePredictor()
land_use_model = LandUseClassifier()
crop_model = CropRecommender()
risk_model = RiskAnalyzer()


def preload_models():
    """Train / load all ML models into memory on startup."""
    land_rate_model.train()
    land_use_model.train()
    crop_model.train()
    risk_model.train()
    print("All ML models preloaded")
