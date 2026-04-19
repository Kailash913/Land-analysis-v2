import { Map, Calculator, Sprout, ShieldAlert, FileText, Landmark, ChevronLeft, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";
import { useNavigation, PageId } from "@/contexts/NavigationContext";
import { useState } from "react";

const navItems: { id: PageId; label: string; icon: React.ElementType }[] = [
  { id: "map", label: "Interactive Map", icon: Map },
  { id: "valuation", label: "Valuation Engine", icon: Calculator },
  { id: "agriculture", label: "Agricultural Insights", icon: Sprout },
  { id: "risk", label: "Risk & Simulation", icon: ShieldAlert },
  { id: "reports", label: "Reports", icon: FileText },
];

export function AppSidebar() {
  const { activePage, setActivePage } = useNavigation();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-sidebar flex flex-col z-50 transition-all duration-300 ${
        collapsed ? "w-[68px]" : "w-64"
      }`}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-sidebar-border">
        <div className="w-9 h-9 rounded-lg bg-sidebar-primary flex items-center justify-center flex-shrink-0">
          <Landmark className="w-5 h-5 text-sidebar-primary-foreground" />
        </div>
        {!collapsed && (
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="font-bold text-sidebar-primary-foreground text-lg tracking-tight"
          >
            LRES
          </motion.span>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 px-2 space-y-1">
        {navItems.map((item) => {
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group relative ${
                isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-md"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              }`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span>{item.label}</span>}
              {isActive && (
                <motion.div
                  layoutId="sidebar-indicator"
                  className="absolute inset-0 rounded-xl bg-sidebar-primary -z-10"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
            </button>
          );
        })}
      </nav>

      {/* Admin badge */}
      <div className="px-3 pb-3">
        {!collapsed && (
          <div className="px-3 py-2 rounded-xl bg-sidebar-accent text-xs text-sidebar-muted flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-sidebar-primary animate-pulse-slow" />
            <span>Admin Access</span>
          </div>
        )}
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-20 w-6 h-6 rounded-full bg-card border border-border flex items-center justify-center shadow-sm hover:bg-muted transition-colors"
      >
        {collapsed ? <ChevronRight className="w-3 h-3" /> : <ChevronLeft className="w-3 h-3" />}
      </button>
    </aside>
  );
}
