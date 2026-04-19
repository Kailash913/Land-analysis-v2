import { Brain, BarChart3, Droplets, Mountain, Building2, Route, Leaf, Zap } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";
import { useEvaluation } from "@/contexts/EvaluationContext";
import { formatPerSqft, formatIndianCurrency } from "@/services/api";

export function ValuationEnginePage() {
  const { data } = useEvaluation();

  if (!data) {
    return (
      <div className="glass-card p-8 text-center max-w-6xl">
        <p className="text-muted-foreground">Click a location on the <b>Interactive Map</b> first to generate a valuation.</p>
      </div>
    );
  }

  const guidelineRate = data.real_data.guideline_rate_per_sqft;
  const mlRate = data.ml_prediction.predicted_rate_per_sqft;
  const confidence = Math.min(95, Math.round(50 + (data.features.soil_quality_index) * 0.2 + (data.features.climate_index) * 0.15 + (data.features.infrastructure_score) * 0.1));
  const weights = data.ml_prediction.feature_weights || {};

  const confidenceData = [
    { name: "Confidence", value: confidence },
    { name: "Remaining", value: 100 - confidence },
  ];

  const factors = [
    { label: "Soil Quality", value: Math.round(data.features.soil_quality_index), icon: Mountain },
    { label: "Climate Index", value: Math.round(data.features.climate_index), icon: Droplets },
    { label: "Infrastructure", value: Math.round(data.features.infrastructure_score), icon: Route },
    { label: "Urban Index", value: Math.round(data.features.urban_index), icon: Building2 },
    { label: "Rainfall (mm)", value: Math.min(100, Math.round(data.climate.annual_rainfall / 25)), icon: Leaf },
    { label: "Elevation Score", value: Math.min(100, Math.round(data.climate.elevation / 20)), icon: Zap },
  ];

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Rate Cards — Circle Rate (AUTHORITATIVE) vs Market Estimate */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="stat-card rounded-xl border-2 border-blue-300 bg-blue-50/60 dark:bg-blue-950/30 dark:border-blue-800 p-5 relative"
        >
          <span className="absolute -top-2 right-2 bg-blue-600 text-white text-[8px] px-1.5 py-0.5 rounded font-semibold">SOURCE OF TRUTH</span>
          <p className="text-xs text-blue-600 font-semibold uppercase tracking-wide">📋 Circle Rate</p>
          <p className="text-2xl font-bold text-blue-700 dark:text-blue-300 mt-2">{formatPerSqft(guidelineRate)}</p>
          <p className="text-xs text-blue-700 font-medium mt-1">{data.real_data.source}</p>
          <p className="text-[10px] text-muted-foreground">{data.real_data.lookup_method}</p>
          {data.real_data.matched?.village && (
            <p className="text-[10px] text-muted-foreground">📍 {data.real_data.matched.village}{data.real_data.matched.street ? `, ${data.real_data.matched.street}` : ''}</p>
          )}
          <span className={`inline-block mt-1 px-1.5 py-0.5 rounded text-[9px] font-semibold ${(data.real_data.confidence_score || 0) >= 0.7 ? 'bg-green-100 text-green-700' :
              (data.real_data.confidence_score || 0) >= 0.5 ? 'bg-amber-100 text-amber-700' :
                'bg-red-100 text-red-700'
            }`}>{Math.round((data.real_data.confidence_score || 0) * 100)}% confidence</span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="stat-card rounded-xl border border-gray-200 bg-gray-50/50 dark:bg-gray-900/20 dark:border-gray-700 p-5 relative"
        >
          <span className="absolute -top-2 right-2 bg-gray-500 text-white text-[8px] px-1.5 py-0.5 rounded font-semibold">ESTIMATE ONLY</span>
          <p className="text-xs text-gray-500 font-semibold uppercase tracking-wide">📊 Market Estimate</p>
          <p className="text-2xl font-bold text-gray-600 dark:text-gray-400 mt-2">{formatPerSqft(mlRate)}</p>
          <p className="text-xs text-muted-foreground mt-1">{data.ml_prediction.model}</p>
          <p className="text-[9px] text-amber-600 mt-1">⚠️ Non-authoritative — does not override circle rate</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="stat-card stat-card-emerald"
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">Best Use</p>
              <p className="text-2xl font-bold text-foreground mt-2">{data.predictions.land_use.predicted_use}</p>
              <p className="text-xs text-muted-foreground mt-1">Risk: {data.predictions.risk_analysis.risk_level}</p>
            </div>
            <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-muted-foreground" />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Confidence Meter + Feature Weights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass-card p-6 flex flex-col items-center">
          <h3 className="text-sm font-semibold text-foreground mb-4">Confidence Meter</h3>
          <div className="w-40 h-40 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={confidenceData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={70}
                  startAngle={90}
                  endAngle={-270}
                  dataKey="value"
                  strokeWidth={0}
                >
                  <Cell fill="hsl(160, 84%, 39%)" />
                  <Cell fill="hsl(210, 15%, 92%)" />
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-3xl font-bold text-foreground">{confidence}%</span>
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-2">Model: {data.ml_prediction.model}</p>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-sm font-semibold text-foreground mb-4">ML Feature Weights</h3>
          <div className="bg-muted rounded-xl p-4 font-mono text-sm text-foreground">
            <p className="text-muted-foreground text-xs mb-2">Linear Regression Coefficients</p>
            <div className="space-y-2 text-xs">
              {Object.entries(weights).map(([key, val]) => (
                <div key={key} className="flex justify-between">
                  <span className="text-muted-foreground capitalize">{key.replace(/_/g, ' ')}</span>
                  <span className={val > 0 ? "text-primary" : "text-destructive"}>{val > 0 ? '+' : ''}{val}</span>
                </div>
              ))}
              <hr className="border-border" />
              <div className="flex justify-between font-semibold text-sm">
                <span>ML Rate</span>
                <span className="text-primary">{formatPerSqft(mlRate)}</span>
              </div>
              <div className="flex justify-between font-semibold text-sm text-blue-600">
                <span>Guideline Rate</span>
                <span>{formatPerSqft(guidelineRate)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Indices */}
      <div>
        <h3 className="text-sm font-semibold text-foreground mb-3">Feature Indices</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {factors.map((f, i) => (
            <motion.div
              key={f.label}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + i * 0.05 }}
              className="glass-card-hover p-4 flex items-center gap-4"
            >
              <div className="w-9 h-9 rounded-lg bg-muted flex items-center justify-center flex-shrink-0">
                <f.icon className="w-4 h-4 text-muted-foreground" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-foreground">{f.label}</p>
                <div className="flex items-center gap-2 mt-1">
                  <Progress value={f.value} className="flex-1 h-1.5" />
                  <span className="text-xs text-muted-foreground">{f.value}%</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
