## Why

The IoT platform currently lacks a reliable mechanism for publishing events to the MQTT broker from a Python producer. We need a self-contained script that publishes a signal event ("1") to a Mosquitto broker each time it runs, with resilience features (exponential backoff) and observability (email notification of execution results via Brevo). This script will be containerised for deployment consistency across environments.

## What Changes

- Add a new Python producer script that connects to a Mosquitto MQTT broker, publishes a QoS 2 event containing the payload `"1"`, and retries with exponential backoff on failure.
- Introduce a factory pattern for event creation, keeping event construction decoupled from publishing logic.
- Read all connection and credential configuration from environment variables (broker URL, port, Brevo API key, email addresses, etc.).
- Integrate the Brevo SDK to send an execution-result email after every run, using an HTML template loaded from a separate file.
- Add a multistage Dockerfile: stage 1 installs dependencies, stage 2 copies source and injects environment variables at runtime.

## Non-goals

- Subscribing to or consuming MQTT messages (that belongs in the Consumers folder).
- Managing the Mosquitto broker itself (infrastructure concern).
- Implementing a long-running daemon or scheduled loop — the script runs once per invocation.
- Building a web UI or REST API around the publisher.

## Capabilities

### New Capabilities
- `mqtt-publishing`: Connecting to a Mosquitto broker and publishing a QoS 2 event with exponential backoff retry logic.
- `email-notification`: Sending an execution-result email via the Brevo SDK using an external HTML template.
- `container-packaging`: Multistage Dockerfile for dependency installation and runtime configuration.

### Modified Capabilities
_(none — no existing specs)_

## Impact

- **New files** in `Producers/`: Python script, event factory module, email template file, requirements file, Dockerfile, and `.env.example`.
- **Dependencies**: `paho-mqtt` (MQTT client), `brevo-python` (Brevo email SDK), `python-dotenv` (env loading during local dev).
- **Infrastructure**: Requires a running Mosquitto broker and valid Brevo API credentials at runtime.
