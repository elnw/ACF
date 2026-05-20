## ADDED Requirements

### Requirement: Externalized Configuration
The system SHALL use an external header file `secrets.h` to store and read Wi-Fi credentials and MQTT broker details rather than hardcoding them in the main application logic.

#### Scenario: Compiling with secrets
- **WHEN** the `secrets.h` file is present in the `ESP32/src` directory with all required credential variables defined
- **THEN** the firmware SHALL compile successfully and use those values at runtime for network and MQTT connections

### Requirement: Exclude Secrets from Version Control
The system SHALL NOT commit the `secrets.h` file to the version control repository.

#### Scenario: Version control exclusion
- **WHEN** a developer attempts to stage or commit changes in the repository
- **THEN** Git SHALL ignore the `secrets.h` file according to the configured `.gitignore` rules
