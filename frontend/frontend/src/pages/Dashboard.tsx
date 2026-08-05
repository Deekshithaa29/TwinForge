import DashboardLayout from "../components/layout/DashboardLayout";
import MachineHeader from "../components/telemetry/MachineHeader";
import MetricsGrid from "../components/telemetry/MetricsGrid";
import {useTelemetry} from "../hooks/useTelemetry";
import TelemetryChart from "../components/telemetry/TelemetryChart";
import MachineInformation from "../components/telemetry/MachineInformation";
import SystemStatus from "../components/telemetry/SystemStatus";
import AlertsPanel from "../components/telemetry/AlertsPanel";

export default function Dashboard() {

    const { latestTelemetry, telemetryHistory } = useTelemetry();

    if (!latestTelemetry) {
        return <h2>Loading...</h2>;
    }

return (
    
    <DashboardLayout>

        <MachineHeader telemetry={latestTelemetry} />

        <MetricsGrid telemetry={latestTelemetry} />

        <div className = "mt-8 grid grid-cols-1 gap-6 xl:grid-cols-2">

            <MachineInformation telemetry={latestTelemetry} />

            <SystemStatus telemetry={latestTelemetry} />

            <AlertsPanel telemetry={latestTelemetry} />

            <TelemetryChart
                title="Temperature"
                data={telemetryHistory}
                dataKey="temperature"
                unit="°C"
            />

            <TelemetryChart
                title="RPM"
                data={telemetryHistory}
                dataKey="current_rpm"
                unit="RPM"
            />

            <TelemetryChart
                title="Health"
                data={telemetryHistory}
                dataKey="health"
                unit="%"
            />

            <TelemetryChart
                title="Load"
                data={telemetryHistory}
                dataKey="load"
                unit="%"
            />

            <TelemetryChart
                title="Vibration"
                data={telemetryHistory}
                dataKey="vibration"
                unit="mm/s"
            />

        </div>

    </DashboardLayout>
);
}