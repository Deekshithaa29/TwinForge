import type Telemetry from "../../types/telemetry";
import StatusBadge from "./StatusBadge";

interface MachineHeaderProps {
    telemetry: Telemetry;
}

export default function MachineHeader({
    telemetry,
}: MachineHeaderProps) {
    return (
        <div className="mb-8 flex items-start justify-between">

            <div>

                <h1 className="text-4xl font-bold text-slate-900">
                    TwinForge
                </h1>

                <p className="mt-2 text-2xl font-semibold text-slate-700">
                    {telemetry.machine_name}
                </p>

                <div className="mt-4 space-y-1 text-sm text-slate-500">

                    <p>
                        Machine Type:
                        <span className="ml-2 font-medium text-slate-700">
                            {telemetry.machine_type}
                        </span>
                    </p>

                    <p>
                        Machine ID:
                        <span className="ml-2 font-mono text-slate-700">
                            {telemetry.machine_id.slice(0, 8)}...
                        </span>
                    </p>

                    <p>
                        Last Update:
                        <span className="ml-2 font-medium text-slate-700">
                            {new Date(telemetry.timestamp).toLocaleTimeString()}
                        </span>
                    </p>

                </div>

            </div>

            <StatusBadge status={telemetry.status} />

        </div>
    );
}