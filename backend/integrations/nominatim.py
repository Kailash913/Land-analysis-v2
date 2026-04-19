"""
Nominatim integration — enhanced reverse geocoding via OpenStreetMap.

Extracts full administrative hierarchy:
  state → district → taluk → village → street → locality
"""
import httpx
from utils.cache import timed_cache

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
HEADERS = {"User-Agent": "LRESApp/1.0 (academic project)"}


@timed_cache(seconds=3600)
async def reverse_geocode(lat: float, lng: float) -> dict:
    """
    Convert lat/lng → full administrative hierarchy.

    Returns: state, district, taluk, village, street, suburb, locality,
             region_type, display_name
    """
    # Use zoom=18 for maximum address detail (street-level)
    params = {"format": "jsonv2", "lat": lat, "lon": lng, "zoom": 18, "addressdetails": 1}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(NOMINATIM_URL, params=params, headers=HEADERS)

    if resp.status_code != 200:
        return _default_location()

    data = resp.json()
    address = data.get("address", {})

    # --- Extract administrative hierarchy ---
    state = address.get("state") or address.get("region") or "Unknown State"

    district = (
        address.get("state_district")
        or address.get("county")
        or address.get("city")
        or "Unknown District"
    )

    # Taluk — often in county or city_district
    taluk = (
        address.get("county")
        or address.get("city_district")
        or address.get("state_district")
        or ""
    )

    # Village / town
    village = (
        address.get("village")
        or address.get("town")
        or address.get("city")
        or address.get("suburb")
        or ""
    )

    # Street
    street = (
        address.get("road")
        or address.get("pedestrian")
        or address.get("footway")
        or ""
    )

    # Suburb / locality
    suburb = address.get("suburb") or address.get("neighbourhood") or ""
    locality = address.get("neighbourhood") or address.get("hamlet") or ""

    # Region type heuristic
    has_urban_markers = any(address.get(k) for k in ("city", "town", "suburb", "residential"))
    if has_urban_markers:
        region_type = "urban"
    elif address.get("village") or address.get("hamlet"):
        region_type = "rural"
    else:
        region_type = "semi-urban"

    return {
        "state": state,
        "district": district,
        "taluk": taluk,
        "village": village,
        "street": street,
        "suburb": suburb,
        "locality": locality,
        "region_type": region_type,
        "display_name": data.get("display_name", ""),
        "raw_address": address,
    }


def _default_location():
    return {
        "state": "Unknown",
        "district": "Unknown",
        "taluk": "",
        "village": "",
        "street": "",
        "suburb": "",
        "locality": "",
        "region_type": "unknown",
        "display_name": "",
        "raw_address": {},
    }
