import DashboardLayout from "../components/layout/DashboardLayout";
import MetricCard from "../components/common/MetricCard";
import StatusBadge from "../components/common/StatusBadge";
import {useTelemetry} from "../hooks/useTelemetry";

export default function Dashboard() {

    const telemetry = useTelemetry();

    if (!telemetry) {
        return <h2>Loading...</h2>;
    }

return (
    <DashboardLayout>

        <div className="mb-8 flex items-center justify-between">

            <div>

                <h1 className="text-4xl font-bold">
                    TwinForge Dashboard
                </h1>

                <p className="text-slate-500">
                    {telemetry.machine_name}
                </p>

            </div>

            <StatusBadge
                status={telemetry.status}
            />

        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">

            <MetricCard
                title="Temperature"
                value={telemetry.temperature.toFixed(2) ?? "0.00"}
                unit="°C"
            />

            <MetricCard
                title="RPM"
                value={telemetry.current_rpm.toFixed(0) ?? "0"}
                unit="RPM"
            />

            <MetricCard
                title="Health"
                value={telemetry.health.toFixed(2) ?? "0.00"}
                unit="%"
            />

            <MetricCard
                title="Load"
                value={(telemetry.load * 100).toFixed(0) ?? "0"}
                unit="%"
            />

            <MetricCard
                title="Vibration"
                value={telemetry.vibration.toFixed(2) ?? "0.00"}
                unit="mm/s"
            />

        </div>

    </DashboardLayout>
);
}