import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

import type Telemetry from "../../types/telemetry";

interface TelemetryChartProps {
    title: string;
    data: Telemetry[];
    dataKey: keyof Telemetry;
    unit: string;
}

export default function TelemetryChart({
    title,
    data,
    dataKey,
    unit,
}: TelemetryChartProps) {

    const chartData = data.map((item) => ({
        time: new Date(item.timestamp).toLocaleTimeString(),
        value: item[dataKey] as number,
    }));

    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-4 text-lg font-semibold">
                {title}
            </h2>

            <div className="h-72">

                <ResponsiveContainer width="100%" height="100%">

                    <LineChart data={chartData}>

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis
                            dataKey="time"
                            tick={{ fontSize: 12 }}
                        />

                        <YAxis
                            tick={{ fontSize: 12 }}
                            unit={unit}
                        />

                        <Tooltip />

                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={false}
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

        </div>
    );
}