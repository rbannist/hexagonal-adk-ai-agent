# Hexagonal ADK AI Agent

This project is a starting point for building AI agents using the Agent Development Kit (ADK) and a hexagonal architecture.  It provides a basic agent that can be extended and adapted to your own needs.

## The Path to Hexagonal Architecture

This repository is structured to guide you through the process of building a sophisticated, maintainable, and scalable AI agent.  We'll start with a basic ADK agent and incrementally introduce the concepts of hexagonal architecture.

| Step | What's Being Introduced | Why It's Valuable |
| :--- | :--- | :--- |
| **0** | **The Initial ADK + A2A Agent** | This is our starting point.  The agent is designed to generate marketing images based on text prompts. |
| **1** | **The Domain Model** | We need a deterministic core to apply business logic and capture business state.  It's where we model rules of our agent's world.  Here we ensure that the agent is built around the core concepts of the problem we're trying to solve. |
| **2** | **The Application Layer** | This layer orchestrates.  It contains the use cases of our agent and is the entry point for all external interactions.  By creating a separate application layer, we decouple the core logic from the outside world. |
| **3** | **The Adapter Layer** | Adapters are the glue that connects our agent to the outside world.  They implement the interfaces defined in the application layer and interact with things like databases, APIs, and user interfaces.  This is where we see hexagonal architecture take shape. |

## Getting Started

### Prerequisites

* Python 3.12
* uv
* pip
* Virtualenv (recommended)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/hexagonal-adk-ai-agent.git](https://github.com/hexagonal-adk-ai-agent.git)
    cd hexagonal-adk-ai-agent/0
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and add your configuration details, such as API keys.

### Running the Agent

To run the agent, simply execute `uv run python __main__.py`.