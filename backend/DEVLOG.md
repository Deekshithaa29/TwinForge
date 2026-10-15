# Changelog

## v0.8.0

- Improved application lifecycle management with thread-safe startup and shutdown
- Added protection against duplicate application starts and repeated shutdown requests
- Added lifecycle state tracking to prevent restarting closed application instances
- Improved simulation engine thread safety using synchronization locks and stop events
- Prevented concurrent simulation execution and stop-before-start race conditions
- Replaced blocking simulation sleep with interruptible event-based waiting
- Ensured simulation threads terminate before application resources are released
- Added automated tests for application and simulation lifecycle reliability
- Improved SQLite database thread safety using `threading.RLock`
- Added atomic database transactions with automatic commit and rollback
- Enabled SQLite Write-Ahead Logging (WAL) mode
- Added safe database shutdown and protection against operations on closed connections
- Updated telemetry repository to use synchronized database transactions
- Optimized latest telemetry retrieval to fetch the newest record for each machine
- Added deterministic telemetry history ordering using timestamps and database record IDs
- Added database indexing to improve machine-specific telemetry queries
- Normalized historical machine health-state capitalization for consistent frontend display
- Improved database schema initialization and migration reliability
- Added automated tests for concurrent database access, transaction rollback, telemetry retrieval and schema initialization
- Added failure isolation between SQLite persistence, MQTT publishing and WebSocket broadcasting
- Ensured MQTT and WebSocket failures do not interrupt telemetry collection or simulation execution
- Preserved database persistence errors for proper failure detection
- Updated MQTT publisher to use asynchronous broker connections
- Added automatic MQTT reconnection with configurable retry delays
- Added MQTT connection-state tracking using connection and disconnection callbacks
- Added MQTT publish-result validation and connection error handling
- Improved MQTT startup and shutdown behavior with lifecycle synchronization
- Updated MQTT publisher tests to support asynchronous connection behavior
- Added mocked MQTT reliability tests for connection handling, publishing failures and repeated shutdown
- Updated live MQTT integration tests to wait for successful broker connection
- Added optional execution of live MQTT integration tests using environment configuration
- Improved WebSocket manager with thread-safe client connection management
- Added duplicate WebSocket connection prevention and disconnected-client cleanup
- Added FastAPI event-loop validation before scheduling WebSocket broadcasts
- Added asynchronous broadcast failure detection and logging
- Added graceful WebSocket connection cleanup during application shutdown
- Improved FastAPI WebSocket endpoint to handle client disconnections correctly
- Added guaranteed WebSocket cleanup using `try/finally`
- Verified shared application and WebSocket manager instances across simulation and FastAPI routes
- Improved FastAPI lifespan management for graceful application startup and shutdown
- Moved blocking application shutdown operations to a worker thread to avoid blocking the FastAPI event loop
- Added automated tests for WebSocket connection management, broadcast failures and cleanup
- Added FastAPI lifecycle integration tests for startup, shutdown and WebSocket cleanup
- Added WebSocket integration tests to verify telemetry delivery through the FastAPI endpoint
- Validated end-to-end telemetry flow across simulation, RUL prediction, SQLite, MQTT, WebSocket and React dashboard
- Verified graceful FastAPI shutdown and simulation termination
- Verified full pytest test suite

## v0.7.0

- Added predictive maintenance service based on machine health and Remaining Useful Life (RUL)
- Added maintenance classifications: NORMAL, DUE_SOON, REQUIRED and CRITICAL
- Added configurable RUL thresholds for maintenance classification
- Added maintenance severity, descriptive messages and recommended actions
- Integrated predictive maintenance assessments into SQLite persistence, MQTT publishing and WebSocket updates
- Added accelerated simulation mode using DemoConfig
- Added configurable physics timestep, simulated time per tick and degradation rate
- Enabled accelerated run-to-failure simulation
- Added automatic simulation termination when all machines reach FAILED state
- Ensured final failure-state telemetry is published before simulation termination
- Added failure-specific maintenance assessments and corrective actions
- Ensured failed machines receive CRITICAL maintenance status even when RUL prediction is unavailable
- Added dedicated machine health-state indicator to frontend dashboard
- Separated machine operational status from machine health state
- Added health-state capitalization normalization for consistent frontend display
- Updated automatic failure handling to invoke stop() instead of directly modifying machine status
- Added CNC spindle shutdown behavior to reset RPM to zero
- Fixed nonzero RPM being reported after machine failure
- Added automated tests for maintenance classifications, RUL thresholds and failure-specific assessments
- Added regression tests for spindle shutdown and accelerated simulation termination
- Validated end-to-end run-to-failure simulation, including final WebSocket telemetry delivery
- Verified full test suite

## v0.6.0

- Added RUL dataset feature engineering and lifecycle-aware train/validation/test splitting.
- Added baseline, Random Forest, and Gradient Boosting RUL model training and evaluation.
- Selected the health-assisted Random Forest model based on validation performance.
- Evaluated the final RUL model on an untouched test set.
- Achieved 2.07-hour MAE, 3.82-hour RMSE, and 0.9993 R² on the synthetic TwinForge test dataset.
- Added model persistence using Joblib for saving and loading the trained RUL model.
- Added reusable RUL predictor for inference from runtime, temperature, vibration, load, and health.
- Integrated live RUL prediction into the telemetry pipeline.
- Added predicted RUL to WebSocket and MQTT telemetry payloads.
- Added predicted RUL persistence to SQLite telemetry storage.
- Extended telemetry history retrieval with predicted RUL.
- Added SQLite migration support for the RUL prediction field.
- Integrated live predicted RUL into the React dashboard.
- Added predicted RUL metric card and RUL history trend visualization.
- Added unit tests for RUL dataset splitting, feature engineering, model training, prediction, and persistence integration.

## v0.5.0

- Added stable machine identifiers
- Added machine-specific telemetry history retrieval
- Integrated persisted telemetry history into frontend charts
- Added degradation model abstraction
- Added CNC spindle degradation model
- Linked machine health degradation to RPM, load, temperature and vibration
- Added machine health states: HEALTHY, DEGRADED, CRITICAL and FAILED
- Added automatic machine stop on failure
- Separated spindle physics from health degradation
- Integrated health degradation into normal simulation
- Added run-to-failure simulation
- Added lifecycle record generation
- Added Remaining Useful Life (RUL) label calculation
- Separated physics timestep from dataset sampling interval
- Added multi-run RUL dataset generator
- Added temperature and vibration sensors to generated lifecycle data
- Added machine-to-machine degradation and physics variability
- Added RUL dataset CSV exporter
- Added RUL dataset analysis utility
- Generated RUL Dataset v1 with 100 independent machine lifecycles
- Generated 38,083 lifecycle records with zero missing values
- Verified all generated machine lifecycles reach FAILED state with RUL = 0
- Added degradation and RUL dataset automated tests
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