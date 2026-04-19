import React, { createContext, useContext, useState, useCallback } from "react";
import { EvaluationResult, evaluateLand } from "@/services/api";

interface EvaluationContextType {
    data: EvaluationResult | null;
    isLoading: boolean;
    error: string | null;
    evaluate: (lat: number, lng: number) => Promise<void>;
}

const EvaluationContext = createContext<EvaluationContextType>({
    data: null,
    isLoading: false,
    error: null,
    evaluate: async () => { },
});

export function EvaluationProvider({ children }: { children: React.ReactNode }) {
    const [data, setData] = useState<EvaluationResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const evaluate = useCallback(async (lat: number, lng: number) => {
        setIsLoading(true);
        setError(null);
        try {
            const result = await evaluateLand(lat, lng);
            setData(result);
        } catch (err: any) {
            setError(err.message || "Evaluation failed");
            console.error("Evaluation error:", err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return (
        <EvaluationContext.Provider value={{ data, isLoading, error, evaluate }}>
            {children}
        </EvaluationContext.Provider>
    );
}

export function useEvaluation() {
    return useContext(EvaluationContext);
}
