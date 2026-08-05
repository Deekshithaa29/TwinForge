import type Alert from "../../types/alert";

interface AlertRowProps {
    alert: Alert;
}

export default function AlertRow({
    alert,
}: AlertRowProps) {

    const styles = {
        critical:
            "border-red-200 bg-red-50 text-red-700",

        warning:
            "border-yellow-200 bg-yellow-50 text-yellow-700",

        info:
            "border-blue-200 bg-blue-50 text-blue-700",
    };

    const icons = {
        critical: "🔴",
        warning: "🟡",
        info: "🔵",
    };

    return (
        <div
            className={`rounded-lg border p-4 ${styles[alert.severity]}`}
        >
            <span className="mr-2">
                {icons[alert.severity]}
            </span>

            {alert.message}
        </div>
    );
}