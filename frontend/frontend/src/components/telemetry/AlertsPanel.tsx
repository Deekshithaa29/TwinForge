import type Alert from "../../types/alert";
import type Telemetry from "../../types/telemetry";
import AlertRow from "./AlertCard";

interface AlertsPanelProps {
    telemetry: Telemetry;
}

export default function AlertsPanel({
    telemetry,
}: AlertsPanelProps) {

    const alerts: Alert[] = [];

    if (telemetry.temperature > 80) {
        alerts.push({
            severity: "critical",
            message: "High temperature detected.",
        });
    }

    if (telemetry.health < 95) {
        alerts.push({
            severity: "warning",
            message: "Machine health is degrading.",
        });
    }

    if (telemetry.vibration > 8) {
        alerts.push({
            severity: "warning",
            message: "Excessive vibration detected.",
        });
    }

    if (telemetry.load > 0.90) {
        alerts.push({
            severity: "info",
            message: "Machine operating under high load.",
        });
    }

    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-6 text-lg font-semibold">
                Active Alerts
            </h2>

            {alerts.length === 0 ? (
                <div className="rounded-lg border border-green-200 bg-green-50 p-4 text-green-700">
                    🟢 No active alerts.
                </div>
            ) : (
                <div className="space-y-3">

                    {alerts.map((alert, index) => (
                        <AlertRow
                            key={index}
                            alert={alert}
                        />
                    ))}

                </div>
            )}

        </div>
    );
}