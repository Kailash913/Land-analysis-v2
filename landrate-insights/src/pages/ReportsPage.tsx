import { useState, useEffect } from "react";
import { Download, FileSpreadsheet, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";
import { motion } from "framer-motion";
import { useEvaluation } from "@/contexts/EvaluationContext";
import { formatPerSqft, fetchEvaluations, getPdfUrl, getCsvUrl } from "@/services/api";

interface HistoryItem {
  id: string;
  state: string;
  district: string;
  predicted_rate: number;
  land_use: string;
  risk_level: string;
  created_at: string;
}

const riskBadge = (risk: string) => {
  const cls = risk === "High" ? "bg-destructive/10 text-destructive" : risk === "Medium" ? "badge-amber" : "badge-emerald";
  return <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>{risk}</span>;
};

export function ReportsPage() {
  const { toast } = useToast();
  const { data } = useEvaluation();
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    fetchEvaluations().then(setHistory).catch(() => { });
  }, [data]);

  const handlePdfDownload = () => {
    if (!data?.evaluation_id) {
      toast({ title: "No evaluation", description: "Evaluate a location first." });
      return;
    }
    window.open(getPdfUrl(data.evaluation_id), '_blank');
    toast({ title: "PDF Report", description: "Opening PDF report in new tab." });
  };

  const handleCsvDownload = () => {
    if (!data?.evaluation_id) {
      toast({ title: "No evaluation", description: "Evaluate a location first." });
      return;
    }
    window.open(getCsvUrl(data.evaluation_id), '_blank');
    toast({ title: "CSV Export", description: "Downloading CSV export." });
  };

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Summary */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
        <h3 className="text-sm font-semibold text-foreground mb-4">Current Evaluation Summary</h3>
        {data ? (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
            <div>
              <p className="text-xs text-muted-foreground">📋 Guideline Rate</p>
              <p className="text-lg font-bold text-blue-600 mt-1">{formatPerSqft(data.real_data.guideline_rate_per_sqft)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">🤖 ML Rate</p>
              <p className="text-lg font-bold text-emerald-600 mt-1">{formatPerSqft(data.ml_prediction.predicted_rate_per_sqft)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Location</p>
              <p className="text-sm font-bold text-foreground mt-1">{data.location.district}, {data.location.state}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Risk Level</p>
              <p className="text-lg font-bold text-foreground mt-1">{data.predictions.risk_analysis.risk_level}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Best Use</p>
              <p className="text-lg font-bold text-foreground mt-1">{data.predictions.land_use.predicted_use}</p>
            </div>
          </div>
        ) : (
          <p className="text-center text-muted-foreground">No evaluation yet. Click a location on the Interactive Map.</p>
        )}
      </motion.div>

      {/* Export Actions */}
      <div className="flex gap-3">
        <Button onClick={handlePdfDownload} disabled={!data?.evaluation_id} className="gap-2">
          <Download className="w-4 h-4" />
          Download PDF
        </Button>
        <Button variant="secondary" onClick={handleCsvDownload} disabled={!data?.evaluation_id} className="gap-2">
          <FileSpreadsheet className="w-4 h-4" />
          Export CSV
        </Button>
      </div>

      {/* Previous Evaluations Table */}
      {history.length > 0 && (
        <div className="glass-card overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Rate (₹/sq.ft)</TableHead>
                <TableHead>Land Use</TableHead>
                <TableHead>Risk</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {history.map((ev) => (
                <TableRow key={ev.id}>
                  <TableCell className="text-sm">{ev.created_at ? new Date(ev.created_at).toLocaleDateString() : "—"}</TableCell>
                  <TableCell className="text-sm font-medium">{ev.district}, {ev.state}</TableCell>
                  <TableCell className="text-sm">{ev.predicted_rate ? formatPerSqft(Math.round(ev.predicted_rate / 43560)) : "—"}</TableCell>
                  <TableCell><span className="badge-blue">{ev.land_use}</span></TableCell>
                  <TableCell>{riskBadge(ev.risk_level)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Disclaimer */}
      <div className="flex items-start gap-3 rounded-2xl p-4 bg-accent/10 border border-accent/20">
        <AlertTriangle className="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-medium text-foreground">Academic Use Notice</p>
          <p className="text-xs text-muted-foreground mt-0.5">
            Guideline rates are approximate circle/registration values from state government data. ML predictions are model-generated using environmental and infrastructure features. Neither should be used as the sole basis for financial decisions.
          </p>
        </div>
      </div>
    </div>
  );
}
