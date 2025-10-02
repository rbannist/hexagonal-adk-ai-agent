# Marketing Creative Agent

This is an example implementation of an AI agent for the marketing domain of a supermarket retailer.  The agent is designed to generate marketing images based on text prompts, leveraging Google's Generative AI models and the Google Agent Development Kit (ADK).

The agent's capabilities are exposed via an A2A (Agent-to-Agent Protocol) compliant web server.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Running with Docker](#running-with-docker)
- [Project Structure](#project-structure)

## Features

- **Image Generation**: Generates marketing images from text descriptions - e.g. "A shopping cart full of fresh vegetables".
- **A2A Compliant**: Implements the A2A (Agent-to-Agent) protocol for standardised agent communication.
- **Tool-Using Agent**: Utilises the Google ADK to create an agent that uses a custom tool for image generation.
- **Cloud Integrated**: Stores generated images in a Google Cloud Storage bucket.
- **Containerised**: Includes a `Dockerfile` for easy deployment and scaling.

## Architecture

- **Core Logic (`marketing_image_agent`)**: Contains the agent definition using Google ADK.  The agent is instructed to use a tool (`generate_image_tool`) which calls the `imagen` model on Vertex AI to generate an image and then stores it in Google Cloud Storage.
- **Agent Executor (`agent_executor.py`)**: Acts as a bridge between the A2A server and the Google ADK agent.  The `ADKAgentExecutor` handles incoming requests, invokes the ADK runner, and manages the task lifecycle.
- **Web Framework (`__main__.py`)**: Sets-up and runs a Starlette web application using the `a2a-sdk`.  It defines the agent's public-facing `AgentCard` (its capabilities, skills, and endpoints) and routes incoming HTTP requests to the `ADKAgentExecutor`.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant A2AStarletteApplication
    participant DefaultRequestHandler
    participant ADKAgentExecutor
    participant Runner
    participant marketing_image_agent
    participant GoogleCloudStorage
    participant VertexAI

    User->>A2AStarletteApplication: HTTP Request
    A2AStarletteApplication->>DefaultRequestHandler: handle_request()
    DefaultRequestHandler->>ADKAgentExecutor: execute()
    ADKAgentExecutor->>Runner: run_async()
    Runner->>marketing_image_agent: call tool
    alt generate_marketing_image
        marketing_image_agent->>VertexAI: generate_images()
        VertexAI-->>marketing_image_agent: image_bytes
        marketing_image_agent->>GoogleCloudStorage: save_marketing_image_object()
        GoogleCloudStorage-->>marketing_image_agent: public_url, checksum
        marketing_image_agent-->>Runner: image details
    else accept_marketing_image
        marketing_image_agent->>GoogleCloudStorage: update_marketing_image_metadata()
        GoogleCloudStorage-->>marketing_image_agent: success/failure
        marketing_image_agent-->>Runner: status
    else reject_marketing_image
        marketing_image_agent->>GoogleCloudStorage: update_marketing_image_metadata()
        GoogleCloudStorage-->>marketing_image_agent: success/failure
        marketing_image_agent-->>Runner: status
    else remove_marketing_image
        marketing_image_agent->>GoogleCloudStorage: delete_marketing_image_object()
        GoogleCloudStorage-->>marketing_image_agent: success/failure
        marketing_image_agent-->>Runner: status
    else change_marketing_image_metadata
        marketing_image_agent->>GoogleCloudStorage: update_marketing_image_metadata()
        GoogleCloudStorage-->>marketing_image_agent: success/failure
        marketing_image_agent-->>Runner: status
    end
    Runner-->>ADKAgentExecutor: response
    ADKAgentExecutor->>DefaultRequestHandler: response
    DefaultRequestHandler->>A2AStarletteApplication: response
    A2AStarletteApplication-->>User: HTTP Response
```

## Getting Started

### Prerequisites

- Python 3.12+
- uv (recommended for dependency management)
- Access to a Google Cloud Platform project.
- A Google Cloud Storage bucket.
- Authenticated gcloud CLI or a service account with permissions for Vertex AI and Cloud Storage.

### Configuration

The application is configured using environment variables.  Create a `.env` file (see `.env.example`) and populate it with the following (as a minimum):

```env
# GCP Configuration
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="europe-west4" # Or your preferred Google Cloud region
GOOGLE_CLOUD_STORAGE_BUCKET="your-gcs-bucket-name"

# Agent & Model Configuration (defaults are provided in the code)
ADK_MODEL_1_NAME="gemini-2.5-flash"
GOOGLE_CLOUD_GENAI_IMAGE_MODEL_1_NAME="imagen-4.0-fast-generate-001"

# Application URL (optional)
APP_URL="http://0.0.0.0:8080"
PORT="8080"
```

### Installation

1.  Clone the repository.
2.  Install the dependencies using `uv`:

    ```bash
    uv pip install -r requirements.txt
    ```

### Running the Application

Start the server from the root directory:

```bash
gcloud auth application default-login
```

followed by

```bash
uv run python __main__.py
```

The server will be running at `http://0.0.0.0:8080` and can be tested with [A2AInspector](https://github.com/a2aproject/a2a-inspector).

## Running with Docker

You can also build and run the application using Docker.

1.  **Build the image:**

    ```bash
    docker build -t marketing-creative-agent .
    ```

2.  **Run the container:**

    First, ensure you have authenticated with gcloud to generate the necessary credentials file:

    ```bash
    gcloud auth application-default login
    ```

    Then, run the container.  The following command reads the content of your gcloud credentials file and passes it directly to the `GOOGLE_APPLICATION_CREDENTIALS` environment variable inside the container.  It also passes your `.env` file for application configuration.

```bash
docker run --rm -p 8080:8080 \
  -v "$HOME/.config/gcloud/application_default_credentials.json:/app/gcp-credentials.json:ro" \
  --env GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-credentials.json" \
  --env-file .env \
  marketing-creative-agent
```

## Project Structure

```
├── marketing_image_agent/  # Core agent logic
│   ├── agent.py            # Defines the ADK agent, tools, and GCS client
│   └── __init__.py
├── __main__.py             # Application entrypoint, sets up the A2A Starlette app
├── agent_executor.py       # Bridge between the A2A server and the ADK agent
├── Dockerfile              # For containerizing the application
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Pinned dependencies for production
└── .env.example            # Example environment variables
```