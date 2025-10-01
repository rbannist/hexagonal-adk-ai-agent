# Marketing Creative Agent

This is an example implementation of an AI agent for the marketing domain of a supermarket retailer.  The agent is designed to generate marketing images based on text prompts, leveraging Google's Generative AI models and the Google Agent Development Kit (ADK).  This AI agent has an Application layer that contains the use cases of our agent and is the entry point for all external interactions.

The agent's capabilities are exposed via an A2A (Agent-to-Agent Protocol) compliant web server.

## Table of Contents

  - [Features](https://www.google.com/search?q=%23features)
  - [Architecture](https://www.google.com/search?q=%23architecture)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Configuration](https://www.google.com/search?q=%23configuration)
      - [Installation](https://www.google.com/search?q=%23installation)
      - [Running the Application](https://www.google.com/search?q=%23running-the-application)
  - [Running with Docker](https://www.google.com/search?q=%23running-with-docker)
  - [Project Structure](https://www.google.com/search?q=%23project-structure)

-----

## Features

  - **Image Generation**: Generates marketing images from text descriptions - e.g. "A shopping cart full of fresh vegetables".
  - **A2A Compliant**: Implements the A2A (Agent-to-Agent) protocol for standardised agent communication.
  - **Tool-Using Agent**: Utilises the Google ADK to create an agent that uses a custom tool for image generation.
  - **Cloud Integrated**: Stores generated images in a Google Cloud Storage bucket.
  - **Containerised**: Includes a `Dockerfile` for easy deployment and scaling.
  - **Hexagonal Architecture**: The agent is now built using a Hexagonal (Ports and Adapters) Architecture, which decouples the core logic and deterministic interactions from the agent and any external services.
  - **Application Layer**: Contains the core business logic of the agent service, including services for handling commands and domain events.
  - **Infrastructure Layer**: Provides concrete implementations of the ports defined in the application layer, allowing for easy integration with external services like Google Cloud Storage and Vertex AI.
  - **Integration Event Bus**: An integration event bus is implemented to allow for communication between different parts of the system and with external systems.

-----

## Architecture

This agent is built using a **Hexagonal Architecture** (also known as Ports and Adapters).  This architectural style isolates the core business logic of the application from the services it interacts with.  This is achieved by defining "ports" (interfaces) in the application layer, which are then implemented by "adapters" in the infrastructure layer.

### Application Layer

The **Application Layer** is the heart of the agent.  It contains the core business logic, which is implemented as a set of services.  These services are responsible for handling commands, executing business logic, and publishing events.  The application layer is completely independent of the infrastructure layer, which means that the business logic can be tested in isolation from external services.

The Application Layer includes:

  - **Ports**: Abstract interfaces that define how the application layer interacts with the outside world.
  - **Services**: Implement the core use cases of the agent.
  - **Command Handlers**: Responsible for handling incoming commands and delegating to the appropriate service.
  - **Domain Event Handlers**: Responsible for handling domain events that are raised by the services.

### Infrastructure Layer

The **Infrastructure Layer** provides the concrete implementations of the ports defined in the application layer.  This is where the agent interacts with external services such as databases, messaging systems, and generative AI models.

The Infrastructure Layer includes:

  - **Adapters**: Concrete implementations of the ports.  For example, there are adapters for Google Cloud Storage, Google Cloud Vertex AI, and an in-memory command and domain event dispatchers.
  - **Dependency Injection**: The agent uses dependency injection to wire-up the application and infrastructure layers.  This makes it easy to swap out different implementations of the ports, which is useful for testing and for adapting the agent to different environments.
  - **Configuration Management**: The agent's configuration is managed using a combination of environment variables and a `config.yaml` file.

### Integration Event Bus

The agent uses an **Integration Event Bus** to publish and subscribe to integration events.  This allows the agent to communicate with other systems / bounded contexts / agents / {micro}services in a decoupled way.  The event bus is implemented using Google Cloud Pub/Sub / Eventarc.

-----

## Getting Started

### Prerequisites

  - Python 3.12+
  - uv: Recommended for dependency management.
  - Google Cloud Platform Project: At least one Google Cloud project is required to house all the necessary cloud resources.
  - Google Cloud Storage Buckets:
      - A bucket for storing ADK (Agent Development Kit) artifacts (optional).
      - A separate bucket for storing the generated marketing image objects.
  - Google Cloud Firestore: A Firestore database is required for the marketing image aggregate repository and domain event store (batch written in this example).
  - Google Cloud Vertex AI: You'll need to have the Vertex AI API enabled in your Google Cloud project to access the generative AI models.
  - Google Cloud Pub/Sub: You'll need to have the Pub/Sub API enabled in your Google Cloud project to use the integration event bus and a topic available to push integration events to (and a push or pull subscription to receive them).
  - Authentication: You'll need an authenticated gcloud CLI or a service account with the appropriate permissions for Vertex AI, Cloud Storage, Firestore, Cloud Pub/Sub, Eventarc, etc.

### Configuration

The application is configured using environment variables.  Create a `.env` file (see `.env.example`) and populate it.

### Installation

1.  Clone the repository.

2.  Install the dependencies using `uv`:

    ```bash
    uv pip install -r requirements.txt
    ```

### Running the Application

Start the server from the root directory:

```bash
gcloud auth application-default login
```

followed by

```bash
uv run python __main__.py
```

The server will be running at `http://0.0.0.0:8080` and can be tested with [A2AInspector](https://github.com/a2aproject/a2a-inspector).

-----

## Running with Docker

You can also build and run the application using Docker.

1.  **Build the image:**

    ```bash
    docker build -t marketing-creative-agent .
    ```

2.  **Run the container:**

    First, ensure you have authenticated with gcloud to genrate the necessary credentials file:

    ```bash
    gcloud auth application-default login
    ```

    Then, run the container. The following command reads th content of your gcloud credentials file and passes it directly to the `GOOGLE_APPLICATION_CREDENTIALS` environment variable inside the container. It also passes your `.env` file for application configuration.

<!-- end list -->

```bash
docker run --rm -p 8080:8080 \
  -v "$HOME/.config/gcloud/application_default_credentials.json:/app/gcp-credentials.json:ro" \
  --env GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-credentials.json" \
  --env-file .env \
  marketing-creative-agent
```

-----

## Project Structure

```
├── marketing_image_agent/
│   ├── application/
│   │   ├── command_handlers/
│   │   ├── command_objects/
│   │   ├── domain_event_handlers/
│   │   ├── factories/
│   │   ├── inbound_integration_event_handlers/
│   │   ├── outbound_integration_events/
│   │   ├── ports/
│   │   └── services/
│   ├── domain/
│   │   ├── entities/
│   │   ├── events/
│   │   ├── factories/
│   │   ├── services/
│   │   └── value_objects/
│   ├── infrastructure/
│   │   └── adapters/
│   │   │   ├── dispatching/
│   │   │   ├── generative_ai/
│   │   │   ├── messaging/
│   │   │   ├── object_storage/
│   │   │   └── repository/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── __main__.py             # Application entrypoint, sets up the A2A Starlette app
├── agent_executor.py       # Bridge between the A2A server and the ADK agent
├── config.py               # Configuration loading
├── config.yaml             # Application configuration
├── Dockerfile              # For containerising the application
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Pinned dependencies for production
└── .env.example            # Example environment variables
```