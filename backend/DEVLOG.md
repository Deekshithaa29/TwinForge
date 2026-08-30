# Changelog

## v0.5.0
- Added stable machine identifiers
- Added machine-specific telemetry history retrieval
- Integrated persisted telemetry history into frontend charts
- Added degradation model abstraction
- Added CNC spindle degradation model
- Linked machine health degradation to RPM, load, temperature and vibration
- Added degradation behavior validation
- Added degradation-focused automated tests
- Verified full test suite

## v0.4.0
- Added telemetry repository abstraction
- Added SQLite database integration
- Added SQLite telemetry repository
- Added persistent telemetry storage
- Added latest telemetry retrieval from database
- Added telemetry history retrieval from database
- Added database-to-telemetry object mapping
- Refactored TelemetryManager to use repository-based persistence
- Added in-memory telemetry repository for testing
- Updated telemetry API to support persistent storage
- Updated automated tests for repository-based telemetry management
- Improved telemetry persistence architecture
- Expanded automated test coverage

## v0.3.0
- Added FastAPI backend
- Added REST API endpoints
- Added application lifecycle management
- Added threaded simulation execution
- Added spindle physics engine
- Added dynamic machine load simulation
- Added dynamic RPM simulation
- Added vibration sensor simulation
- Enhanced temperature simulation
- Expanded telemetry model
- Added RPM, load and vibration to telemetry
- Improved MQTT telemetry payload
- Improved telemetry serialization
- Refactored machine update architecture
- Improved physics model extensibility
- Expanded automated tests

## v0.2.0
- Added event-driven simulation architecture
- Added SimulationContext
- Added tick listeners
- Added ConsoleTelemetryListener
- Added MQTTTelemetryListener
- Added MQTT publisher abstraction
- Integrated Mosquitto broker
- Added live telemetry streaming
- Improved telemetry management
- Expanded automated tests

## v0.1.0
- Initial TwinForge project structure
- Machine abstraction
- CNC spindle implementation
- Sensor framework
- Factory model
- Basic simulation