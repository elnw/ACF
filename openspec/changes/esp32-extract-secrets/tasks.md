## 1. Extract Secrets

- [x] 1.1 Create `ESP32/src/secrets.h` with definitions for Wi-Fi (`ssid`, `password`) and MQTT credentials/settings (`mqtt_server`, `mqtt_port`, `mqtt_user`, `mqtt_pass`, `topic_sub`)
- [x] 1.2 Modify `ESP32/src/main.cpp` to `#include "secrets.h"` and remove the hardcoded string constants, using the variables from `secrets.h` instead

## 2. Configure Version Control

- [x] 2.1 Add `ESP32/src/secrets.h` to the `.gitignore` file (create it if it doesn't exist) to prevent committing secrets to the repository
