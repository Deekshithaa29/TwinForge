import type Telemetry from "../../types/telemetry";

interface SystemStatusProps {
    telemetry: Telemetry;
}

export default function SystemStatus({
    telemetry,
}: SystemStatusProps) {
    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-6 text-lg font-semibold">
                System Status
            </h2>

            <div className="grid grid-cols-2 gap-y-4">

                <span className="text-slate-500">
                    Backend
                </span>

                <span className="font-medium text-green-600">
                    🟢 Connected
                </span>

                <span className="text-slate-500">
                    WebSocket
                </span>

                <span className="font-medium text-green-600">
                    🟢 Connected
                </span>

                <span className="text-slate-500">
                    MQTT
                </span>

                <span className="font-medium text-green-600">
                    🟢 Connected
                </span>

                <span className="text-slate-500">
                    Update Rate
                </span>

                <span className="font-medium">
                    1 second
                </span>

                <span className="text-slate-500">
                    Last Update
                </span>

                <span className="font-medium">
                    {new Date(telemetry.timestamp).toLocaleTimeString()}
                </span>

            </div>

        </div>
    );
}