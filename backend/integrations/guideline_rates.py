"""
Government Guideline Land Rate Dataset — taluk/district level.

These are approximate circle/guideline rates from state government registrations
(e.g., Karnataka Bhoomi, TN IGRS, MH IGR) — representative values in ₹/sq.ft.

1 acre = 43,560 sq.ft
"""

# Format: state → district → { urban_rate, semi_urban_rate, rural_rate } in ₹/sq.ft
GUIDELINE_RATES = {
    "Karnataka": {
        "Bengaluru Urban": {"urban": 8500, "semi-urban": 4200, "rural": 1800},
        "Bengaluru Rural": {"urban": 3500, "semi-urban": 1800, "rural": 800},
        "Mysuru": {"urban": 4200, "semi-urban": 2000, "rural": 700},
        "Mangaluru": {"urban": 5500, "semi-urban": 2500, "rural": 900},
        "Hubballi-Dharwad": {"urban": 3200, "semi-urban": 1500, "rural": 500},
        "Belagavi": {"urban": 2800, "semi-urban": 1200, "rural": 450},
        "Kalaburagi": {"urban": 2000, "semi-urban": 900, "rural": 350},
        "Davanagere": {"urban": 2200, "semi-urban": 1000, "rural": 400},
        "Shivamogga": {"urban": 2500, "semi-urban": 1100, "rural": 500},
        "Tumakuru": {"urban": 2800, "semi-urban": 1400, "rural": 600},
        "Raichur": {"urban": 1600, "semi-urban": 700, "rural": 300},
        "Hassan": {"urban": 2200, "semi-urban": 1000, "rural": 450},
        "Udupi": {"urban": 4500, "semi-urban": 2200, "rural": 1000},
        "Chikkamagaluru": {"urban": 2800, "semi-urban": 1300, "rural": 500},
        "Mandya": {"urban": 2000, "semi-urban": 900, "rural": 400},
        "Ramanagara": {"urban": 3000, "semi-urban": 1600, "rural": 700},
        "_default": {"urban": 2200, "semi-urban": 1000, "rural": 400},
    },
    "Tamil Nadu": {
        "Chennai": {"urban": 12000, "semi-urban": 6000, "rural": 2500},
        "Coimbatore": {"urban": 5500, "semi-urban": 2800, "rural": 1000},
        "Madurai": {"urban": 4000, "semi-urban": 2000, "rural": 700},
        "Tiruchirappalli": {"urban": 3500, "semi-urban": 1600, "rural": 600},
        "Salem": {"urban": 3200, "semi-urban": 1500, "rural": 500},
        "Tirunelveli": {"urban": 2800, "semi-urban": 1200, "rural": 450},
        "Erode": {"urban": 3000, "semi-urban": 1400, "rural": 500},
        "Vellore": {"urban": 3500, "semi-urban": 1600, "rural": 600},
        "Thanjavur": {"urban": 2500, "semi-urban": 1200, "rural": 500},
        "Kanchipuram": {"urban": 7000, "semi-urban": 3500, "rural": 1200},
        "Tiruvallur": {"urban": 6500, "semi-urban": 3200, "rural": 1100},
        "_default": {"urban": 3000, "semi-urban": 1400, "rural": 550},
    },
    "Maharashtra": {
        "Mumbai": {"urban": 25000, "semi-urban": 12000, "rural": 5000},
        "Mumbai Suburban": {"urban": 20000, "semi-urban": 10000, "rural": 4000},
        "Pune": {"urban": 8000, "semi-urban": 4000, "rural": 1500},
        "Thane": {"urban": 10000, "semi-urban": 5000, "rural": 2000},
        "Nagpur": {"urban": 4500, "semi-urban": 2200, "rural": 800},
        "Nashik": {"urban": 3800, "semi-urban": 1800, "rural": 700},
        "Aurangabad": {"urban": 3200, "semi-urban": 1500, "rural": 600},
        "Kolhapur": {"urban": 3000, "semi-urban": 1400, "rural": 550},
        "Solapur": {"urban": 2500, "semi-urban": 1200, "rural": 450},
        "Navi Mumbai": {"urban": 9000, "semi-urban": 4500, "rural": 1800},
        "_default": {"urban": 3500, "semi-urban": 1600, "rural": 600},
    },
    "Telangana": {
        "Hyderabad": {"urban": 10000, "semi-urban": 5000, "rural": 2000},
        "Rangareddy": {"urban": 7000, "semi-urban": 3500, "rural": 1200},
        "Medchal-Malkajgiri": {"urban": 8000, "semi-urban": 4000, "rural": 1500},
        "Warangal": {"urban": 3000, "semi-urban": 1400, "rural": 500},
        "Karimnagar": {"urban": 2500, "semi-urban": 1200, "rural": 450},
        "Nalgonda": {"urban": 2200, "semi-urban": 1000, "rural": 400},
        "Nizamabad": {"urban": 2000, "semi-urban": 900, "rural": 350},
        "_default": {"urban": 2500, "semi-urban": 1200, "rural": 450},
    },
    "Andhra Pradesh": {
        "Visakhapatnam": {"urban": 5500, "semi-urban": 2800, "rural": 1000},
        "Vijayawada": {"urban": 5000, "semi-urban": 2500, "rural": 900},
        "Guntur": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "Tirupati": {"urban": 4000, "semi-urban": 2000, "rural": 800},
        "Kakinada": {"urban": 3000, "semi-urban": 1500, "rural": 600},
        "Nellore": {"urban": 2800, "semi-urban": 1300, "rural": 500},
        "Kurnool": {"urban": 2200, "semi-urban": 1000, "rural": 400},
        "Anantapur": {"urban": 2000, "semi-urban": 900, "rural": 350},
        "_default": {"urban": 2500, "semi-urban": 1200, "rural": 450},
    },
    "Kerala": {
        "Thiruvananthapuram": {"urban": 7000, "semi-urban": 3500, "rural": 1500},
        "Kochi": {"urban": 9000, "semi-urban": 4500, "rural": 2000},
        "Kozhikode": {"urban": 6000, "semi-urban": 3000, "rural": 1200},
        "Thrissur": {"urban": 5500, "semi-urban": 2800, "rural": 1200},
        "Kannur": {"urban": 4500, "semi-urban": 2200, "rural": 900},
        "Kollam": {"urban": 4000, "semi-urban": 2000, "rural": 800},
        "Alappuzha": {"urban": 5000, "semi-urban": 2500, "rural": 1000},
        "Palakkad": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "_default": {"urban": 5000, "semi-urban": 2500, "rural": 1000},
    },
    "Gujarat": {
        "Ahmedabad": {"urban": 6000, "semi-urban": 3000, "rural": 1200},
        "Surat": {"urban": 5500, "semi-urban": 2800, "rural": 1000},
        "Vadodara": {"urban": 4000, "semi-urban": 2000, "rural": 800},
        "Rajkot": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "Gandhinagar": {"urban": 5000, "semi-urban": 2500, "rural": 1000},
        "_default": {"urban": 3000, "semi-urban": 1500, "rural": 600},
    },
    "Rajasthan": {
        "Jaipur": {"urban": 5000, "semi-urban": 2500, "rural": 900},
        "Jodhpur": {"urban": 3000, "semi-urban": 1500, "rural": 500},
        "Udaipur": {"urban": 3500, "semi-urban": 1800, "rural": 600},
        "Kota": {"urban": 2800, "semi-urban": 1400, "rural": 500},
        "Ajmer": {"urban": 2500, "semi-urban": 1200, "rural": 450},
        "_default": {"urban": 2000, "semi-urban": 1000, "rural": 350},
    },
    "Uttar Pradesh": {
        "Lucknow": {"urban": 4500, "semi-urban": 2200, "rural": 800},
        "Noida": {"urban": 8000, "semi-urban": 4000, "rural": 1500},
        "Ghaziabad": {"urban": 6000, "semi-urban": 3000, "rural": 1200},
        "Agra": {"urban": 3000, "semi-urban": 1500, "rural": 500},
        "Varanasi": {"urban": 3500, "semi-urban": 1800, "rural": 600},
        "Kanpur": {"urban": 3000, "semi-urban": 1500, "rural": 500},
        "Prayagraj": {"urban": 2800, "semi-urban": 1400, "rural": 500},
        "_default": {"urban": 2500, "semi-urban": 1200, "rural": 400},
    },
    "Madhya Pradesh": {
        "Bhopal": {"urban": 3500, "semi-urban": 1800, "rural": 600},
        "Indore": {"urban": 4000, "semi-urban": 2000, "rural": 700},
        "Gwalior": {"urban": 2500, "semi-urban": 1200, "rural": 400},
        "Jabalpur": {"urban": 2800, "semi-urban": 1400, "rural": 500},
        "_default": {"urban": 2000, "semi-urban": 900, "rural": 350},
    },
    "Punjab": {
        "Chandigarh": {"urban": 8000, "semi-urban": 4000, "rural": 1500},
        "Ludhiana": {"urban": 5000, "semi-urban": 2500, "rural": 1000},
        "Amritsar": {"urban": 4500, "semi-urban": 2200, "rural": 900},
        "Jalandhar": {"urban": 4000, "semi-urban": 2000, "rural": 800},
        "Patiala": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "_default": {"urban": 3000, "semi-urban": 1500, "rural": 600},
    },
    "Haryana": {
        "Gurugram": {"urban": 12000, "semi-urban": 6000, "rural": 2500},
        "Faridabad": {"urban": 7000, "semi-urban": 3500, "rural": 1400},
        "Panipat": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "Ambala": {"urban": 3000, "semi-urban": 1500, "rural": 600},
        "Hisar": {"urban": 2800, "semi-urban": 1400, "rural": 500},
        "_default": {"urban": 3000, "semi-urban": 1500, "rural": 600},
    },
    "West Bengal": {
        "Kolkata": {"urban": 8000, "semi-urban": 4000, "rural": 1500},
        "Howrah": {"urban": 5000, "semi-urban": 2500, "rural": 1000},
        "North 24 Parganas": {"urban": 4000, "semi-urban": 2000, "rural": 800},
        "South 24 Parganas": {"urban": 3000, "semi-urban": 1500, "rural": 600},
        "Darjeeling": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "_default": {"urban": 2500, "semi-urban": 1200, "rural": 450},
    },
    "Bihar": {
        "Patna": {"urban": 3500, "semi-urban": 1800, "rural": 600},
        "Gaya": {"urban": 2000, "semi-urban": 900, "rural": 350},
        "Muzaffarpur": {"urban": 2200, "semi-urban": 1000, "rural": 400},
        "_default": {"urban": 1800, "semi-urban": 800, "rural": 300},
    },
    "Odisha": {
        "Bhubaneswar": {"urban": 4000, "semi-urban": 2000, "rural": 700},
        "Cuttack": {"urban": 3000, "semi-urban": 1500, "rural": 600},
        "Puri": {"urban": 3500, "semi-urban": 1800, "rural": 700},
        "_default": {"urban": 2000, "semi-urban": 900, "rural": 350},
    },
    "Goa": {
        "North Goa": {"urban": 12000, "semi-urban": 6000, "rural": 3000},
        "South Goa": {"urban": 10000, "semi-urban": 5000, "rural": 2500},
        "_default": {"urban": 10000, "semi-urban": 5000, "rural": 2500},
    },
    "Delhi": {
        "New Delhi": {"urban": 20000, "semi-urban": 10000, "rural": 5000},
        "South Delhi": {"urban": 18000, "semi-urban": 9000, "rural": 4500},
        "Central Delhi": {"urban": 25000, "semi-urban": 12000, "rural": 6000},
        "_default": {"urban": 15000, "semi-urban": 8000, "rural": 4000},
    },
}

# Default for unknown states
DEFAULT_RATES = {"urban": 2000, "semi-urban": 1000, "rural": 400}

# Per sq.ft conversion (1 acre = 43,560 sq.ft)
SQFT_PER_ACRE = 43560


def lookup_guideline_rate(state: str, district: str, region_type: str) -> dict:
    """
    Look up the government guideline rate for a given location.
    Returns rate in ₹/sq.ft and ₹/acre.
    """
    state_data = GUIDELINE_RATES.get(state, {})

    # Try exact district match first
    district_rates = None
    for key in state_data:
        if key == "_default":
            continue
        if key.lower() in district.lower() or district.lower() in key.lower():
            district_rates = state_data[key]
            break

    # Fall back to state default, then global default
    if district_rates is None:
        district_rates = state_data.get("_default", DEFAULT_RATES)

    rtype = region_type if region_type in district_rates else "semi-urban"
    rate_per_sqft = district_rates.get(rtype, district_rates.get("semi-urban", 1000))

    rate_per_acre = rate_per_sqft * SQFT_PER_ACRE

    return {
        "guideline_rate_per_sqft": rate_per_sqft,
        "guideline_rate_per_acre": rate_per_acre,
        "source": f"Government Guideline / Circle Rate — {state}",
        "region_type_used": rtype,
        "note": "Based on approximate state government guidance values for registration purposes",
    }
