export default interface Telemetry {
    timestamp: string;

    machine_id: string;
    machine_name: string;
    machine_type: string;

    status: string;

    temperature: number;
    vibration: number;

    current_rpm: number;
    load: number;

    health: number;
    health_state: string;

    runtime_hours: number;
    predicted_rul_hours: number | null;

    maintenance_status: string | null;
    maintenance_severity: string | null;
    maintenance_message: string | null;
    recommended_action: string | null;
}