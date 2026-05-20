import sys
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv(override=True)

from event_factory import EventFactory
from mqtt_publisher import publish_event
from email_notifier import send_notification

def main():
    success = False
    details = ""
    
    print("Starting IoT Event Publisher execution...")

    try:
        # Create event payload using the Factory Pattern
        payload = EventFactory.create_event()
        
        # Publish event using QoS 2 and exponential backoff
        details = publish_event(payload)
        success = True
        print("IoT Event Publisher completed successfully.")
        
    except Exception as e:
        success = False
        details = f"Execution failed during execution.\nError detail:\n{e}"
        print(f"Execution Error: {e}", file=sys.stderr)
        
    finally:
        # Ensure email notification is sent no matter what happens to MQTT or other logic
        try:
            send_notification(success, details)
        except Exception as email_err:
            print(f"Fatal error trying to dispatch notification handler: {email_err}", file=sys.stderr)

    # Exit with appropriate code
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
