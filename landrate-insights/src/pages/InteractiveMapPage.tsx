import { useState, useEffect, useRef } from "react";
import { Search, MapPin, Navigation, Loader2, Pentagon, Layers, ChevronDown, ChevronRight, Hospital, GraduationCap, ShoppingCart, TrainFront, Landmark, Bus, Fuel, Route } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { motion, AnimatePresence } from "framer-motion";
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMapEvents, useMap, FeatureGroup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import { useEvaluation } from "@/contexts/EvaluationContext";
import { formatPerSqft, formatIndianCurrency } from "@/services/api";
import { computePolygonArea, formatArea, type AreaResult } from "@/utils/AreaCalculator";

// Fix Leaflet default icon
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Tile layers
const TILE_LAYERS = {
  street: {
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    label: "Street",
  },
  satellite: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution: '&copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics',
    label: "Satellite",
  },
  terrain: {
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attribution: '&copy; OpenTopoMap',
    label: "Terrain",
  },
};

type MapStyle = keyof typeof TILE_LAYERS;
type DrawMode = "pin" | "polygon";

// -- Map event handlers --
function MapClickHandler({ onMapClick, drawMode }: {
  onMapClick: (lat: number, lng: number) => void;
  drawMode: DrawMode;
}) {
  useMapEvents({
    click(e) {
      if (drawMode === "pin") {
        onMapClick(e.latlng.lat, e.latlng.lng);
      }
    },
  });
  return null;
}

function MapFlyTo({ position }: { position: [number, number] }) {
  const map = useMap();
  useEffect(() => { map.flyTo(position, map.getZoom()); }, [position, map]);
  return null;
}

// -- Draw control component --
function DrawControl({ onPolygonCreated }: {
  onPolygonCreated: (coords: [number, number][]) => void;
}) {
  const map = useMap();
  const drawControlRef = useRef<any>(null);

  useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new (L.Control as any).Draw({
      position: 'topright',
      draw: {
        polygon: {
          allowIntersection: false,
          shapeOptions: {
            color: '#3b82f6',
            weight: 3,
            fillColor: '#3b82f680',
            fillOpacity: 0.3,
          },
          showArea: true,
        },
        rectangle: {
          shapeOptions: {
            color: '#3b82f6',
            weight: 3,
            fillColor: '#3b82f680',
            fillOpacity: 0.3,
          },
        },
        polyline: false,
        circle: false,
        circlemarker: false,
        marker: false,
      },
      edit: {
        featureGroup: drawnItems,
        edit: true,
        remove: true,
      },
    });

    map.addControl(drawControl);
    drawControlRef.current = drawControl;

    map.on((L as any).Draw.Event.CREATED, (e: any) => {
      drawnItems.clearLayers();
      drawnItems.addLayer(e.layer);
      const latlngs = e.layer.getLatLngs()[0];
      const coords: [number, number][] = latlngs.map((ll: any) =>
        [ll.lat, ll.lng] as [number, number]
      );
      onPolygonCreated(coords);
    });

    return () => {
      map.removeControl(drawControl);
      map.removeLayer(drawnItems);
    };
  }, [map, onPolygonCreated]);

  return null;
}

// ============================================================
// MAIN PAGE
// ============================================================
// Category icon map
const FACILITY_ICONS: Record<string, React.ReactNode> = {
  hospitals: <Hospital className="w-3.5 h-3.5 text-red-500" />,
  schools: <GraduationCap className="w-3.5 h-3.5 text-blue-500" />,
  markets: <ShoppingCart className="w-3.5 h-3.5 text-amber-500" />,
  highways: <Route className="w-3.5 h-3.5 text-gray-500" />,
  metro_rail: <TrainFront className="w-3.5 h-3.5 text-purple-500" />,
  banks: <Landmark className="w-3.5 h-3.5 text-emerald-500" />,
  bus: <Bus className="w-3.5 h-3.5 text-cyan-500" />,
  fuel: <Fuel className="w-3.5 h-3.5 text-orange-500" />,
};

const FACILITY_LABELS: Record<string, string> = {
  hospitals: "Hospitals",
  schools: "Schools & Colleges",
  markets: "Markets",
  highways: "Highways",
  metro_rail: "Metro / Rail",
  banks: "Banks",
  bus: "Bus Stations",
  fuel: "Fuel Stations",
};

export function InteractiveMapPage() {
  const [position, setPosition] = useState<[number, number]>([12.9716, 77.5946]);
  const { data, isLoading, error, evaluate } = useEvaluation();
  const [drawMode, setDrawMode] = useState<DrawMode>("pin");
  const [mapStyle, setMapStyle] = useState<MapStyle>("satellite");
  const [showLayerMenu, setShowLayerMenu] = useState(false);
  const [polygonCoords, setPolygonCoords] = useState<[number, number][] | null>(null);
  const [areaResult, setAreaResult] = useState<AreaResult | null>(null);
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);

  useEffect(() => {
    evaluate(position[0], position[1]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleMapClick = (lat: number, lng: number) => {
    setPosition([lat, lng]);
    setPolygonCoords(null);
    setAreaResult(null);
    evaluate(lat, lng);
  };

  const handlePolygonCreated = (coords: [number, number][]) => {
    const area = computePolygonArea(coords);
    setAreaResult(area);
    setPolygonCoords(coords);

    // Evaluate centroid
    const cLat = coords.reduce((s, c) => s + c[0], 0) / coords.length;
    const cLng = coords.reduce((s, c) => s + c[1], 0) / coords.length;
    setPosition([cLat, cLng]);
    evaluate(cLat, cLng);
  };

  const tile = TILE_LAYERS[mapStyle];
  const areaName = data?.location?.village || data?.location?.suburb || data?.location?.locality || data?.location?.district || '';

  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 h-[calc(100vh-8rem)]">
      {/* Map Panel — 60% */}
      <div className="lg:col-span-3 relative glass-card overflow-hidden flex items-center justify-center bg-card">

        {/* Search Bar */}
        <div className="absolute top-4 left-4 z-[400] flex items-center gap-2">
          <div className="flex items-center gap-2 bg-card/90 backdrop-blur-md rounded-xl px-4 py-2.5 shadow-md border border-border/50 max-w-sm">
            <Search className="w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search location..."
              className="bg-transparent text-sm outline-none w-full placeholder:text-muted-foreground/60"
            />
          </div>
        </div>

        {/* Mode Toggle: Pin ↔ Polygon */}
        <div className="absolute top-4 right-4 z-[400] flex flex-col gap-2">
          <div className="bg-card/90 backdrop-blur-md rounded-xl shadow-md border border-border/50 p-1 flex flex-col gap-1">
            <button
              onClick={() => setDrawMode("pin")}
              className={`p-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${drawMode === "pin"
                ? "bg-primary text-primary-foreground shadow"
                : "text-muted-foreground hover:bg-muted"
                }`}
              title="Pin Mode"
            >
              <MapPin className="w-4 h-4" />
              <span className="hidden sm:inline">Pin</span>
            </button>
            <button
              onClick={() => setDrawMode("polygon")}
              className={`p-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${drawMode === "polygon"
                ? "bg-primary text-primary-foreground shadow"
                : "text-muted-foreground hover:bg-muted"
                }`}
              title="Polygon Draw Mode"
            >
              <Pentagon className="w-4 h-4" />
              <span className="hidden sm:inline">Draw</span>
            </button>
          </div>

          {/* Map Style Toggle */}
          <div className="relative">
            <button
              onClick={() => setShowLayerMenu(!showLayerMenu)}
              className="bg-card/90 backdrop-blur-md rounded-xl shadow-md border border-border/50 p-2 flex items-center gap-1.5 text-xs font-semibold text-muted-foreground hover:bg-muted transition-all w-full"
            >
              <Layers className="w-4 h-4" />
              <span className="hidden sm:inline">{tile.label}</span>
              <ChevronDown className="w-3 h-3 ml-auto" />
            </button>
            {showLayerMenu && (
              <div className="absolute right-0 mt-1 bg-card/95 backdrop-blur-md rounded-xl shadow-lg border border-border/50 py-1 min-w-[120px]">
                {(Object.keys(TILE_LAYERS) as MapStyle[]).map((key) => (
                  <button
                    key={key}
                    onClick={() => { setMapStyle(key); setShowLayerMenu(false); }}
                    className={`block w-full text-left px-3 py-1.5 text-xs transition-all ${mapStyle === key
                      ? "bg-primary/10 text-primary font-semibold"
                      : "text-muted-foreground hover:bg-muted"
                      }`}
                  >
                    {TILE_LAYERS[key].label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Area name label overlay */}
        {areaName && (
          <div className="absolute bottom-16 left-1/2 -translate-x-1/2 z-[400] bg-card/90 backdrop-blur-md rounded-full px-4 py-1.5 shadow-lg border border-border/60 pointer-events-none">
            <p className="text-xs font-semibold text-foreground tracking-wide whitespace-nowrap">📍 {areaName}{data?.location?.district && areaName !== data.location.district ? `, ${data.location.district}` : ''}</p>
          </div>
        )}

        {/* Area info (polygon mode) */}
        {areaResult && (
          <div className="absolute bottom-4 left-4 z-[400] bg-card/95 backdrop-blur-md rounded-xl px-4 py-3 shadow-lg border border-primary/30">
            <p className="text-[10px] text-primary font-semibold uppercase tracking-wide">Polygon Area</p>
            <p className="text-lg font-bold text-foreground">{formatArea(areaResult)}</p>
            <p className="text-[10px] text-muted-foreground">
              {areaResult.area_sqmeters.toLocaleString("en-IN")} sq.m • {areaResult.perimeter_meters.toFixed(0)}m perimeter
            </p>
          </div>
        )}

        {/* Leaflet Map */}
        <div className="absolute inset-0 z-0">
          <MapContainer
            center={position}
            zoom={13}
            scrollWheelZoom={true}
            style={{ height: '100%', width: '100%' }}
            zoomControl={false}
          >
            <>
              <TileLayer
                key={mapStyle}
                attribution={tile.attribution}
                url={tile.url}
                maxZoom={19}
              />
              {drawMode === "pin" && (
                <Marker position={position}>
                  <Popup>
                    <div className="text-center min-w-[140px]">
                      {areaName && (
                        <p className="font-semibold text-sm text-foreground mb-1">📍 {areaName}</p>
                      )}
                      <p className="text-[11px] text-muted-foreground">
                        {position[0].toFixed(5)}, {position[1].toFixed(5)}
                      </p>
                    </div>
                  </Popup>
                </Marker>
              )}
              <MapClickHandler onMapClick={handleMapClick} drawMode={drawMode} />
              <MapFlyTo position={position} />
              {drawMode === "polygon" && (
                <DrawControl onPolygonCreated={handlePolygonCreated} />
              )}
            </>
          </MapContainer>
        </div>

        <div className="absolute bottom-4 right-4 z-[400] w-10 h-10 rounded-full bg-card/90 backdrop-blur border border-border/50 flex items-center justify-center shadow-sm">
          <Navigation className="w-4 h-4 text-primary" />
        </div>
      </div>

      {/* Insights Panel — 40% */}
      <div className="lg:col-span-2 space-y-4 relative overflow-y-auto">
        <AnimatePresence>
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 z-50 bg-background/50 backdrop-blur-sm flex items-center justify-center rounded-2xl"
            >
              <div className="text-center">
                <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto" />
                <p className="text-xs text-muted-foreground mt-2">Running analysis pipeline...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error Banner */}
        {error && !isLoading && (
          <div className="bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-red-700 dark:text-red-400">⚠️ Backend unavailable</p>
              <p className="text-[11px] text-red-600 dark:text-red-500 mt-0.5">{error}</p>
            </div>
            <button
              onClick={() => evaluate(position[0], position[1])}
              className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {/* 📍 Land Summary */}
        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-foreground">📍 Land Summary</h3>
            <span className="text-xs text-muted-foreground">{data?.location.display_name?.slice(0, 50)}</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-[10px] text-muted-foreground">District → Taluk</p>
              <p className="font-medium">{data?.location.district} → {data?.location.taluk || '—'}</p>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Village / Locality</p>
              <p className="font-medium">{data?.location.village || data?.location.suburb || '—'}</p>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Land Type</p>
              <span className="badge-emerald text-xs">{data?.predictions?.land_use?.predicted_use || 'Residential'}</span>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Region</p>
              <p className="font-medium capitalize">{data?.location.region_type || '—'}</p>
            </div>
          </div>
          {areaResult && (
            <div className="mt-3 pt-3 border-t border-border/50 grid grid-cols-3 gap-2 text-center">
              <div>
                <p className="text-[10px] text-muted-foreground">Area (sq.ft)</p>
                <p className="text-sm font-bold">{areaResult.area_sqft.toLocaleString("en-IN")}</p>
              </div>
              <div>
                <p className="text-[10px] text-muted-foreground">Area (acres)</p>
                <p className="text-sm font-bold">{areaResult.area_acres.toFixed(3)}</p>
              </div>
              <div>
                <p className="text-[10px] text-muted-foreground">Perimeter</p>
                <p className="text-sm font-bold">{areaResult.perimeter_meters.toFixed(0)}m</p>
              </div>
            </div>
          )}
        </div>

        {/* 💰 Circle Rate (SOURCE OF TRUTH) */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-3">💰 Land Rate (per sq.ft)</h3>
          <div className="grid grid-cols-2 gap-3">
            {/* Government Circle Rate */}
            <div className="rounded-xl border-2 border-blue-300 bg-blue-50/60 p-4 dark:bg-blue-950/30 dark:border-blue-800 relative">
              <span className="absolute -top-2 right-2 bg-blue-600 text-white text-[8px] px-1.5 py-0.5 rounded font-semibold">SOURCE OF TRUTH</span>
              <p className="text-[10px] text-blue-600 font-semibold uppercase tracking-wide mb-1">📋 Circle Rate</p>
              <p className="text-xl font-bold text-blue-700 dark:text-blue-300">
                {formatPerSqft(data?.real_data?.guideline_rate_per_sqft || 0)}
              </p>
              <p className="text-[10px] text-blue-700 font-medium mt-1">{data?.real_data?.source}</p>
              <p className="text-[10px] text-muted-foreground">{data?.real_data?.lookup_method}</p>
              {data?.real_data?.matched?.village && (
                <p className="text-[10px] text-muted-foreground">📍 {data.real_data.matched.village}{data.real_data.matched.street ? `, ${data.real_data.matched.street}` : ''}</p>
              )}
              <span className={`inline-block mt-1 px-1.5 py-0.5 rounded text-[9px] font-semibold ${(data?.real_data?.confidence_score || 0) >= 0.9 ? 'bg-green-100 text-green-700' :
                (data?.real_data?.confidence_score || 0) >= 0.7 ? 'bg-blue-100 text-blue-700' :
                  (data?.real_data?.confidence_score || 0) >= 0.5 ? 'bg-amber-100 text-amber-700' :
                    'bg-red-100 text-red-700'
                }`}>{Math.round((data?.real_data?.confidence_score || 0) * 100)}% confidence</span>
            </div>

            {/* ML Circle Rate Prediction */}
            <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 p-4 dark:bg-emerald-950/20 dark:border-emerald-900 relative">
              <span className="absolute -top-2 right-2 bg-emerald-600 text-white text-[8px] px-1.5 py-0.5 rounded font-semibold">ML PREDICTED</span>
              <p className="text-[10px] text-emerald-600 font-semibold uppercase tracking-wide mb-1">🤖 ML Circle Rate</p>
              <p className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
                {formatPerSqft((data as any)?.ml_circle_rate?.predicted_circle_rate || data?.ml_prediction?.predicted_rate_per_sqft || 0)}
              </p>
              <p className="text-[10px] text-muted-foreground mt-1">{(data as any)?.ml_circle_rate?.model_type || data?.ml_prediction?.model}</p>
              <p className="text-[10px] text-muted-foreground">{(data as any)?.ml_circle_rate?.prediction_basis?.[0] || ''}</p>
              <span className={`inline-block mt-1 px-1.5 py-0.5 rounded text-[9px] font-semibold ${((data as any)?.ml_circle_rate?.confidence || 0) >= 0.8 ? 'bg-green-100 text-green-700' :
                ((data as any)?.ml_circle_rate?.confidence || 0) >= 0.5 ? 'bg-amber-100 text-amber-700' :
                  'bg-red-100 text-red-700'
                }`}>{Math.round(((data as any)?.ml_circle_rate?.confidence || 0) * 100)}% confidence</span>
            </div>
          </div>

          {/* Total valuation for polygon */}
          {areaResult && data?.real_data?.circle_rate && (
            <div className="mt-3 pt-3 border-t border-border/50 text-center">
              <p className="text-[10px] text-muted-foreground">Total Valuation (Area × Circle Rate)</p>
              <p className="text-2xl font-bold text-primary">
                {formatIndianCurrency(data.real_data.circle_rate * areaResult.area_sqft)}
              </p>
            </div>
          )}
        </div>

        {/* 🏙️ Urban Intelligence */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-3">🏙️ Urban Intelligence</h3>
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <p className="text-[10px] text-muted-foreground">Urban Suitability</p>
              <div className="flex items-center gap-2">
                <Progress value={(data as any)?.urban_intelligence?.urban_suitability_index || data?.features?.urban_index || 50} className="flex-1 h-2" />
                <span className="text-xs font-semibold">{(data as any)?.urban_intelligence?.urban_suitability_index || data?.features?.urban_index || 50}%</span>
              </div>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Accessibility</p>
              <div className="flex items-center gap-2">
                <Progress value={(data as any)?.urban_intelligence?.accessibility_score || 50} className="flex-1 h-2" />
                <span className="text-xs font-semibold">{(data as any)?.urban_intelligence?.accessibility_score || 50}%</span>
              </div>
            </div>
          </div>

          {/* Facility summary counts */}
          <div className="grid grid-cols-4 gap-2 text-center mb-3">
            {["hospitals", "schools", "markets", "metro_rail"].map((cat) => (
              <div key={cat} className="rounded-lg bg-muted/50 p-2">
                <p className="text-lg font-bold">{(data as any)?.urban_intelligence?.facility_counts?.[cat] || 0}</p>
                <p className="text-[9px] text-muted-foreground capitalize">{cat.replace("_", "/")}</p>
              </div>
            ))}
          </div>

          {/* Detailed nearby facilities with names + distances */}
          <div className="space-y-1">
            <p className="text-[10px] text-muted-foreground font-semibold uppercase tracking-wide mb-1">Nearby Facilities</p>
            {Object.entries((data as any)?.urban_intelligence?.nearby_facilities || {}).map(([cat, items]: [string, any]) => {
              const facilityList = items as { name: string; distance_km: number }[];
              if (!facilityList || facilityList.length === 0) return null;
              const isExpanded = expandedCategory === cat;
              return (
                <div key={cat} className="rounded-lg border border-border/40 overflow-hidden">
                  <button
                    onClick={() => setExpandedCategory(isExpanded ? null : cat)}
                    className="w-full flex items-center gap-2 px-3 py-2 hover:bg-muted/50 transition-colors text-left"
                  >
                    {FACILITY_ICONS[cat] || <MapPin className="w-3.5 h-3.5 text-muted-foreground" />}
                    <span className="text-xs font-medium flex-1">{FACILITY_LABELS[cat] || cat}</span>
                    <span className="text-[10px] text-muted-foreground mr-1">{facilityList.length}</span>
                    <ChevronRight className={`w-3 h-3 text-muted-foreground transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                  </button>
                  {isExpanded && (
                    <div className="border-t border-border/30 max-h-32 overflow-y-auto">
                      {facilityList.map((f, i) => (
                        <div
                          key={i}
                          className="flex items-center justify-between px-3 py-1.5 text-[11px] border-b border-border/20 last:border-0 hover:bg-muted/30"
                        >
                          <span className="font-medium text-foreground truncate mr-2">{f.name}</span>
                          <span className="text-muted-foreground whitespace-nowrap font-mono">{f.distance_km} km</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* 🌾 Agricultural Intelligence */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-3">🌾 Agricultural Intelligence</h3>
          <div className="grid grid-cols-3 gap-3 text-center mb-3">
            <div>
              <p className="text-[10px] text-muted-foreground">Soil</p>
              <p className="text-xs font-semibold">{data?.soil?.texture || '—'}</p>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Rainfall</p>
              <p className="text-xs font-semibold">{data?.climate?.annual_rainfall || 0}mm</p>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Agri Score</p>
              <p className="text-xs font-semibold">{(data as any)?.agricultural_intelligence?.agriculture_suitability || (data as any)?.ml_features?.agricultural?.agriculture_suitability_score || '—'}%</p>
            </div>
          </div>
          {data?.predictions?.crop_recommendations?.top_crops?.slice(0, 3).map((crop, i) => (
            <div key={i} className="flex items-center justify-between py-1 border-b border-border/30 last:border-0">
              <span className="text-xs font-medium">🌱 {crop.crop}</span>
              <span className="text-[10px] text-muted-foreground">{crop.suitability_pct}% suitable</span>
            </div>
          ))}
        </div>

        {/* 📊 Investment Insight */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-3">📊 Investment Insight</h3>
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <p className="text-[10px] text-muted-foreground">Best Use</p>
              <span className="badge-emerald text-xs">{data?.predictions?.land_use?.predicted_use}</span>
            </div>
            <div>
              <p className="text-[10px] text-muted-foreground">Risk</p>
              <p className={`text-sm font-bold ${data?.predictions?.risk_analysis?.risk_level === 'High' ? 'text-destructive' :
                data?.predictions?.risk_analysis?.risk_level === 'Medium' ? 'text-amber-500' : 'text-primary'
                }`}>
                {data?.predictions?.risk_analysis?.risk_level || "N/A"}
              </p>
            </div>
          </div>
          {/* Conflict warnings */}
          {(data as any)?.investment_insight?.conflict_analysis?.warnings?.length > 0 && (
            <div className="mt-2 space-y-1">
              {(data as any).investment_insight.conflict_analysis.warnings.map((w: string, i: number) => (
                <p key={i} className="text-[10px] text-amber-600 bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded">⚠️ {w}</p>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
