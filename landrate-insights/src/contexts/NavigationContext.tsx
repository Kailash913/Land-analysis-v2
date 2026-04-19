import React, { createContext, useContext, useState, useCallback } from "react";

export type PageId = "map" | "valuation" | "agriculture" | "risk" | "reports";

interface NavigationContextType {
  activePage: PageId;
  setActivePage: (page: PageId) => void;
  pageTitle: string;
}

const pageTitles: Record<PageId, string> = {
  map: "Interactive Map",
  valuation: "Valuation Engine",
  agriculture: "Agricultural Insights",
  risk: "Risk & Simulation",
  reports: "Reports & Export",
};

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activePage, setActivePageState] = useState<PageId>("map");

  const setActivePage = useCallback((page: PageId) => {
    setActivePageState(page);
  }, []);

  const pageTitle = pageTitles[activePage];

  return (
    <NavigationContext.Provider value={{ activePage, setActivePage, pageTitle }}>
      {children}
    </NavigationContext.Provider>
  );
};

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) throw new Error("useNavigation must be used within NavigationProvider");
  return context;
};
