"""
Real Estate Market Data Preprocessor.

Loads the 99acres dataset, extracts price/sq.ft by city + neighborhood,
and provides training data for the ML model.
"""
import json
import re
import os
from typing import Optional

DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "datasetml.json")


def _parse_sqft(size_str: str) -> Optional[float]:
    """Extract a numeric sqft value from size strings like '1085 sqft', '799-1258 sqft'."""
    if not size_str or size_str in ("N/A", "Varies", "various", "", "sq.ft", "0 sqft"):
        return None
    # Match patterns like "1085 sqft", "799-1258 sqft", "1085 sq ft", "1085 sq.ft."
    nums = re.findall(r"[\d,]+\.?\d*", size_str.replace(",", ""))
    if not nums:
        return None
    vals = [float(n) for n in nums if float(n) > 10]
    if not vals:
        return None
    # For ranges, use the midpoint
    if len(vals) >= 2:
        return (vals[0] + vals[-1]) / 2
    return vals[0]


def load_and_preprocess() -> list[dict]:
    """
    Load the JSON dataset and compute price_per_sqft for each valid listing.
    Returns a list of dicts with: city, neighborhood, type, price, sqft, price_per_sqft, beds, baths
    """
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Dataset not found or invalid at {DATASET_PATH}, using embedded data")
        return _get_embedded_data()

    listings = raw[0].get("real_estate_listings", []) if raw else []
    return _process_listings(listings)


def _process_listings(listings: list) -> list[dict]:
    """Process raw listings into clean training records."""
    records = []
    for item in listings:
        price = item.get("price", 0)
        if not price or price < 1000:
            continue  # skip entries with no or tiny price

        size_str = str(item.get("size", ""))
        sqft = _parse_sqft(size_str)
        if not sqft or sqft < 50:
            continue  # skip entries with no valid size

        price_per_sqft = price / sqft

        # Filter out unreasonable values
        if price_per_sqft < 200 or price_per_sqft > 200000:
            continue

        records.append({
            "city": item.get("city", "Unknown"),
            "neighborhood": item.get("neighborhood", "Unknown"),
            "type": item.get("type", "Unknown"),
            "beds": item.get("beds", 0),
            "baths": item.get("baths", 0),
            "price": price,
            "sqft": sqft,
            "price_per_sqft": round(price_per_sqft, 2),
        })
    return records


def get_city_rates() -> dict[str, dict]:
    """
    Aggregate by city: compute avg, min, max price_per_sqft.
    Returns { city: { avg_per_sqft, min_per_sqft, max_per_sqft, samples } }
    """
    records = load_and_preprocess()
    from collections import defaultdict
    city_data = defaultdict(list)
    for r in records:
        city_data[r["city"]].append(r["price_per_sqft"])

    result = {}
    for city, prices in city_data.items():
        result[city] = {
            "avg_per_sqft": round(sum(prices) / len(prices)),
            "min_per_sqft": round(min(prices)),
            "max_per_sqft": round(max(prices)),
            "samples": len(prices),
        }
    return result


def get_neighborhood_rates() -> dict[str, dict[str, dict]]:
    """
    Aggregate by city → neighborhood: compute avg price_per_sqft.
    Returns { city: { neighborhood: { avg_per_sqft, samples, listings } } }
    """
    records = load_and_preprocess()
    from collections import defaultdict
    nested = defaultdict(lambda: defaultdict(list))
    for r in records:
        nested[r["city"]][r["neighborhood"]].append(r["price_per_sqft"])

    result = {}
    for city, neighborhoods in nested.items():
        result[city] = {}
        for hood, prices in neighborhoods.items():
            result[city][hood] = {
                "avg_per_sqft": round(sum(prices) / len(prices)),
                "samples": len(prices),
            }
    return result


def _get_embedded_data() -> list[dict]:
    """
    Fallback embedded data when the JSON file is not available.
    Derived from the 99acres dataset provided by the user.
    """
    # Key city-level averages from the dataset
    embedded = [
        # Bangalore
        {"city": "Bangalore", "neighborhood": "Jigani", "type": "Land", "beds": 0, "baths": 0, "price": 2317000, "sqft": 1028, "price_per_sqft": 2253},
        {"city": "Bangalore", "neighborhood": "Tumkur Road", "type": "Flat", "beds": 2, "baths": 2, "price": 12500000, "sqft": 1085, "price_per_sqft": 11521},
        {"city": "Bangalore", "neighborhood": "Whitefield", "type": "Apartment", "beds": 3, "baths": 2, "price": 23200000, "sqft": 1837, "price_per_sqft": 12629},
        {"city": "Bangalore", "neighborhood": "Kalkere", "type": "Apartment", "beds": 2, "baths": 2, "price": 6483000, "sqft": 1314, "price_per_sqft": 4934},
        {"city": "Bangalore", "neighborhood": "Sarjapur Road", "type": "Apartment", "beds": 2, "baths": 2, "price": 15000000, "sqft": 1841, "price_per_sqft": 8148},
        {"city": "Bangalore", "neighborhood": "Yelahanka", "type": "Apartment", "beds": 2, "baths": 2, "price": 7518000, "sqft": 1358, "price_per_sqft": 5536},
        {"city": "Bangalore", "neighborhood": "Bannerghatta Road", "type": "Apartment", "beds": 2, "baths": 2, "price": 15700000, "sqft": 2017, "price_per_sqft": 7784},
        # Gurgaon
        {"city": "Gurgaon", "neighborhood": "Sector 65", "type": "Flat", "beds": 4, "baths": 4, "price": 200000000, "sqft": 6050, "price_per_sqft": 33058},
        {"city": "Gurgaon", "neighborhood": "Sector 103", "type": "Flat", "beds": 4, "baths": 4, "price": 40100000, "sqft": 4200, "price_per_sqft": 9548},
        {"city": "Gurgaon", "neighborhood": "Sector 49", "type": "Apartment", "beds": 3, "baths": 3, "price": 52800000, "sqft": 1359, "price_per_sqft": 38853},
        {"city": "Gurgaon", "neighborhood": "South City 2", "type": "Floor", "beds": 4, "baths": 5, "price": 45000000, "sqft": 4500, "price_per_sqft": 10000},
        {"city": "Gurgaon", "neighborhood": "Rosewood City", "type": "Land", "beds": 0, "baths": 0, "price": 249500000, "sqft": 9000, "price_per_sqft": 27722},
        # Hyderabad
        {"city": "Hyderabad", "neighborhood": "Mokila", "type": "Flat", "beds": 3, "baths": 4, "price": 13600000, "sqft": 2713, "price_per_sqft": 5013},
        {"city": "Hyderabad", "neighborhood": "Tellapur", "type": "Apartment", "beds": 2, "baths": 2, "price": 10000000, "sqft": 1200, "price_per_sqft": 8333},
        {"city": "Hyderabad", "neighborhood": "Kondapur", "type": "Flat", "beds": 3, "baths": 4, "price": 25300000, "sqft": 1965, "price_per_sqft": 12875},
        {"city": "Hyderabad", "neighborhood": "KPHB", "type": "Apartment", "beds": 3, "baths": 3, "price": 19200000, "sqft": 1600, "price_per_sqft": 12000},
        {"city": "Hyderabad", "neighborhood": "Kokapet", "type": "Apartment", "beds": 3, "baths": 3, "price": 12600000, "sqft": 1500, "price_per_sqft": 8400},
        # Chennai
        {"city": "Chennai", "neighborhood": "Maduravoyal", "type": "Flat", "beds": 2, "baths": 2, "price": 8445000, "sqft": 959, "price_per_sqft": 8806},
        {"city": "Chennai", "neighborhood": "T Nagar", "type": "Apartment", "beds": 3, "baths": 3, "price": 34000000, "sqft": 2372, "price_per_sqft": 14334},
        {"city": "Chennai", "neighborhood": "Sholinganallur", "type": "Apartment", "beds": 3, "baths": 3, "price": 19200000, "sqft": 2183, "price_per_sqft": 8797},
        {"city": "Chennai", "neighborhood": "ECR", "type": "Apartment", "beds": 1, "baths": 1, "price": 8460000, "sqft": 1187, "price_per_sqft": 7128},
        {"city": "Chennai", "neighborhood": "Perungudi", "type": "Flat", "beds": 3, "baths": 3, "price": 20700000, "sqft": 1723, "price_per_sqft": 12014},
        # Mumbai
        {"city": "Mumbai", "neighborhood": "Santacruz West", "type": "Flat", "beds": 3, "baths": 4, "price": 73000000, "sqft": 1459, "price_per_sqft": 50034},
        {"city": "Mumbai", "neighborhood": "Wadala", "type": "Apartment", "beds": 2, "baths": 2, "price": 29900000, "sqft": 1052, "price_per_sqft": 28422},
        {"city": "Mumbai", "neighborhood": "Worli", "type": "Apartment", "beds": 2, "baths": 2, "price": 48000000, "sqft": 1546, "price_per_sqft": 31047},
        {"city": "Mumbai", "neighborhood": "Prabhadevi", "type": "Apartment", "beds": 3, "baths": 2, "price": 95400000, "sqft": 2211, "price_per_sqft": 43145},
        {"city": "Mumbai", "neighborhood": "Mahalaxmi", "type": "Apartment", "beds": 2, "baths": 2, "price": 45700000, "sqft": 1281, "price_per_sqft": 35675},
        # Delhi
        {"city": "Delhi", "neighborhood": "Paschim Vihar", "type": "Floor", "beds": 3, "baths": 3, "price": 25500000, "sqft": 1350, "price_per_sqft": 18889},
        {"city": "Delhi", "neighborhood": "Karol Bagh", "type": "Apartment", "beds": 2, "baths": 2, "price": 22500000, "sqft": 1200, "price_per_sqft": 18750},
        {"city": "Delhi", "neighborhood": "Greater Kailash 2", "type": "Floor", "beds": 3, "baths": 3, "price": 50000000, "sqft": 2000, "price_per_sqft": 25000},
        {"city": "Delhi", "neighborhood": "Moti Nagar", "type": "Apartment", "beds": 2, "baths": 2, "price": 21000000, "sqft": 1300, "price_per_sqft": 16154},
        # Noida
        {"city": "Noida", "neighborhood": "Sector 146", "type": "Flat", "beds": 3, "baths": 3, "price": 29800000, "sqft": 1925, "price_per_sqft": 15481},
        {"city": "Noida", "neighborhood": "Sector 75", "type": "Apartment", "beds": 3, "baths": 2, "price": 26500000, "sqft": 2083, "price_per_sqft": 12723},
        {"city": "Noida", "neighborhood": "Sector 44", "type": "Apartment", "beds": 3, "baths": 3, "price": 73000000, "sqft": 3000, "price_per_sqft": 24333},
        {"city": "Noida", "neighborhood": "Sector 94", "type": "Apartment", "beds": 3, "baths": 3, "price": 81700000, "sqft": 3500, "price_per_sqft": 23343},
        # Pune
        {"city": "Pune", "neighborhood": "Ghorpadi", "type": "Apartment", "beds": 3, "baths": 3, "price": 16000000, "sqft": 1510, "price_per_sqft": 10596},
        {"city": "Pune", "neighborhood": "Hinjewadi", "type": "Apartment", "beds": 2, "baths": 2, "price": 8700000, "sqft": 710, "price_per_sqft": 12254},
        {"city": "Pune", "neighborhood": "Undri", "type": "Apartment", "beds": 3, "baths": 2, "price": 9500000, "sqft": 1150, "price_per_sqft": 8261},
        {"city": "Pune", "neighborhood": "Sinhgad Road", "type": "Apartment", "beds": 2, "baths": 2, "price": 13000000, "sqft": 1075, "price_per_sqft": 12093},
        {"city": "Pune", "neighborhood": "Mahalunge", "type": "Apartment", "beds": 3, "baths": 3, "price": 12000000, "sqft": 878, "price_per_sqft": 13667},
        # Jaipur
        {"city": "Jaipur", "neighborhood": "Tonk Road", "type": "Flat", "beds": 3, "baths": 2, "price": 9378000, "sqft": 1916, "price_per_sqft": 4894},
        {"city": "Jaipur", "neighborhood": "Mansarovar", "type": "Apartment", "beds": 3, "baths": 2, "price": 12200000, "sqft": 1967, "price_per_sqft": 6203},
        {"city": "Jaipur", "neighborhood": "Vaishali Nagar", "type": "Apartment", "beds": 2, "baths": 2, "price": 4200000, "sqft": 1208, "price_per_sqft": 3477},
        {"city": "Jaipur", "neighborhood": "C Scheme", "type": "Apartment", "beds": 3, "baths": 2, "price": 28900000, "sqft": 2332, "price_per_sqft": 12393},
        # Kakinada
        {"city": "Kakinada", "neighborhood": "Atchampeta", "type": "Villa", "beds": 3, "baths": 5, "price": 16500000, "sqft": 2600, "price_per_sqft": 6346},
        {"city": "Kakinada", "neighborhood": "Gandhi Nagar", "type": "Flat", "beds": 2, "baths": 2, "price": 7800000, "sqft": 1450, "price_per_sqft": 5379},
        {"city": "Kakinada", "neighborhood": "Vidyut Nagar", "type": "Flat", "beds": 3, "baths": 2, "price": 7000000, "sqft": 1472, "price_per_sqft": 4756},
        {"city": "Kakinada", "neighborhood": "Ramanayapeta", "type": "Villa", "beds": 5, "baths": 5, "price": 25000000, "sqft": 3150, "price_per_sqft": 7937},
        {"city": "Kakinada", "neighborhood": "Sarpavaram", "type": "House", "beds": 5, "baths": 4, "price": 33000000, "sqft": 2430, "price_per_sqft": 13580},
        # Visakhapatnam
        {"city": "Visakhapatnam", "neighborhood": "Madhurawada", "type": "Apartment", "beds": 2, "baths": 2, "price": 4940000, "sqft": 1117, "price_per_sqft": 4423},
        {"city": "Visakhapatnam", "neighborhood": "Gajuwaka", "type": "Apartment", "beds": 2, "baths": 2, "price": 3133000, "sqft": 972, "price_per_sqft": 3224},
        {"city": "Visakhapatnam", "neighborhood": "Yendada", "type": "Apartment", "beds": 2, "baths": 2, "price": 6947000, "sqft": 1316, "price_per_sqft": 5278},
        {"city": "Visakhapatnam", "neighborhood": "Kommadi", "type": "House", "beds": 4, "baths": 4, "price": 19500000, "sqft": 2403, "price_per_sqft": 8115},
        # Kochi
        {"city": "Kochi", "neighborhood": "Vennala", "type": "Land", "beds": 0, "baths": 0, "price": 12000000, "sqft": 3049, "price_per_sqft": 3935},
        {"city": "Kochi", "neighborhood": "Chalikavattom", "type": "House", "beds": 3, "baths": 3, "price": 7000000, "sqft": 1375, "price_per_sqft": 5091},
        {"city": "Kochi", "neighborhood": "Chakkaraparambu", "type": "House", "beds": 3, "baths": 3, "price": 7500000, "sqft": 1000, "price_per_sqft": 7500},
        # Lucknow
        {"city": "Lucknow", "neighborhood": "Sultanpur Road", "type": "Flat", "beds": 3, "baths": 3, "price": 6105000, "sqft": 1489, "price_per_sqft": 4100},
        {"city": "Lucknow", "neighborhood": "Gomti Nagar Extension", "type": "Apartment", "beds": 2, "baths": 2, "price": 20300000, "sqft": 1800, "price_per_sqft": 11278},
        {"city": "Lucknow", "neighborhood": "Sushant Golf City", "type": "Apartment", "beds": 2, "baths": 2, "price": 9059000, "sqft": 1350, "price_per_sqft": 6710},
        # Bhubaneswar
        {"city": "Bhubaneswar", "neighborhood": "Patia", "type": "Flat", "beds": 3, "baths": 3, "price": 18000000, "sqft": 2179, "price_per_sqft": 8262},
        {"city": "Bhubaneswar", "neighborhood": "Khandagiri", "type": "Apartment", "beds": 3, "baths": 3, "price": 20600000, "sqft": 1802, "price_per_sqft": 11432},
        {"city": "Bhubaneswar", "neighborhood": "Gothapatna", "type": "Apartment", "beds": 2, "baths": 2, "price": 8286000, "sqft": 2117, "price_per_sqft": 3914},
        # Gandhinagar
        {"city": "Gandhinagar", "neighborhood": "Sargasan", "type": "Flat", "beds": 2, "baths": 2, "price": 6500000, "sqft": 1530, "price_per_sqft": 4248},
        {"city": "Gandhinagar", "neighborhood": "Gift City", "type": "Apartment", "beds": 3, "baths": 3, "price": 25400000, "sqft": 1918, "price_per_sqft": 13242},
        # Coimbatore
        {"city": "Coimbatore", "neighborhood": "Ganapathy", "type": "Villa", "beds": 4, "baths": 4, "price": 25100000, "sqft": 3000, "price_per_sqft": 8367},
        {"city": "Coimbatore", "neighborhood": "Sulur", "type": "Land", "beds": 0, "baths": 0, "price": 1998000, "sqft": 2874, "price_per_sqft": 695},
        # Patna
        {"city": "Patna", "neighborhood": "Bihta", "type": "Land", "beds": 0, "baths": 0, "price": 1558000, "sqft": 1200, "price_per_sqft": 1298},
        {"city": "Patna", "neighborhood": "Sonepur", "type": "Land", "beds": 0, "baths": 0, "price": 5520000, "sqft": 2400, "price_per_sqft": 2300},
        {"city": "Patna", "neighborhood": "Danapur", "type": "Apartment", "beds": 2, "baths": 2, "price": 6294000, "sqft": 1200, "price_per_sqft": 5245},
        # Agra
        {"city": "Agra", "neighborhood": "Taj Nagari", "type": "Flat", "beds": 3, "baths": 3, "price": 11000000, "sqft": 1883, "price_per_sqft": 5842},
        {"city": "Agra", "neighborhood": "Shastripuram", "type": "Flat", "beds": 2, "baths": 2, "price": 5200000, "sqft": 968, "price_per_sqft": 5372},
        {"city": "Agra", "neighborhood": "Dayal Bagh", "type": "Flat", "beds": 3, "baths": 3, "price": 8200000, "sqft": 1705, "price_per_sqft": 4810},
        # Vijayawada
        {"city": "Vijayawada", "neighborhood": "Penamaluru", "type": "Land", "beds": 0, "baths": 0, "price": 2004000, "sqft": 1503, "price_per_sqft": 1333},
        {"city": "Vijayawada", "neighborhood": "Sri Ramachandra Nagar", "type": "Apartment", "beds": 4, "baths": 4, "price": 26700000, "sqft": 3690, "price_per_sqft": 7236},
        {"city": "Vijayawada", "neighborhood": "Gannavaram", "type": "Apartment", "beds": 2, "baths": 2, "price": 5065000, "sqft": 954, "price_per_sqft": 5309},
    ]
    return embedded
