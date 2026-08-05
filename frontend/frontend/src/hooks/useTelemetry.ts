import { useEffect, useState } from "react";
import type TelemetryState from "../types/telemetryState"
import { getLatestTelemetry } from "../api/telemetry";
import type Telemetry from "../types/telemetry";

const WS_URL = "ws://localhost:8000/ws/telemetry";

export function useTelemetry() {

    const [state, setState] = useState<TelemetryState>({
        latestTelemetry: null,
        telemetryHistory: [],
    });

    useEffect(() => {
        loadTelemetry();

        const ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            console.log("WebSocket connected");
        };

        ws.onmessage = (event) => {
            const data: Telemetry = JSON.parse(event.data);
            setState((prev) => ({
                latestTelemetry: data,

                telemetryHistory: [...prev.telemetryHistory, data].slice(-100), // Keep only the last 100 telemetry entries
            }));
            //setTelemetry(data);
        };

        ws.onerror = (error) => {
            console.error("WebSocket error", error);
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected");
        };

        return () => {
            ws.close();
        };
    }, []);

    async function loadTelemetry() {
        try {
            const data = await getLatestTelemetry();
            setState((prev) => {

                if (prev.latestTelemetry) {
                    return prev;
                }

                return{
                    ...prev,
                    latestTelemetry: data,
                    telemetryHistory: [data],
                };
            });
        }
        catch (error) {
            console.error("Failed to load telemetry", error);
        }
    }

    return state;
}