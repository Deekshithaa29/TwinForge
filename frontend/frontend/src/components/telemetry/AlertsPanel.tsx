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

    // Condition-based alerts
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

    const maintenanceStatus =
        telemetry.maintenance_status ?? "UNKNOWN";

    const isMaintenanceAlert =
        maintenanceStatus !== "NORMAL" &&
        maintenanceStatus !== "UNKNOWN";

    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-6 text-lg font-semibold">
                Predictive Maintenance
            </h2>

            <div className="mb-6 rounded-lg border p-4">

                <div className="flex items-center justify-between">

                    <span className="text-sm text-gray-500">
                        Maintenance Status
                    </span>

                    <span className="font-semibold">
                        {maintenanceStatus}
                    </span>

                </div>

                <div className="mt-3 flex items-center justify-between">

                    <span className="text-sm text-gray-500">
                        Predicted RUL
                    </span>

                    <span className="font-semibold">
                        {telemetry.predicted_rul_hours !== null
                            ? `${telemetry.predicted_rul_hours.toFixed(2)} hrs`
                            : "--"}
                    </span>

                </div>

                {telemetry.maintenance_message && (
                    <p className="mt-4 text-sm text-gray-700">
                        {telemetry.maintenance_message}
                    </p>
                )}

                {telemetry.recommended_action && (
                    <div className="mt-3 rounded-md bg-gray-50 p-3">
                        <p className="text-xs font-semibold text-gray-500">
                            RECOMMENDED ACTION
                        </p>

                        <p className="mt-1 text-sm text-gray-700">
                            {telemetry.recommended_action}
                        </p>
                    </div>
                )}

            </div>

            <h3 className="mb-3 text-sm font-semibold text-gray-700">
                Active Alerts
            </h3>

            {isMaintenanceAlert && telemetry.maintenance_message && (
                <div className="mb-3">
                    <AlertRow
                        alert={{
                            severity:
                                maintenanceStatus === "CRITICAL"
                                    ? "critical"
                                    : "warning",
                            message: telemetry.maintenance_message,
                        }}
                    />
                </div>
            )}

            {alerts.length === 0 && !isMaintenanceAlert ? (
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