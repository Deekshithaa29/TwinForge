interface MetricCardProps {
    title: string;
    value: string | number;
    unit?: string;
}

export default function MetricCard({
    title,
    value,
    unit,
}: MetricCardProps) {
    return (
        <div className="rounded-xl bg-white p-6 shadow-md">
            <p className="text-sm font-medium text-slate-500">
                {title}
            </p>

            <div className="mt-3 flex items-end gap-2">
                <span className="text-3xl font-bold text-slate-900">
                    {value}
                </span>

                {unit && (
                    <span className="text-slate-500">
                        {unit}
                    </span>
                )}
            </div>
        </div>
    );
}