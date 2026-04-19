import { useState, useMemo } from "react";
import { AlertTriangle, Shield, Flame, CloudRain, TrendingDown } from "lucide-react";
import { Slider } from "@/components/ui/slider";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";
import { useEvaluation } from "@/contexts/EvaluationContext";
import { formatPerSqft } from "@/services/api";

const levelConfig = {
  High: { border: "risk-border-high", badge: "bg-destructive/10 text-destructive" },
  Medium: { border: "risk-border-moderate", badge: "bg-accent/10 text-accent" },
  Low: { border: "risk-border-low", badge: "bg-primary/10 text-primary" },
} as const;

const riskIcons = [CloudRain, TrendingDown, Flame, AlertTriangle, Shield];

function generateProjection(baseSqft: number, urban: number, infra: number) {
  return Array.from({ length: 6 }, (_, i) => {
    const year = 2024 + i;
    const urbanEffect = (urban / 100) * i * (baseSqft * 0.06);
    const infraEffect = (infra / 100) * i * (baseSqft * 0.04);
    return {
      year: year.toString(),
      value: Math.round(baseSqft + urbanEffect + infraEffect),
    };
  });
}

export function RiskSimulationPage() {
  const [urbanGrowth, setUrbanGrowth] = useState(40);
  const [infraDev, setInfraDev] = useState(55);
  const { data } = useEvaluation();

  const baseSqft = data?.ml_prediction.predicted_rate_per_sqft || 500;
  const projectionData = useMemo(() => generateProjection(baseSqft, urbanGrowth, infraDev), [baseSqft, urbanGrowth, infraDev]);

  const riskFactors = data?.predictions.risk_analysis.risk_factors || [];
  const riskLevel = (data?.predictions.risk_analysis.risk_level || "Low") as keyof typeof levelConfig;

  if (!data) {
    return (
      <div className="glass-card p-8 text-center max-w-6xl">
        <p className="text-muted-foreground">Click a location on the <b>Interactive Map</b> first to see risk analysis.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Risk Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5 text-center">
          <p className="text-xs text-muted-foreground">Risk Level</p>
          <p className={`text-3xl font-bold mt-1 ${riskLevel === 'High' ? 'text-destructive' :
              riskLevel === 'Medium' ? 'text-amber-500' : 'text-primary'
            }`}>{riskLevel}</p>
        </div>
        <div className="glass-card p-5 text-center">
          <p className="text-xs text-muted-foreground">Risk Score</p>
          <p className="text-3xl font-bold text-foreground mt-1">{data.predictions.risk_analysis.risk_score}/100</p>
        </div>
        <div className="glass-card p-5 text-center">
          <p className="text-xs text-muted-foreground">Model</p>
          <p className="text-lg font-bold text-foreground mt-1">{data.predictions.risk_analysis.model}</p>
        </div>
      </div>

      {/* Risk Factor Cards */}
      <div>
        <h3 className="text-sm font-semibold text-foreground mb-3">Risk Factors</h3>
        <div className="space-y-3">
          {riskFactors.map((factor, i) => {
            const Icon = riskIcons[i % riskIcons.length];
            return (
              <motion.div
                key={factor}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className={`glass-card p-4 ${levelConfig[riskLevel]?.border || ''} flex items-center gap-4`}
              >
                <div className="w-9 h-9 rounded-lg bg-muted flex items-center justify-center flex-shrink-0">
                  <Icon className="w-4 h-4 text-muted-foreground" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-foreground">{factor}</p>
                </div>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${levelConfig[riskLevel]?.badge || ''}`}>
                  {riskLevel}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* What-If Simulator */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold text-foreground mb-5">What-If Simulator — Rate Projection (₹/sq.ft)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-medium text-foreground">Urban Growth</label>
              <span className="text-xs font-semibold text-primary">{urbanGrowth}%</span>
            </div>
            <Slider value={[urbanGrowth]} onValueChange={([v]) => setUrbanGrowth(v)} max={100} step={5} className="w-full" />
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-medium text-foreground">Infrastructure Development</label>
              <span className="text-xs font-semibold text-primary">{infraDev}%</span>
            </div>
            <Slider value={[infraDev]} onValueChange={([v]) => setInfraDev(v)} max={100} step={5} className="w-full" />
          </div>
        </div>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={projectionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(214, 20%, 90%)" />
              <XAxis dataKey="year" tick={{ fontSize: 12 }} stroke="hsl(215, 15%, 50%)" />
              <YAxis tick={{ fontSize: 12 }} stroke="hsl(215, 15%, 50%)" tickFormatter={(v) => `₹${v}`} />
              <Tooltip
                contentStyle={{
                  background: "hsl(0, 0%, 100%)",
                  border: "1px solid hsl(214, 20%, 90%)",
                  borderRadius: "12px",
                  fontSize: "12px",
                }}
                formatter={(value: number) => [formatPerSqft(value), "Projected Rate"]}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="hsl(160, 84%, 39%)"
                strokeWidth={2.5}
                dot={{ fill: "hsl(160, 84%, 39%)", r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Risk Probabilities */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold text-foreground mb-3">Risk Probability Distribution</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          {Object.entries(data.predictions.risk_analysis.probabilities).map(([level, pct]) => (
            <div key={level}>
              <p className={`text-2xl font-bold ${level === 'High' ? 'text-destructive' :
                  level === 'Medium' ? 'text-amber-500' : 'text-primary'
                }`}>{pct}%</p>
              <p className="text-xs text-muted-foreground">{level} Risk</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
