"""
ISRIC SoilGrids API integration — soil properties at any global coordinate.
"""
import httpx
from utils.cache import timed_cache

SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

# Soil texture classes from USDA classification
TEXTURE_MAP = {
    1: "Clay", 2: "Silty Clay", 3: "Sandy Clay",
    4: "Clay Loam", 5: "Silty Clay Loam", 6: "Sandy Clay Loam",
    7: "Loam", 8: "Silt Loam", 9: "Sandy Loam",
    10: "Silt", 11: "Loamy Sand", 12: "Sand",
}


@timed_cache(seconds=7200)
async def fetch_soil_data(lat: float, lng: float) -> dict:
    """
    Fetch soil pH, organic carbon, texture class from ISRIC SoilGrids.
    Returns processed soil summary.
    """
    params = {
        "lon": lng,
        "lat": lat,
        "property": ["phh2o", "ocd", "clay", "sand", "silt"],
        "depth": "0-30cm",
        "value": "mean",
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(SOILGRIDS_URL, params=params)

        if resp.status_code != 200:
            return _fallback_soil()

        data = resp.json()
        properties = data.get("properties", {}).get("layers", [])

        soil = {}
        for layer in properties:
            name = layer.get("name", "")
            depths = layer.get("depths", [{}])
            value = depths[0].get("values", {}).get("mean") if depths else None

            if name == "phh2o" and value is not None:
                soil["ph"] = round(value / 10, 1)  # SoilGrids stores pH * 10
            elif name == "ocd" and value is not None:
                soil["organic_carbon"] = round(value / 10, 2)  # g/kg → %
            elif name == "clay" and value is not None:
                soil["clay_pct"] = round(value / 10, 1)
            elif name == "sand" and value is not None:
                soil["sand_pct"] = round(value / 10, 1)
            elif name == "silt" and value is not None:
                soil["silt_pct"] = round(value / 10, 1)

        # Derive texture class
        soil["texture"] = _classify_texture(
            soil.get("clay_pct", 20),
            soil.get("sand_pct", 40),
            soil.get("silt_pct", 40),
        )

        # Derive soil type name
        soil["soil_type"] = _derive_soil_type(soil)

        return soil

    except Exception as e:
        print(f"SoilGrids error: {e}")
        return _fallback_soil()


def _classify_texture(clay: float, sand: float, silt: float) -> str:
    """Simplified USDA texture triangle classification."""
    if clay >= 40:
        return "Clay"
    elif silt >= 50 and clay >= 27:
        return "Silty Clay Loam"
    elif silt >= 50:
        return "Silt Loam"
    elif sand >= 70:
        return "Sandy Loam" if clay >= 10 else "Sand"
    elif clay >= 27:
        return "Clay Loam"
    else:
        return "Loam"


def _derive_soil_type(soil: dict) -> str:
    """Derive a readable soil type based on properties."""
    ph = soil.get("ph", 7.0)
    oc = soil.get("organic_carbon", 0.5)
    texture = soil.get("texture", "Loam")

    if "Clay" in texture and ph < 7.0:
        return "Black Cotton Soil (Regur)"
    elif "Sand" in texture:
        return "Sandy Arid Soil"
    elif ph > 7.5:
        return "Alkaline Alluvial Soil"
    elif oc > 1.5:
        return "Organic-Rich Laterite"
    elif "Loam" in texture:
        return "Alluvial Loam"
    else:
        return "Mixed Sedimentary Soil"


def _fallback_soil() -> dict:
    return {
        "ph": 6.8,
        "organic_carbon": 0.5,
        "clay_pct": 25.0,
        "sand_pct": 40.0,
        "silt_pct": 35.0,
        "texture": "Loam",
        "soil_type": "Alluvial Loam",
    }
