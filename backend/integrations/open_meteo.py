"""
Open-Meteo API integration — climate and elevation data.
"""
import httpx
from utils.cache import timed_cache

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"


@timed_cache(seconds=3600)
async def fetch_climate_data(lat: float, lng: float) -> dict:
    """
    Fetch current temperature, precipitation, elevation, and historical averages.
    """
    # Current conditions + elevation
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": "temperature_2m,precipitation",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(FORECAST_URL, params=params)

        if resp.status_code != 200:
            return _fallback()

        data = resp.json()
        current = data.get("current", {})

        result = {
            "elevation": data.get("elevation", 0),
            "current_temp": current.get("temperature_2m", 25),
            "current_precipitation": current.get("precipitation", 0),
        }

        # Fetch historical averages (last year)
        hist = await _fetch_historical_averages(lat, lng)
        result.update(hist)

        # Derive climate zone
        result["climate_zone"] = _classify_climate(
            result.get("avg_temperature", 25),
            result.get("annual_rainfall", 800),
        )

        return result

    except Exception as e:
        print(f"Open-Meteo error: {e}")
        return _fallback()


async def _fetch_historical_averages(lat: float, lng: float) -> dict:
    """Fetch last year's averages for temperature and rainfall."""
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "daily": "temperature_2m_mean,precipitation_sum",
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(HISTORICAL_URL, params=params)

        if resp.status_code != 200:
            return {"avg_temperature": 25, "annual_rainfall": 800}

        data = resp.json()
        daily = data.get("daily", {})

        temps = [t for t in (daily.get("temperature_2m_mean") or []) if t is not None]
        precips = [p for p in (daily.get("precipitation_sum") or []) if p is not None]

        return {
            "avg_temperature": round(sum(temps) / len(temps), 1) if temps else 25,
            "annual_rainfall": round(sum(precips), 1) if precips else 800,
        }

    except Exception:
        return {"avg_temperature": 25, "annual_rainfall": 800}


def _classify_climate(avg_temp: float, rainfall: float) -> str:
    """Simplified Köppen-style climate classification."""
    if rainfall > 2000:
        return "Tropical Wet"
    elif rainfall > 1000 and avg_temp > 22:
        return "Tropical Wet & Dry"
    elif rainfall > 600 and avg_temp > 20:
        return "Tropical Savanna"
    elif rainfall > 500:
        return "Subtropical Humid"
    elif avg_temp > 25 and rainfall < 500:
        return "Arid / Desert"
    elif avg_temp < 15:
        return "Temperate / Highland"
    else:
        return "Semi-Arid"


def _fallback() -> dict:
    return {
        "elevation": 0,
        "current_temp": 25,
        "current_precipitation": 0,
        "avg_temperature": 25,
        "annual_rainfall": 800,
        "climate_zone": "Tropical Savanna",
    }
