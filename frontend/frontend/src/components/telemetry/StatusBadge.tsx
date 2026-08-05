interface StatusBadgeProps {
    status: string;
}

export default function StatusBadge({
    status,
}: StatusBadgeProps) {

    const color =
        status === "RUNNING"
            ? "bg-green-500"
            : "bg-red-500";

    return (
        <div className="flex items-center gap-2">

            <span
                className={`h-3 w-3 rounded-full ${color}`}
            />

            <span className="font-semibold">
                {status}
            </span>

        </div>
    );
}