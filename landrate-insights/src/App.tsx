import { NavigationProvider } from "@/contexts/NavigationContext";
import { EvaluationProvider } from "@/contexts/EvaluationContext";
import { AppLayout } from "@/components/layout/AppLayout";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <EvaluationProvider>
        <NavigationProvider>
          <AppLayout />
        </NavigationProvider>
      </EvaluationProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
