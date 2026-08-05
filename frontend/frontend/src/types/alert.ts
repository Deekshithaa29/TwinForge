import type { AlertSeverity } from "./alertSeverity";

export default interface Alert {
    severity: AlertSeverity;
    message: string;
}