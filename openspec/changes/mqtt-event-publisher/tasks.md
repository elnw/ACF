## 1. Project Skeleton and Event Generation

- [x] 1.1 Create `Producers/requirements.txt` with `paho-mqtt`, `brevo-python`, and `python-dotenv`
- [x] 1.2 Create `Producers/.env.example` documenting MQTT and Brevo environment variables
- [x] 1.3 Implement `Producers/event_factory.py` containing an `EventFactory` class that returns the `"1"` payload

## 2. Email Notification Logic

- [x] 2.1 Create `Producers/email_template.html` with basic HTML for the notification content
- [x] 2.2 Implement `Producers/email_notifier.py` using the Brevo SDK, reading from the template file, configured via environment variables

## 3. MQTT Publisher Implementation

- [x] 3.1 Implement `Producers/mqtt_publisher.py` incorporating MQTT client setup driven by environment variables
- [x] 3.2 Add QoS 2 publishing support to `Producers/mqtt_publisher.py`
- [x] 3.3 Add an exponential backoff retry loop (wrapping the publish call) in `Producers/mqtt_publisher.py`

## 4. Orchestration and Packaging

- [x] 4.1 Create `Producers/main.py` to coordinate the event factory, MQTT publish logic, and ensure the email notifier runs using a `try...except...finally` pattern
- [x] 4.2 Create `Producers/Dockerfile` using a multistage approach (stage 1: dependencies, stage 2: script and environment variable mapping)
