import type Telemetry from "../../types/telemetry";
import MetricCard from "./MetricCard";

interface MetricsGridProps {
    telemetry: Telemetry;
}

export default function MetricsGrid({
    telemetry,
}: MetricsGridProps) {
    return (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">

            <MetricCard
                title="Temperature"
                value={telemetry.temperature.toFixed(2)}
                unit="°C"
            />

            <MetricCard
                title="RPM"
                value={telemetry.current_rpm.toFixed(0)}
                unit="RPM"
            />

            <MetricCard
                title="Health"
                value={telemetry.health.toFixed(2)}
                unit="%"
            />

            <MetricCard
                title="Load"
                value={(telemetry.load * 100).toFixed(0)}
                unit="%"
            />

            <MetricCard
                title="Vibration"
                value={telemetry.vibration.toFixed(2)}
                unit="mm/s"
            />

            <MetricCard
                title="Predicted Remaining Useful Life"
                value={telemetry.predicted_rul_hours !==null ? telemetry.predicted_rul_hours.toFixed(2) : "--"}
                unit="hrs"
            />

        </div>
    );
}