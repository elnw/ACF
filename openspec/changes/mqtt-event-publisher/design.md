## Context

The ACF platform follows a publisher-subscriber architecture where Python scripts in the `Producers/` folder publish events to a Mosquitto MQTT broker. Currently, the folder is empty — there is no producer implementation. This change introduces the first producer: a single-run script that publishes a signal event (`"1"`) to the broker and sends an email report of the outcome via Brevo.

The script will be containerised with a multistage Dockerfile so it can be deployed consistently across environments (local dev, CI, edge servers).

## Goals / Non-Goals

**Goals:**
- Deliver a production-ready, single-invocation MQTT publisher with guaranteed delivery (QoS 2).
- Resilient connectivity via exponential backoff retries.
- Observable execution via Brevo email notifications after every run.
- Reproducible builds via a multistage Dockerfile.

**Non-Goals:**
- Long-running daemon or cron scheduling (orchestration is external).
- Broker provisioning or TLS certificate management.
- Consumer-side logic.

## Decisions

### 1. MQTT client library — `paho-mqtt`
**Choice:** `paho-mqtt` v2.x (callback API v2).
**Alternatives considered:**
- `gmqtt` — async-first, but adds unnecessary complexity for a single-publish script.
- `hbmqtt` — unmaintained.
**Rationale:** `paho-mqtt` is the de-facto standard Python MQTT client, widely supported, synchronous by default, and supports QoS 2 out of the box.

### 2. Event creation — Factory pattern
**Choice:** A dedicated `EventFactory` class with a static `create_event()` method that returns a standardised event dict/object with the payload `"1"`.
**Rationale:** The user explicitly requires the factory pattern. This keeps event construction separate from publishing, making it easy to extend payload formats later without touching the publisher.

### 3. Retry strategy — Exponential backoff
**Choice:** Custom retry loop with exponential backoff (base 2 s, max ~60 s, max 5 attempts). The retry wraps the `publish()` + `wait_for_publish()` call.
**Alternatives considered:**
- `tenacity` library — more flexible, but adds a dependency for a simple loop.
**Rationale:** A lightweight hand-rolled loop avoids an extra dependency and keeps the logic transparent. The backoff formula: `delay = min(base * 2^attempt, max_delay)`.

### 4. Email notification — Brevo SDK (`brevo-python`)
**Choice:** Use the official Brevo Python SDK to send a transactional email with HTML content loaded from a template file (`email_template.html`).
**Rationale:** Direct SDK usage is simpler than the REST API. The template is externalised so non-developers can edit the email content.

### 5. Configuration — Environment variables
**Choice:** All configuration via env vars, loaded with `os.environ`. A `.env.example` file documents required variables. `python-dotenv` is an optional dev convenience (not required in Docker).
**Variables:**
| Variable | Purpose |
|---|---|
| `MQTT_BROKER_HOST` | Mosquitto broker hostname/IP |
| `MQTT_BROKER_PORT` | Broker port (default 1883) |
| `MQTT_TOPIC` | Topic to publish to |
| `MQTT_CLIENT_ID` | Client identifier |
| `BREVO_API_KEY` | Brevo transactional API key |
| `EMAIL_SENDER_NAME` | Sender display name |
| `EMAIL_SENDER_EMAIL` | Sender email address |
| `EMAIL_RECIPIENT_NAME` | Recipient display name |
| `EMAIL_RECIPIENT_EMAIL` | Recipient email address |
| `EMAIL_SUBJECT` | Email subject line |

### 6. Dockerfile — Multistage build
**Choice:** Two stages:
1. **Builder** (`python:3.12-slim`): copy `requirements.txt`, run `pip install --no-cache-dir`.
2. **Runtime** (`python:3.12-slim`): copy installed packages from builder, copy source, declare `ENV` placeholders, set `CMD`.
**Rationale:** Keeps the final image small and avoids shipping build tooling. Environment variables are declared (not hardcoded) in stage 2 so they can be injected at `docker run` time.

### 7. Project file layout

```
Producers/
├── main.py               # Entry point
├── event_factory.py      # EventFactory class
├── mqtt_publisher.py     # MQTT connection + publish with backoff
├── email_notifier.py     # Brevo email logic
├── email_template.html   # HTML email template
├── requirements.txt      # paho-mqtt, sib-api-v3-sdk, python-dotenv
├── Dockerfile            # Multistage build
└── .env.example          # Documented env var template
```

## Risks / Trade-offs

- **Broker unavailable after all retries** → The script exits with a non-zero code and the Brevo email reports the failure. Orchestration layer is responsible for re-triggering.
- **Brevo API failure** → Logged to stderr; does not affect MQTT publishing result. A `try/except` wraps the email call so it never masks the primary outcome.
- **QoS 2 latency** → QoS 2 requires a four-step handshake which adds latency. Acceptable for a single-publish, non-realtime script.
