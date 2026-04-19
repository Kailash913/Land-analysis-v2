import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Droplets, Sun, Cloud, Sprout } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Progress } from "@/components/ui/progress";
import { motion } from "framer-motion";
import { useEvaluation } from "@/contexts/EvaluationContext";

export function AgriculturalInsightsPage() {
  const [activeTab, setActiveTab] = useState("landuse");
  const { data } = useEvaluation();

  // Land use comparison from simulations
  const landUseData = data?.simulations.land_use_comparison.suitability.map(s => ({
    label: s.use,
    value: Math.round(s.percentage),
    recommended: s.use === data.simulations.land_use_comparison.best_use,
  })) || [
      { label: "Agricultural", value: 65, recommended: true },
      { label: "Residential", value: 20, recommended: false },
      { label: "Commercial", value: 15, recommended: false },
    ];

  // Crop cards from ML predictions
  const crops = data?.predictions.crop_recommendations.top_crops.map(c => ({
    name: c.crop,
    suitability: c.suitability_pct,
    water: c.water_need,
    season: c.season.split(" ")[0], // Take just "Kharif" from "Kharif (Jun-Oct)"
    fullSeason: c.season,
  })) || [];

  // Water analysis from simulations
  const waterData = data?.simulations.water_analysis.water_analysis.map(w => ({
    crop: w.crop,
    Rainfall: w.available_rainfall_mm,
    "Water Need": w.water_need_mm,
    Deficit: w.deficit_mm,
  })) || [];

  // Crop rotation from simulations
  const rotationSteps = data?.simulations.crop_rotation.rotation_plan.map(r => ({
    crop: r.crop,
    period: `Year ${r.year} — ${r.season}`,
    benefit: r.benefit,
    icon: r.season === "Kharif" ? Sprout : r.season === "Rabi" ? Sun : Cloud,
  })) || [];

  return (
    <div className="max-w-6xl">
      {!data && (
        <div className="glass-card p-8 text-center">
          <p className="text-muted-foreground">Click a location on the <b>Interactive Map</b> first to see agricultural insights.</p>
        </div>
      )}

      {data && (
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="landuse">Land Use</TabsTrigger>
            <TabsTrigger value="crops">Crop Grid</TabsTrigger>
            <TabsTrigger value="water">Water & Rotation</TabsTrigger>
          </TabsList>

          <TabsContent value="landuse">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card p-6 space-y-5">
              <h3 className="text-sm font-semibold text-foreground">Land Use Comparison (Simulation)</h3>
              {landUseData.map((item) => (
                <div key={item.label} className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-foreground">{item.label}</span>
                      {item.recommended && <span className="badge-emerald text-[10px]">Recommended</span>}
                    </div>
                    <span className="text-sm font-semibold text-foreground">{item.value}%</span>
                  </div>
                  <Progress value={item.value} className="h-3 rounded-full" />
                </div>
              ))}
              <p className="text-xs text-muted-foreground">Best use: <b>{data.simulations.land_use_comparison.best_use}</b> | ML prediction: <b>{data.predictions.land_use.predicted_use}</b></p>
            </motion.div>
          </TabsContent>

          <TabsContent value="crops">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {crops.map((crop, i) => (
                  <motion.div
                    key={crop.name}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.06 }}
                    className="glass-card-hover p-5"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-semibold text-foreground">{crop.name}</h4>
                      <span className={`badge-${crop.season === "Rabi" ? "blue" : crop.season === "Year-round" ? "teal" : "emerald"}`}>
                        {crop.season}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 mb-3">
                      <div className="relative w-14 h-14">
                        <svg className="w-14 h-14 -rotate-90" viewBox="0 0 56 56">
                          <circle cx="28" cy="28" r="22" fill="none" stroke="hsl(var(--muted))" strokeWidth="5" />
                          <circle
                            cx="28" cy="28" r="22" fill="none"
                            stroke="hsl(var(--emerald))"
                            strokeWidth="5"
                            strokeDasharray={`${(crop.suitability / 100) * 138} 138`}
                            strokeLinecap="round"
                          />
                        </svg>
                        <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-foreground">
                          {crop.suitability}%
                        </span>
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <Droplets className="w-3 h-3" />
                          <span>Water: {crop.water}</span>
                        </div>
                        <p className="text-xs text-muted-foreground">{crop.fullSeason}</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Crop Rotation Timeline */}
              {rotationSteps.length > 0 && (
                <div className="glass-card p-6">
                  <h3 className="text-sm font-semibold text-foreground mb-2">Crop Rotation Plan — {data.simulations.crop_rotation.primary_crop}</h3>
                  <p className="text-xs text-muted-foreground mb-4">{data.simulations.crop_rotation.rationale}</p>
                  <div className="flex items-center gap-2">
                    {rotationSteps.map((step, i) => (
                      <div key={i} className="flex items-center flex-1">
                        <div className="flex-1 bg-muted rounded-xl p-3 text-center">
                          <step.icon className="w-5 h-5 mx-auto mb-1 text-primary" />
                          <p className="text-xs font-semibold text-foreground">{step.crop}</p>
                          <p className="text-[10px] text-muted-foreground">{step.period}</p>
                        </div>
                        {i < rotationSteps.length - 1 && (
                          <div className="w-6 h-0.5 bg-border flex-shrink-0" />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          </TabsContent>

          <TabsContent value="water">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              <div className="glass-card p-6">
                <h3 className="text-sm font-semibold text-foreground mb-4">Water Requirement vs Rainfall (mm)</h3>
                <p className="text-xs text-muted-foreground mb-4">Annual Rainfall: {data.simulations.water_analysis.annual_rainfall_mm}mm</p>
                {waterData.length > 0 ? (
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={waterData} barGap={2}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(214, 20%, 90%)" />
                        <XAxis dataKey="crop" tick={{ fontSize: 11 }} stroke="hsl(215, 15%, 50%)" />
                        <YAxis tick={{ fontSize: 12 }} stroke="hsl(215, 15%, 50%)" />
                        <Tooltip
                          contentStyle={{
                            background: "hsl(0, 0%, 100%)",
                            border: "1px solid hsl(214, 20%, 90%)",
                            borderRadius: "12px",
                            fontSize: "12px",
                          }}
                        />
                        <Legend />
                        <Bar dataKey="Rainfall" fill="hsl(217, 91%, 50%)" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Water Need" fill="hsl(38, 92%, 50%)" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No water analysis data.</p>
                )}
              </div>

              {/* Detailed water status */}
              <div className="glass-card p-6">
                <h3 className="text-sm font-semibold text-foreground mb-3">Irrigation Status</h3>
                <div className="space-y-3">
                  {data.simulations.water_analysis.water_analysis.map((w, i) => (
                    <div key={i} className="flex items-center justify-between text-sm">
                      <span className="font-medium text-foreground">{w.crop}</span>
                      <span className={`text-xs px-2 py-1 rounded ${w.deficit_mm === 0 ? 'bg-primary/10 text-primary' :
                          w.deficit_mm < 300 ? 'badge-amber' : 'bg-destructive/10 text-destructive'
                        }`}>{w.status}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}
