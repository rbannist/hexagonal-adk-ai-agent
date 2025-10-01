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


## Agent Development and Maturity Roadmap

| Step | What's Being Introduced | Why It's Valuable |
| :--- | :--- | :--- |
| **4** | **Foundational Infrastructure & Governance** | This step prepares the agent for scalable, repeatable deployments and formalises our architectural principles. |
| | <ul> <li>Terraform Google Cloud resource deployment.</li> <li>Documented Quality Attributes & ADRs fed into code and deployment concerns.</li> </ul> | <ul> <li>**Terraform IaC** allows us to automatically and reliably deploy the cloud infrastructure - e.g. storage for images, container runtime, etc. -  needed to run our agent. </li> <li>**ADRs** and defined **Quality Attributes** - e.g. performance, security, reliability, observability, etc. - force us to make conscious decisions, ensuring the architecture can handle what's required of it.</li> </ul> |
| **5** | **Production-Grade Observability** | We can't fix or improve what we can't see.  This step gives us deep insight into how image generation requests are performing. |
| | <ul> <li>Structured Logging.</li> <li>End-to-End Tracing (ADK + Traditional).</li> </ul> | <ul> <li>**Tracing** lets us follow a single request from the initial prompt to the final output, pinpointing bottlenecks or errors in the process. </li> <li>**Structured Logs** provide the rich, machine-readable details at each step of the trace, answering *why* a problem occurred.</li> </ul> |
| **6** | **Core Agent Performance & Statefulness** | This focuses on making the single agent faster, smarter, and more capable of handling complex, long-running tasks. |
| | <ul> <li>Async end-to-end processing.</li> <li>Vertex AI Agent Engine (Memory & Sessions).</li> <li>ADK Artifact Storage advancements.</li> </ul> | <ul> <li>**Async processing** makes the whole agent service non-blocking, so it can start generating a complex image while remaining responsive to other users.</li> <li>**Memory & Sessions** allow the agent to remember context from a user's previous requests - e.g. "Use the same colour palette as last time", leading to more coherent and useful images. </li> <li>Advanced **Artifact Storage** improves how we manage the terabytes of generated images, drafts, and assets.</li> </ul> |
| **7** | **Advanced Multi-Agent System Architecture** | This evolves our single agent into a sophisticated system of collaborating specialist agents, enabling complex, automated marketing workflows. |
| | <ul> <li>An **Agent / A2A Registry**.</li> <li>Multi-agent patterns - i.e. CQRS, Sagas, Event Sourcing, Claim-Check, etc. </li> </ul> | <ul> <li>We can now have specialised agents. The **Registry** allows them to discover and talk to each other.</li> <li>Patterns like **Choreography Sagas** and **Event Sourcing** enable reliable, multi-step workflows - e.g. draft image -> get legal approval -> publish to social media - without a central point of failure. The **Claim-Check** pattern is used to pass large data, like high-resolution images, between them efficiently.</li> </ul> |