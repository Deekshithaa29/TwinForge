import type Telemetry from "./telemetry";

export default interface TelemetryState {
    latestTelemetry: Telemetry | null;
    telemetryHistory: Telemetry[];
}