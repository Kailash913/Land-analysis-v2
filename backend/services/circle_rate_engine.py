"""
Circle Rate Engine — Geospatial lookup + government valuation database.

NOT a prediction model. This is a LOOKUP ENGINE that:
1. Takes coordinates → reverse geocode → admin hierarchy
2. Matches to TNREGINET guideline value database
3. Returns validated circle rate with confidence score

AI role is limited to:
  - Normalizing user input addresses
  - Resolving ambiguous locations
  - Detecting mismatched zones
  - Providing confidence score
  - Explaining valuation source

AI does NOT fabricate land values.
"""
from integrations.tn_guideline_values import lookup_tn_guideline_value, SOURCE, EFFECTIVE_DATE
from integrations.guideline_rates import lookup_guideline_rate


def lookup_circle_rate(location: dict, property_type: str = "residential") -> dict:
    """
    Master circle rate lookup — routes to the correct state engine.

    For Tamil Nadu → uses TNREGINET (street/village/taluk matching)
    For other states → uses the generic guideline rate lookup
    """
    state = location.get("state", "")

    if _is_tamil_nadu(state):
        return _tn_lookup(location, property_type)
    else:
        return _generic_lookup(location)


def _is_tamil_nadu(state: str) -> bool:
    """Check if state is Tamil Nadu (handles variations)."""
    s = state.lower().strip()
    return s in ("tamil nadu", "tamilnadu", "tn")


def _tn_lookup(location: dict, property_type: str) -> dict:
    """
    Tamil Nadu circle rate lookup using TNREGINET data.

    Pipeline:
      lat/lng → reverse geocode → admin mapping → spatial match → guideline value
    """
    district = location.get("district", "")
    taluk = location.get("taluk", "") or location.get("county", "")
    village = (
        location.get("village", "")
        or location.get("suburb", "")
        or location.get("locality", "")
    )
    street = location.get("street", "")

    # Run TNREGINET hierarchical lookup
    result = lookup_tn_guideline_value(
        district=district,
        taluk=taluk,
        village=village,
        street=street,
        property_type=property_type,
    )

    # Enrich with location context
    result["state"] = "Tamil Nadu"
    result["input_location"] = {
        "district": district,
        "taluk": taluk,
        "village": village,
        "street": street,
    }
    result["system_type"] = "TNREGINET Spatial Lookup"

    return result


def _generic_lookup(location: dict) -> dict:
    """
    Non-TN states: use the existing generic guideline rates.
    Wraps the output in the new circle_rate response format.
    """
    state = location.get("state", "")
    district = location.get("district", "")
    region_type = location.get("region_type", "semi-urban")

    old = lookup_guideline_rate(state, district, region_type)

    return {
        "circle_rate": old["guideline_rate_per_sqft"],
        "unit": "INR/sq.ft",
        "source": old["source"],
        "lookup_method": "State-District Lookup",
        "confidence_score": 0.60,
        "effective_date": "2024-01-01",
        "property_type": "residential",
        "property_type_multiplier": 1.0,
        "base_residential_rate": old["guideline_rate_per_sqft"],
        "matched": {
            "district": district,
            "taluk": "",
            "village": "",
            "street": "",
        },
        "state": state,
        "input_location": {
            "district": district,
            "taluk": "",
            "village": "",
            "street": "",
        },
        "system_type": "Generic State Guideline",
    }
