"""
Enhanced Overpass API — Radius-based facility detection.

Queries facilities within specific radii:
  hospitals:  3 km
  schools:    2 km
  markets:    2 km
  highways:   5 km
  metro/rail: 5 km

Returns:
  nearby_facilities: categorized facility list with distances
  urban_suitability_index: composite score (0-100)
  facility_counts: per-category counts
"""
import math
import httpx
from utils.cache import timed_cache

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Facility detection configuration
FACILITY_CONFIG = {
    "hospitals":  {"radius": 3000, "query": 'node["amenity"="hospital"]', "weight": 20},
    "schools":    {"radius": 2000, "query": 'node["amenity"~"school|university|college"]', "weight": 15},
    "markets":    {"radius": 2000, "query": 'node["amenity"~"marketplace|supermarket"]', "weight": 15},
    "highways":   {"radius": 5000, "query": 'way["highway"~"trunk|motorway|primary"]', "weight": 20},
    "metro_rail": {"radius": 5000, "query": 'node["railway"~"station|halt"]', "weight": 15},
    "banks":      {"radius": 2000, "query": 'node["amenity"="bank"]', "weight": 5},
    "bus":        {"radius": 3000, "query": 'node["amenity"="bus_station"]', "weight": 5},
    "fuel":       {"radius": 3000, "query": 'node["amenity"="fuel"]', "weight": 5},
}


@timed_cache(seconds=3600)
async def fetch_facilities(lat: float, lng: float) -> dict:
    """
    Fetch nearby facilities within specified radii.
    Returns categorized facilities, counts, and urban suitability index.
    """
    # Build a single Overpass query combining all facility types
    parts = []
    max_radius = 5000
    for ftype, config in FACILITY_CONFIG.items():
        r = config["radius"]
        q = config["query"]
        parts.append(f'  {q}(around:{r},{lat},{lng});')

    query = f"""
    [out:json][timeout:15];
    (
    {chr(10).join(parts)}
    );
    out center 20;
    """

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(OVERPASS_URL, params={"data": query})

        if resp.status_code != 200:
            return _fallback()

        data = resp.json()
        elements = data.get("elements", [])

        # Categorize results
        facilities = {k: [] for k in FACILITY_CONFIG}
        for el in elements:
            tags = el.get("tags", {})
            el_lat = el.get("center", {}).get("lat") or el.get("lat")
            el_lng = el.get("center", {}).get("lon") or el.get("lon")
            if not el_lat or not el_lng:
                continue

            dist_km = _haversine(lat, lng, el_lat, el_lng)
            name = tags.get("name") or tags.get("ref") or "Unnamed"

            # Classify into category
            amenity = tags.get("amenity", "")
            highway = tags.get("highway", "")
            railway = tags.get("railway", "")

            if amenity == "hospital":
                _add_facility(facilities, "hospitals", name, dist_km, 3.0)
            elif amenity in ("school", "university", "college"):
                _add_facility(facilities, "schools", name, dist_km, 2.0)
            elif amenity in ("marketplace", "supermarket"):
                _add_facility(facilities, "markets", name, dist_km, 2.0)
            elif highway in ("trunk", "motorway", "primary"):
                _add_facility(facilities, "highways", name, dist_km, 5.0)
            elif railway in ("station", "halt"):
                _add_facility(facilities, "metro_rail", name, dist_km, 5.0)
            elif amenity == "bank":
                _add_facility(facilities, "banks", name, dist_km, 2.0)
            elif amenity == "bus_station":
                _add_facility(facilities, "bus", name, dist_km, 3.0)
            elif amenity == "fuel":
                _add_facility(facilities, "fuel", name, dist_km, 3.0)

        # Sort each category by distance
        for cat in facilities:
            facilities[cat].sort(key=lambda x: x["distance_km"])

        # Compute counts and scores
        facility_counts = {k: len(v) for k, v in facilities.items()}
        total_facilities = sum(facility_counts.values())

        # Urban suitability index (0-100)
        urban_suit_score = _compute_urban_suitability(facilities, facility_counts)

        # Accessibility score (based on nearest facility in each category)
        accessibility = _compute_accessibility(facilities)

        # Nearest distances
        nearest = {}
        for cat, items in facilities.items():
            if items:
                nearest[f"nearest_{cat}_km"] = items[0]["distance_km"]
            else:
                nearest[f"nearest_{cat}_km"] = None

        return {
            "nearby_facilities": facilities,
            "facility_counts": facility_counts,
            "total_facilities": total_facilities,
            "urban_suitability_index": urban_suit_score,
            "accessibility_score": accessibility,
            "nearest_distances": nearest,
        }

    except Exception as e:
        print(f"Facility detection error: {e}")
        return _fallback()


def _add_facility(facilities: dict, category: str, name: str, dist: float, max_radius: float):
    """Add a facility if within radius and not duplicate."""
    if dist <= max_radius and not any(f["name"] == name for f in facilities[category]):
        facilities[category].append({
            "name": name,
            "distance_km": round(dist, 2),
        })


def _compute_urban_suitability(facilities: dict, counts: dict) -> float:
    """Compute urban suitability index (0-100)."""
    score = 0
    for cat, config in FACILITY_CONFIG.items():
        weight = config["weight"]
        count = counts.get(cat, 0)
        items = facilities.get(cat, [])

        if count > 0:
            # Score based on count and proximity
            nearest_dist = items[0]["distance_km"] if items else 99
            proximity_bonus = max(0, 1 - nearest_dist / (config["radius"] / 1000))
            score += weight * min(1.0, count / 3 * 0.6 + proximity_bonus * 0.4)

    return round(min(100, score), 1)


def _compute_accessibility(facilities: dict) -> float:
    """Compute accessibility score (0-100) based on nearest facility distances."""
    scores = []
    for cat, items in facilities.items():
        if items:
            nearest = items[0]["distance_km"]
            # Closer = higher score
            s = max(0, 100 - nearest * 20)
            scores.append(s)
        else:
            scores.append(10)  # No facility = low score

    return round(sum(scores) / max(len(scores), 1), 1)


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _fallback():
    return {
        "nearby_facilities": {k: [] for k in FACILITY_CONFIG},
        "facility_counts": {k: 0 for k in FACILITY_CONFIG},
        "total_facilities": 0,
        "urban_suitability_index": 30.0,
        "accessibility_score": 30.0,
        "nearest_distances": {f"nearest_{k}_km": None for k in FACILITY_CONFIG},
    }
