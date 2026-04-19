import { MapPin } from "lucide-react";
import { useNavigation } from "@/contexts/NavigationContext";
import { useEvaluation } from "@/contexts/EvaluationContext";

export function AppHeader() {
  const { pageTitle } = useNavigation();
  const { data } = useEvaluation();

  const lat = data?.coordinates.lat?.toFixed(4) || "—";
  const lng = data?.coordinates.lng?.toFixed(4) || "—";

  // Build admin hierarchy: village → taluk → district → state
  const parts = [
    data?.location.village,
    data?.location.taluk,
    data?.location.district,
    data?.location.state,
  ].filter(Boolean);
  // Deduplicate adjacent identical parts
  const uniqueParts = parts.filter((p, i) => i === 0 || p !== parts[i - 1]);
  const locationLabel = uniqueParts.length > 0 ? uniqueParts.join(" → ") : "";

  return (
    <header className="h-16 border-b border-border bg-card/60 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-40">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold text-foreground">{pageTitle}</h1>
        <div className="hidden sm:flex items-center gap-1.5 text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">
          <MapPin className="w-3.5 h-3.5" />
          <span>{lat}° N, {lng}° E</span>
        </div>
        {locationLabel && (
          <span className="hidden md:inline text-xs text-muted-foreground">{locationLabel}</span>
        )}
      </div>
    </header>
  );
}
