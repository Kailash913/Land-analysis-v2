/**
 * Geodesic Area Calculator — Client-side polygon area computation.
 *
 * Uses the Shoelace formula on WGS84 to compute:
 *   area_sqft, area_acres, area_sqmeters, area_hectares
 *   perimeter_meters
 *
 * From user-drawn Leaflet polygon coordinates.
 */

const EARTH_RADIUS = 6371000; // meters

/** Convert degrees to radians */
function toRad(deg: number): number {
    return (deg * Math.PI) / 180;
}

/**
 * Haversine distance between two points in meters.
 */
export function haversineDistance(
    lat1: number, lng1: number,
    lat2: number, lng2: number
): number {
    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);
    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
    return EARTH_RADIUS * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/**
 * Compute the geodesic area of a polygon on Earth's surface.
 * Uses the spherical excess formula.
 *
 * @param coords Array of [lat, lng] pairs (closed or open polygon)
 * @returns area in square meters
 */
export function computeGeodesicArea(coords: [number, number][]): number {
    if (coords.length < 3) return 0;

    // Ensure polygon is closed
    const closed = [...coords];
    if (
        closed[0][0] !== closed[closed.length - 1][0] ||
        closed[0][1] !== closed[closed.length - 1][1]
    ) {
        closed.push(closed[0]);
    }

    // Shoelace on projected coordinates (equirectangular approximation)
    const avgLat = coords.reduce((sum, c) => sum + c[0], 0) / coords.length;
    const cosAvg = Math.cos(toRad(avgLat));

    let area = 0;
    for (let i = 0; i < closed.length - 1; i++) {
        const x1 = toRad(closed[i][1]) * cosAvg * EARTH_RADIUS;
        const y1 = toRad(closed[i][0]) * EARTH_RADIUS;
        const x2 = toRad(closed[i + 1][1]) * cosAvg * EARTH_RADIUS;
        const y2 = toRad(closed[i + 1][0]) * EARTH_RADIUS;
        area += x1 * y2 - x2 * y1;
    }

    return Math.abs(area / 2);
}

/**
 * Compute the perimeter of a polygon in meters.
 */
export function computePerimeter(coords: [number, number][]): number {
    if (coords.length < 2) return 0;

    let perimeter = 0;
    for (let i = 0; i < coords.length; i++) {
        const next = (i + 1) % coords.length;
        perimeter += haversineDistance(
            coords[i][0], coords[i][1],
            coords[next][0], coords[next][1]
        );
    }
    return perimeter;
}

/**
 * Full area computation result.
 */
export interface AreaResult {
    area_sqmeters: number;
    area_sqft: number;
    area_acres: number;
    area_hectares: number;
    perimeter_meters: number;
}

/**
 * Compute all area metrics for a polygon.
 */
export function computePolygonArea(coords: [number, number][]): AreaResult {
    const areaSqM = computeGeodesicArea(coords);
    const perimeterM = computePerimeter(coords);

    return {
        area_sqmeters: Math.round(areaSqM * 100) / 100,
        area_sqft: Math.round(areaSqM * 10.7639 * 100) / 100,
        area_acres: Math.round((areaSqM / 4046.86) * 10000) / 10000,
        area_hectares: Math.round((areaSqM / 10000) * 10000) / 10000,
        perimeter_meters: Math.round(perimeterM * 100) / 100,
    };
}

/**
 * Compute centroid of a polygon.
 */
export function computeCentroid(coords: [number, number][]): [number, number] {
    const lat = coords.reduce((s, c) => s + c[0], 0) / coords.length;
    const lng = coords.reduce((s, c) => s + c[1], 0) / coords.length;
    return [lat, lng];
}

/**
 * Format area for display.
 */
export function formatArea(area: AreaResult): string {
    if (area.area_acres >= 1) {
        return `${area.area_acres.toFixed(2)} acres`;
    } else if (area.area_sqft >= 100) {
        return `${area.area_sqft.toLocaleString("en-IN")} sq.ft`;
    }
    return `${area.area_sqmeters.toFixed(1)} sq.m`;
}
