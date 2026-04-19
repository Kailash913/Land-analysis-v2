import httpx, json

print("=== TESTING FULL GIS PLATFORM PIPELINE ===")
print()

# Test with Chennai T.Nagar
print("--- Test: Chennai T.Nagar ---")
r = httpx.get('http://localhost:3001/api/evaluate-land?lat=13.0418&lng=80.2341', timeout=60)
d = r.json()

# Check all new sections exist
sections = ['real_data', 'ml_circle_rate', 'ml_features', 'urban_intelligence',
            'agricultural_intelligence', 'investment_insight', 'land_summary']
for s in sections:
    print(f"  {s}: {'YES' if s in d else 'MISSING'}")

print()

# Circle rate
rd = d.get('real_data', {})
print(f"  Circle Rate: Rs.{rd.get('circle_rate', 0)}/sq.ft")
print(f"  Source: {rd.get('source', '')}")
print(f"  Lookup: {rd.get('lookup_method', '')}")

# ML Circle Rate
mc = d.get('ml_circle_rate', {})
print(f"  ML Circle Rate: Rs.{mc.get('predicted_circle_rate', 0)}/sq.ft")
print(f"  ML Confidence: {mc.get('confidence', 0)}")
print(f"  ML Model: {mc.get('model_type', '')}")
print(f"  ML Basis: {mc.get('prediction_basis', [])}")

# Urban Intelligence
ui = d.get('urban_intelligence', {})
print(f"  Urban Suitability: {ui.get('urban_suitability_index', 0)}")
print(f"  Accessibility: {ui.get('accessibility_score', 0)}")
print(f"  Total Facilities: {ui.get('total_facilities', 0)}")
print(f"  Facility Counts: {ui.get('facility_counts', {})}")

# Investment Insight
ii = d.get('investment_insight', {})
ca = ii.get('conflict_analysis', {})
print(f"  Conflict: {ca.get('conflict_level', '')}")
print(f"  Urbanization: {ca.get('urbanization_score', 0)}")
print(f"  Conversion Prob: {ca.get('conversion_probability', 0)}")

# ML Features
mf = d.get('ml_features', {})
print(f"  ML Feature Families: {list(mf.keys())}")

print()
print("=== PIPELINE TEST COMPLETE ===")
