## Why

Currently, sensitive configuration values (like Wi-Fi credentials, MQTT broker details, and credentials) are hardcoded directly in the ESP32 source code (`main.cpp`). This poses a security risk when checking code into source control and makes it difficult to change configurations across different environments without modifying the main application logic. Extracting these secrets prevents accidental exposure in version control.

## What Changes

- Extract Wi-Fi credentials (`ssid`, `password`) into a new header file `secrets.h`.
- Extract MQTT credentials and configuration (`mqtt_user`, `mqtt_pass`, `mqtt_server`, `mqtt_port`, `topic_sub`) into `secrets.h`.
- Include `secrets.h` in `ESP32/src/main.cpp` and use the extracted constants.
- Add `secrets.h` to the project's `.gitignore` file to prevent committing sensitive data.

## Capabilities

### New Capabilities

- `secrets-management`: Moving hardcoded secrets into an external, git-ignored header file for improved security and configuration separation.

### Modified Capabilities

None.

## Impact

- `ESP32/src/main.cpp`: Will be modified to include `secrets.h` and remove hardcoded constants.
- `ESP32/src/secrets.h`: New file created to hold the configuration constants.
- `.gitignore`: Will be updated to exclude `secrets.h`.

## Non-goals

- Implement advanced secret management like dynamic provisioning, secure element storage, or encrypted flash storage.
