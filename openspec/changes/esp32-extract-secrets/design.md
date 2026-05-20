## Context

Currently, the ESP32 source code (`main.cpp`) contains hardcoded strings for Wi-Fi and MQTT configurations. This means that anytime these credentials or broker IP addresses change, the `main.cpp` must be modified. Additionally, checking these credentials into source control is a security risk. By extracting these into a separate, git-ignored header file, we maintain a cleaner separation of configuration and logic while keeping secrets secure from public repositories.

## Goals / Non-Goals

**Goals:**
- Separate all hardcoded credentials and network configuration parameters into a distinct configuration file.
- Prevent this configuration file from being checked into version control.
- Ensure `main.cpp` successfully compiles and runs using the externalized definitions.

**Non-Goals:**
- Implement dynamic Wi-Fi provisioning (e.g., using WiFiManager).
- Store credentials in persistent flash memory (SPIFFS/LittleFS) or EEPROM.
- Introduce encryption for the stored secrets.

## Decisions

- **Use of a C++ Header File (`secrets.h`)**: This is the standard, simplest approach for C++ Arduino/ESP32 projects to handle external configurations without needing complex build scripts or environment variable injection at compile time.
- **Git Ignore**: We will add `ESP32/src/secrets.h` to the `.gitignore` file to prevent it from being committed.

## Risks / Trade-offs

- **Risk**: Other developers cloning the repository will not be able to build the code immediately because `secrets.h` will be missing.
  - **Mitigation**: The documentation or README should eventually mention creating this file, but for the scope of this change, we accept that manual creation of `secrets.h` is required for a successful build.
