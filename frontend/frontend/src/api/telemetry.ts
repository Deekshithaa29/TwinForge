import axios from "axios";
import type Telemetry from "../types/telemetry";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export async function getLatestTelemetry(): Promise<Telemetry> {
    const response = await api.get<Telemetry>(
        "/telemetry/latest"
    );

    return response.data;
}