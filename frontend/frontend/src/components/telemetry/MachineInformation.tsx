import type Telemetry from "../../types/telemetry";

interface MachineInformationProps {
    telemetry: Telemetry;
}

export default function MachineInformation({
    telemetry,
}: MachineInformationProps) {
    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-6 text-lg font-semibold">
                Machine Information
            </h2>

            <div className="grid grid-cols-2 gap-y-4">

                <span className="text-slate-500">
                    Machine Name
                </span>

                <span className="font-medium">
                    {telemetry.machine_name}
                </span>

                <span className="text-slate-500">
                    Machine ID
                </span>

                <span className="truncate font-medium">
                    {telemetry.machine_id}
                </span>

                <span className="text-slate-500">
                    Machine Type
                </span>

                <span className="font-medium">
                    {telemetry.machine_type}
                </span>

                <span className="text-slate-500">
                    Status
                </span>

                <span className="font-medium">
                    {telemetry.status}
                </span>

                <span className="text-slate-500">
                    Runtime
                </span>

                <span className="font-medium">
                    {telemetry.runtime_hours.toFixed(2)} hrs
                </span>

                <span className="text-slate-500">
                    Last Updated
                </span>

                <span className="font-medium">
                    {new Date(telemetry.timestamp).toLocaleTimeString()}
                </span>

            </div>

        </div>
    );
}