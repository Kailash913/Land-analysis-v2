import { AppSidebar } from "./AppSidebar";
import { AppHeader } from "./AppHeader";
import { AnimatePresence, motion } from "framer-motion";
import { useNavigation } from "@/contexts/NavigationContext";
import { InteractiveMapPage } from "@/pages/InteractiveMapPage";
import { ValuationEnginePage } from "@/pages/ValuationEnginePage";
import { AgriculturalInsightsPage } from "@/pages/AgriculturalInsightsPage";
import { RiskSimulationPage } from "@/pages/RiskSimulationPage";
import { ReportsPage } from "@/pages/ReportsPage";

const pageComponents = {
  map: InteractiveMapPage,
  valuation: ValuationEnginePage,
  agriculture: AgriculturalInsightsPage,
  risk: RiskSimulationPage,
  reports: ReportsPage,
};

export function AppLayout() {
  const { activePage } = useNavigation();
  const PageComponent = pageComponents[activePage];

  return (
    <div className="min-h-screen flex">
      <AppSidebar />
      <div className="flex-1 ml-64 flex flex-col transition-all duration-300">
        <AppHeader />
        <main className="flex-1 p-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
            >
              <PageComponent />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
