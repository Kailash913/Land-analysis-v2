// Frontend API client — calls the Python FastAPI backend.

const BACKEND_URL = `http://${window.location.hostname}:8000`;

// ---- Types matching the Python backend response ----

export interface EvaluationResult {
    coordinates: { lat: number; lng: number };
    location: {
        state: string;
        district: string;
        taluk: string;
        village: string;
        street: string;
        suburb: string;
        locality: string;
        region_type: string;
        display_name: string;
    };
    soil: {
        ph: number;
        organic_carbon: number;
        clay_pct: number;
        sand_pct: number;
        silt_pct: number;
        texture: string;
        soil_type: string;
    };
    climate: {
        elevation: number;
        current_temp: number;
        current_precipitation: number;
        avg_temperature: number;
        annual_rainfall: number;
        climate_zone: string;
    };
    infrastructure: {
        landmarks: { name: string; type: string; dist_km: number }[];
        nearest_road_km: number | null;
        nearest_market_km: number | null;
        nearest_settlement_km: number | null;
        infrastructure_score: number;
        total_amenities: number;
    };
    features: {
        soil_quality_index: number;
        climate_index: number;
        infrastructure_score: number;
        urban_index: number;
    };
    /* Circle Rate — Government data (AUTHORITATIVE) */
    real_data: {
        circle_rate: number | null;
        unit: string;
        guideline_rate_per_sqft: number;
        guideline_rate_per_acre: number;
        source: string;
        lookup_method: string;
        confidence_score: number;
        effective_date: string;
        property_type: string;
        matched: {
            district: string;
            taluk: string;
            village: string;
            street: string;
        };
        system_type: string;
        region_type_used: string;
        note: string;
    };
    /* ML Prediction — TNREGINET-trained LightGBM */
    ml_prediction: {
        predicted_rate_per_sqft: number;
        predicted_rate_per_acre: number;
        predicted_rate_lakhs: number;
        model: string;
        confidence: string;
        source: string;
        feature_weights: Record<string, number>;
        label: string;
        note: string;
    };
    /* LightGBM Circle Rate Prediction (learns govt valuation) */
    ml_circle_rate?: {
        predicted_circle_rate: number;
        unit: string;
        confidence: number;
        prediction_basis: string[];
        model_type: string;
        feature_importances: Record<string, number>;
        label: string;
        note: string;
    };
    /* Land Summary */
    land_summary?: {
        area_sqft: number;
        area_acres: number;
        land_type: string;
        land_type_confidence: number;
        circle_rate: number | null;
        total_valuation: number | null;
    };
    /* Urban Intelligence */
    urban_intelligence?: {
        nearby_facilities: Record<string, { name: string; distance_km: number }[]>;
        facility_counts: Record<string, number>;
        total_facilities: number;
        urban_suitability_index: number;
        accessibility_score: number;
        nearest_distances: Record<string, number | null>;
    };
    /* Agricultural Intelligence */
    agricultural_intelligence?: {
        soil_type: string;
        soil_ph: number;
        organic_carbon: number;
        texture: string;
        agriculture_suitability: number;
        water_availability: number;
        crop_recommendations: any;
        water_analysis: any;
        crop_rotation: any;
    };
    /* Investment Insight */
    investment_insight?: {
        development_potential: number;
        urbanization_index: number;
        zoning_risk: string;
        conflict_analysis: {
            conflict_level: string;
            urbanization_score: number;
            agriculture_viability: number;
            conversion_probability: number;
            warnings: string[];
            risk_factors: string[];
        };
        risk_analysis: any;
        land_use_comparison: any;
    };
    /* ML Features used */
    ml_features?: {
        administrative: Record<string, number>;
        zoning: Record<string, number>;
        infrastructure: Record<string, number>;
        urban_development: Record<string, number>;
        agricultural: Record<string, number>;
    };
    predictions: {
        land_use: {
            predicted_use: string;
            probabilities: Record<string, number>;
            model: string;
        };
        crop_recommendations: {
            top_crops: {
                crop: string;
                suitability_pct: number;
                season: string;
                water_need: string;
                reasons: string[];
            }[];
            total_suitable: number;
            model: string;
        };
        risk_analysis: {
            risk_level: string;
            risk_score: number;
            probabilities: Record<string, number>;
            risk_factors: string[];
            model: string;
        };
    };
    simulations: {
        land_use_comparison: {
            best_use: string;
            suitability: { use: string; score: number; percentage: number }[];
        };
        crop_rotation: {
            primary_crop: string;
            rotation_plan: { year: number; season: string; crop: string; benefit: string }[];
            rationale: string;
        };
        water_analysis: {
            water_analysis: {
                crop: string;
                water_need_mm: number;
                available_rainfall_mm: number;
                deficit_mm: number;
                irrigation_pct: number;
                status: string;
            }[];
            annual_rainfall_mm: number;
        };
    };
    evaluation_id: string | null;
}

/**
 * Evaluate a location using the full ML pipeline.
 */
export async function evaluateLand(lat: number, lng: number): Promise<EvaluationResult> {
    const res = await fetch(`${BACKEND_URL}/api/evaluate-land?lat=${lat}&lng=${lng}`);
    if (!res.ok) {
        throw new Error(`Backend API error: ${res.status}`);
    }
    return res.json();
}

/**
 * Fetch evaluation history from MongoDB.
 */
export async function fetchEvaluations(): Promise<any[]> {
    const res = await fetch(`${BACKEND_URL}/api/evaluations?limit=20`);
    if (!res.ok) return [];
    return res.json();
}

/**
 * Download PDF report for a given evaluation.
 */
export function getPdfUrl(evaluationId: string): string {
    return `${BACKEND_URL}/api/report/pdf/${evaluationId}`;
}

/**
 * Download CSV report for a given evaluation.
 */
export function getCsvUrl(evaluationId: string): string {
    return `${BACKEND_URL}/api/report/csv/${evaluationId}`;
}

// ---- Utility ----

export function formatIndianCurrency(value: number): string {
    if (value >= 10000000) {
        return `₹${(value / 10000000).toFixed(2)} Cr`;
    } else if (value >= 100000) {
        return `₹${(value / 100000).toFixed(2)} Lakhs`;
    }
    return `₹${value.toLocaleString("en-IN")}`;
}

export function formatPerSqft(value: number): string {
    return `₹${value.toLocaleString("en-IN")}/sq.ft`;
}
