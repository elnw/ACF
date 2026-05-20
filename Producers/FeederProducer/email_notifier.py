import os
import sys
import datetime
from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)

def send_notification(success: bool, details: str) -> None:
    """
    Sends an email notification via Brevo SDK communicating the execution result.
    This function fails gracefully to avoid masking primary outcomes.
    """
    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("EMAIL_SENDER_EMAIL")
    sender_name = os.getenv("EMAIL_SENDER_NAME", "IoT Publisher")
    recipient_email = os.getenv("EMAIL_RECIPIENT_EMAIL")
    recipient_name = os.getenv("EMAIL_RECIPIENT_NAME", "System Administrator")
    subject = os.getenv("EMAIL_SUBJECT", "IoT Event Publish Execution Result")

    # Gracefully handle missing required environment variables for email
    if not api_key:
        print("Warning: BREVO_API_KEY environment variable is not set. Email notification skipped.", file=sys.stderr)
        return

    if not sender_email or not recipient_email:
        print("Warning: EMAIL_SENDER_EMAIL or EMAIL_RECIPIENT_EMAIL environment variable is not set. Email notification skipped.", file=sys.stderr)
        return

    try:
        # Load the external HTML template
        template_path = os.path.join(os.path.dirname(__file__), "email_template.html")
        if not os.path.exists(template_path):
            print(f"Warning: Email template not found at {template_path}. Email notification skipped.", file=sys.stderr)
            return

        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Prepare replacement variables
        status = "SUCCESS" if success else "FAILURE"
        status_class = "status-success" if success else "status-failure"
        status_color = "#166534" if success else "#991b1b"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        broker_topic = os.getenv("MQTT_TOPIC", "iot/events")

        # Replace placeholders in template
        html_content = html_content.replace("{{status}}", status)
        html_content = html_content.replace("{{status_class}}", status_class)
        html_content = html_content.replace("{{status_color}}", status_color)
        html_content = html_content.replace("{{timestamp}}", timestamp)
        html_content = html_content.replace("{{broker_host}}", broker_host)
        html_content = html_content.replace("{{broker_topic}}", broker_topic)
        html_content = html_content.replace("{{details}}", details)

        # Initialize the Brevo client with the API key
        client = Brevo(api_key=api_key)

        # Send the transactional email
        print(f"Attempting to send email notification (Status: {status})...")
        result = client.transactional_emails.send_transac_email(
            subject=subject,
            html_content=html_content,
            sender=SendTransacEmailRequestSender(
                name=sender_name,
                email=sender_email
            ),
            to=[
                SendTransacEmailRequestToItem(
                    name=recipient_name,
                    email=recipient_email
                )
            ]
        )
        print(f"Email notification successfully sent. Message ID: {result.message_id}")

    except Exception as e:
        print(f"Error occurred while sending email notification via Brevo: {e}", file=sys.stderr)
