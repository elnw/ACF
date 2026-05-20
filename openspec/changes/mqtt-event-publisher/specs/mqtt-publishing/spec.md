## ADDED Requirements

### Requirement: Factory pattern for event creation
The system SHALL use a factory pattern to create the event object. The event payload MUST consist exclusively of the string or number `"1"`.

#### Scenario: Event generation
- **WHEN** the script runs and needs to build the payload
- **THEN** it calls the event factory which returns an object containing `"1"`

### Requirement: Environment variable configuration
The system SHALL read MQTT connection parameters (broker URL/IP, port, topic, client ID) from environment variables.

#### Scenario: Missing environment variables
- **WHEN** the script is executed without required MQTT environment variables
- **THEN** it immediately exits with an error indicating the missing configuration

### Requirement: QoS 2 publishing
The system SHALL publish the event to the configured MQTT broker using Quality of Service (QoS) level 2 (Exactly once).

#### Scenario: Successful publish
- **WHEN** the script connects to the broker and calls publish
- **THEN** the broker acknowledges the message with the QoS 2 handshake and the script records a success

### Requirement: Exponential backoff retries
The system SHALL implement exponential backoff if the MQTT broker is not reachable or fails to acknowledge the message.

#### Scenario: Broker is temporarily unavailable
- **WHEN** the MQTT client fails to publish the message
- **THEN** the script waits for an exponentially increasing delay (e.g., 2s, 4s, 8s) up to a maximum number of attempts before failing completely
