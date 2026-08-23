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

    runtime_hours: number;
}