import { useEffect, useState } from "react";

import { getLatestTelemetry } from "../api/telemetry";
import type Telemetry from "../types/telemetry";

const WS_URL = "ws://localhost:8000/ws/telemetry";

export function useTelemetry() {
    const [telemetry, setTelemetry] =
        useState<Telemetry | null>(null);

    useEffect(() => {
        loadTelemetry();

        const ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            console.log("WebSocket connected");
        };

        ws.onmessage = (event) => {
            const data: Telemetry = JSON.parse(event.data);
            setTelemetry(data);
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
            setTelemetry(data);
        }
        catch (error) {
            console.error("Failed to load telemetry", error);
        }
    }

    return telemetry;
}