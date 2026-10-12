interface HealthStateBadgeProps {
    healthState: string;
}

export default function HealthStateBadge({
    healthState,
}: HealthStateBadgeProps) {
    const state = healthState.toUpperCase();

    const colorClasses: Record<string, string> = {
        HEALTHY: "bg-green-100 text-green-700",
        DEGRADED: "bg-yellow-100 text-yellow-700",
        CRITICAL: "bg-orange-100 text-orange-700",
        FAILED: "bg-red-100 text-red-700",
    };

    const colorClass =
        colorClasses[state] ?? "bg-gray-100 text-gray-700";

    return (
        <span
            className={`
                inline-flex items-center
                rounded-full px-4 py-2
                text-sm font-semibold
                ${colorClass}
            `}
        >
            {state}
        </span>
    );
}