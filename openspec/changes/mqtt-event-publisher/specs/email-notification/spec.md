## ADDED Requirements

### Requirement: Send email notification via Brevo SDK
The system SHALL use the official Brevo SDK to send an email communicating the final result of the script's execution (success or failure).

#### Scenario: Execution succeeds
- **WHEN** the MQTT message is successfully published
- **THEN** an email is sent stating that the execution was successful

#### Scenario: Execution fails
- **WHEN** the MQTT message fails to publish after all retries
- **THEN** an email is sent stating that the execution failed, without stopping the script from exiting gracefully

### Requirement: Unconditional notification execution
The system SHALL attempt to send the email notification regardless of what happens in the MQTT publishing logic. The email logic MUST be placed after a `try...except` block or in a `finally` block to guarantee execution.

#### Scenario: Unhandled exception in main logic
- **WHEN** an unexpected exception occurs during the MQTT connection phase
- **THEN** the email notification logic still executes to report the failure

### Requirement: External HTML template
The system SHALL read the email body content from a separate HTML template file, rather than hardcoding it into the Python script.

#### Scenario: Loading email template
- **WHEN** the email logic prepares the message body
- **THEN** it reads the contents of the local HTML template file and uses it for the email payload

### Requirement: Notification environment variables
The system SHALL read email configuration parameters (Brevo API key, sender email, recipient email) from environment variables.

#### Scenario: Missing Brevo API key
- **WHEN** the Brevo API key is not provided
- **THEN** the email sending logic fails gracefully, logging an error but not crashing the script execution
