"""
Overpass API integration — nearby infrastructure from OpenStreetMap.
"""
import math
import httpx
from utils.cache import timed_cache

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


@timed_cache(seconds=3600)
async def fetch_infrastructure(lat: float, lng: float) -> dict:
    """
    Fetch nearby roads, railways, markets, settlements within 5 km.
    Returns infrastructure analysis with distances and score.
    """
    radius = 5000  # meters
    query = f"""
    [out:json][timeout:10];
    (
      node["railway"="station"](around:{radius},{lat},{lng});
      node["amenity"~"marketplace|school|hospital|bank"](around:{radius},{lat},{lng});
      way["highway"~"trunk|primary|secondary"](around:{radius},{lat},{lng});
      node["place"~"town|city"](around:{radius},{lat},{lng});
    );
    out center 10;
    """

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(OVERPASS_URL, params={"data": query})

        if resp.status_code != 200:
            return _fallback()

        data = resp.json()
        elements = data.get("elements", [])

        landmarks = []
        nearest_road_km = 99.0
        nearest_market_km = 99.0
        nearest_settlement_km = 99.0

        for el in elements:
            tags = el.get("tags", {})
            el_lat = el.get("center", {}).get("lat") or el.get("lat")
            el_lng = el.get("center", {}).get("lon") or el.get("lon")

            if not el_lat or not el_lng:
                continue

            dist_km = _haversine(lat, lng, el_lat, el_lng)
            name = tags.get("name") or tags.get("ref") or "Unnamed"

            # Categorize
            if "highway" in tags:
                nearest_road_km = min(nearest_road_km, dist_km)
                if not any(l["name"] == name for l in landmarks):
                    landmarks.append({"name": name, "type": "road", "dist_km": round(dist_km, 1)})
            elif "railway" in tags:
                if not any(l["name"] == name for l in landmarks):
                    landmarks.append({"name": name, "type": "railway", "dist_km": round(dist_km, 1)})
            elif tags.get("amenity") == "marketplace":
                nearest_market_km = min(nearest_market_km, dist_km)
                if not any(l["name"] == name for l in landmarks):
                    landmarks.append({"name": name, "type": "market", "dist_km": round(dist_km, 1)})
            elif tags.get("place") in ("town", "city"):
                nearest_settlement_km = min(nearest_settlement_km, dist_km)
                if not any(l["name"] == name for l in landmarks):
                    landmarks.append({"name": name, "type": "settlement", "dist_km": round(dist_km, 1)})
            else:
                if not any(l["name"] == name for l in landmarks):
                    landmarks.append({"name": name, "type": "amenity", "dist_km": round(dist_km, 1)})

        # Sort by distance, take top 6
        landmarks.sort(key=lambda x: x["dist_km"])
        landmarks = landmarks[:6]

        # Compute infrastructure score (0-100)
        score = _compute_infra_score(nearest_road_km, nearest_market_km, nearest_settlement_km, len(elements))

        return {
            "landmarks": landmarks,
            "nearest_road_km": round(nearest_road_km, 2) if nearest_road_km < 99 else None,
            "nearest_market_km": round(nearest_market_km, 2) if nearest_market_km < 99 else None,
            "nearest_settlement_km": round(nearest_settlement_km, 2) if nearest_settlement_km < 99 else None,
            "infrastructure_score": score,
            "total_amenities": len(elements),
        }

    except Exception as e:
        print(f"Overpass error: {e}")
        return _fallback()


def _compute_infra_score(road_km: float, market_km: float, settlement_km: float, total: int) -> float:
    """Score from 0-100 based on proximity to infrastructure."""
    road_score = max(0, 30 - (road_km * 6)) if road_km < 99 else 5
    market_score = max(0, 25 - (market_km * 5)) if market_km < 99 else 5
    settlement_score = max(0, 25 - (settlement_km * 5)) if settlement_km < 99 else 5
    density_score = min(20, total * 2)
    return round(min(100, max(0, road_score + market_score + settlement_score + density_score)), 1)


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distance in km between two coordinates."""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _fallback() -> dict:
    return {
        "landmarks": [],
        "nearest_road_km": None,
        "nearest_market_km": None,
        "nearest_settlement_km": None,
        "infrastructure_score": 40.0,
        "total_amenities": 0,
    }
