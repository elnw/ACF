# Stage 1: Build dependencies
FROM --platform=linux/arm64/v8 python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies if any native compilation is needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies to a specific target prefix
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final runtime container
FROM --platform=linux/arm64/v8 python:3.12-slim AS runner

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy application source files
COPY event_factory.py .
COPY mqtt_publisher.py .
COPY email_notifier.py .
COPY email_template.html .
COPY main.py .

# Define required environment variable placeholders
ENV MQTT_BROKER_HOST=localhost
ENV MQTT_BROKER_PORT=1883
ENV MQTT_TOPIC=iot/events
ENV MQTT_CLIENT_ID=iot_event_publisher
ENV BREVO_API_KEY=""
ENV EMAIL_SENDER_NAME="IoT Publisher"
ENV EMAIL_SENDER_EMAIL=""
ENV EMAIL_RECIPIENT_NAME="System Administrator"
ENV EMAIL_RECIPIENT_EMAIL=""
ENV EMAIL_SUBJECT="IoT Event Publish Execution Result"

# Run the python script
CMD ["python", "main.py"]
