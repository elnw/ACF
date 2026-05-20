## ADDED Requirements

### Requirement: Multistage Docker build
The system SHALL use a multistage Dockerfile to containerise the Python script.

#### Scenario: Building the Docker image
- **WHEN** a user runs `docker build`
- **THEN** the process creates an intermediate image for installing dependencies, and a final lightweight runtime image

### Requirement: Stage 1 dependency installation
The first stage of the Dockerfile SHALL install all required dependencies (e.g., `paho-mqtt`, `brevo-python`) listed in `requirements.txt`.

#### Scenario: Resolving dependencies
- **WHEN** the first stage executes
- **THEN** `pip install` downloads and installs the required packages into the intermediate container

### Requirement: Stage 2 runtime configuration
The second stage of the Dockerfile SHALL copy the installed dependencies and source code, and define the necessary environment variable placeholders using the `ENV` instruction.

#### Scenario: Running the container
- **WHEN** a user runs `docker run` on the built image
- **THEN** the container executes the main Python script with the environment variables properly exposed and ready to be overridden at runtime
