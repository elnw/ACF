import os
import sys
import time
import threading
import paho.mqtt.client as mqtt

def publish_event(payload: str) -> str:
    """
    Connects to the Mosquitto broker, publishes the payload using QoS 2,
    and retries with exponential backoff if the broker is not reachable or not receiving the event.
    Returns a multiline string log of the execution details.
    """
    host = os.getenv("MQTT_BROKER_HOST")
    port_str = os.getenv("MQTT_BROKER_PORT", "1883")
    topic = os.getenv("MQTT_TOPIC")
    client_id = os.getenv("MQTT_CLIENT_ID", "iot_event_publisher")
    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")

    if not host or not topic:
        raise ValueError("Missing required MQTT environment variables: MQTT_BROKER_HOST and MQTT_TOPIC must be set.")

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid MQTT_BROKER_PORT: {port_str}. Must be an integer.")

    max_attempts = 5
    base_delay = 2.0
    max_delay = 60.0
    
    details_log = []

    for attempt in range(1, max_attempts + 1):
        client = None
        try:
            log_msg = f"Attempt {attempt}/{max_attempts}: Connecting to MQTT broker at {host}:{port}..."
            print(log_msg)
            details_log.append(log_msg)

            # Initialize client with Callback API version 2
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            client.username_pw_set(username, password)
            
            # Setup a callback variable to verify acknowledgement
            published_successfully = False
            
            def on_publish(client, userdata, mid, reason_code, properties):
                nonlocal published_successfully
                published_successfully = True
                print(f"Callback received: mid={mid}, reason_code={reason_code}")

            client.on_publish = on_publish

            # Threading event to signal connection readiness
            connected_event = threading.Event()

            def on_connect(client, userdata, flags, reason_code, properties):
                if reason_code == 0:
                    print("MQTT client connected successfully.")
                    connected_event.set()
                else:
                    print(f"MQTT connection failed: reason_code={reason_code}", file=sys.stderr)

            client.on_connect = on_connect

            # Connect to broker
            client.connect(host, port, keepalive=60)
            
            # Start background thread to handle packets and callbacks
            client.loop_start()

            # Wait for broker CONNACK before publishing
            if not connected_event.wait(timeout=10.0):
                raise RuntimeError("Timed out waiting for MQTT broker CONNACK.")
            
            log_msg = f"Publishing event '{payload}' to topic '{topic}' with QoS 2..."
            print(log_msg)
            details_log.append(log_msg)
            
            publish_result = client.publish(topic, payload, qos=2)
            
            # Wait for publish to be acknowledged (10 seconds timeout)
            publish_result.wait_for_publish(timeout=10.0)
            
            if publish_result.is_published() or published_successfully:
                success_msg = f"Success: Event '{payload}' published to '{topic}' and acknowledged by the broker."
                print(success_msg)
                details_log.append(success_msg)
                
                # Cleanup client cleanly
                client.loop_stop()
                client.disconnect()
                return "\n".join(details_log)
            else:
                raise RuntimeError("Publish call succeeded but message was not acknowledged within the timeout.")

        except Exception as e:
            error_msg = f"Error during attempt {attempt}: {e}"
            print(error_msg, file=sys.stderr)
            details_log.append(error_msg)
            
            # Ensure client is stopped and disconnected on failure
            if client:
                try:
                    client.loop_stop()
                    client.disconnect()
                except Exception:
                    pass
            
            # Apply exponential backoff delay
            if attempt < max_attempts:
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                delay_msg = f"Retrying in {delay:.1f} seconds..."
                print(delay_msg)
                details_log.append(delay_msg)
                time.sleep(delay)

    raise RuntimeError(f"Failed to publish event after {max_attempts} attempts.")
