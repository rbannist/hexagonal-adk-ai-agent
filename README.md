# Hexagonal ADK AI Agent

This project is a starting point for building AI agents using the Agent Development Kit (ADK) and a hexagonal architecture.  It provides a basic agent that can be extended and adapted to your own needs.

-------------------------------------------------------------------------------------------------------------

## The Path to Hexagonal Architecture

This repository is structured to guide you through the process of building a sophisticated, maintainable, and scalable AI agent.  We'll start with a basic ADK + A2A agent and incrementally introduce the concepts of hexagonal architecture.

| Step | What's Being Introduced | Why It's Valuable |
| :--- | :--- | :--- |
| **0** | **The Initial ADK + A2A Agent** | This is our starting point.  The agent is designed to deal with lifecycle of AI-generated marketing images based on text prompts. |
| **1** | **The Domain Model, Aggregate Repository, and Domain Event store** | We need a deterministic core to apply business logic and capture business state.  It's where we model rules of our agent's world and capture and store business state.  Here we ensure that the agent is built around the core concepts of the problem we're trying to solve.  This capturing of business logic and state is what will allow us to produce meaningful audit logs, enable loose-coupling of agents and system components and {micro}services, align with Event-Driven Architecture patterns, tie agent actions with business controls and metrics, etc.  |
| **2** | **The Application and Infrastructure Layers** | The Application Layer orchestrates.  It contains the use cases of our agent and is the entry point for all external interactions.  By creating a separate application layer, we decouple the core logic from the outside world.  The Infrastructure Layer and its Adapters are the glue that connects our agent to the outside world.  They implement the interfaces defined in the application layer and interact with things like databases, APIs, user interfaces, etc.  This is where we see hexagonal architecture take shape and we also introduce new  ports and adapters for additional purposes and configurations due to the flexibility afforded by the pattern - e.g. interchangeable Imagen and Gemini Flash Image adapters. |

-----------------------------------------------------------------------------------------------------------

## End-State Benefits
*   **Maintainability**: Clear separation of concerns makes the codebase easier to understand, debug, and modify.
*   **Modifiability**: Rapid and safe introduction of new features or changes due to the isolated nature of components.
*   **Modularity**: The modular design allows for independent development and deployment of components, fostering better organisation and management of the codebase.
*   **Observability**: Both the business state and logic (deterministic) and the agent's internal state and behaviour (probabilistic) are transparent, making it easier to monitor and troubleshoot.
*   **Portability**: The agent can be easily moved to different environments or cloud providers due to its decoupled architecture.
*   **Testability**: Isolated components can be tested independently, leading to more robust and reliable agents.
*   **Flexibility**: Business logic is decoupled from probablistic elements and external dependencies, making it easier to swap out infrastructure components - e.g. databases, AI models, etc. - without affecting the core functionality.
*   **Auditability**: The clear separation of concerns and well-defined interfaces make it easier to implement logging, monitoring, and auditing mechanisms, providing a transparent view of the agent's operations and decisions.
*   **Securability**: Enhanced security measures can be implemented at each layer, protecting sensitive data and intellectual property.
*   **Scalability**: The architecture supports easy integration of new technologies and services, allowing the agent to grow and adapt.
*   **Performance**: Optimised resource utilsation and faster response times due to efficient component interaction and data flow.
*   **Measurability**: The architecture facilitates the collection of metrics and data points, allowing for quantitative analysis of the agent's performance, efficiency, and impact.
*   **Configurability**:The agent's behaviour can be easily modified through external configurations without changing the code.
*   **Extensibility**: The ability to add new features or modify existing ones with minimal impact on the rest of the system.
*   **Composability**:The ability to combine and recombine smaller, independent components to create new functionalities or agents.
*   **Learnability**: The architecture is designed to be easily understood and adopted by new team members, reducing the learning curve and accelerating onboarding.
*   **Localisability**: The ability to adapt the agent to different languages, regions, and cultural contexts, ensuring a broader reach and user acceptance.
*   **Team Collaboration**: Different teams can work on different layers or adapters simultaneously with minimal conflicts.

-----------------------------------------------------------------------------------------------------------

## Getting Started

### Main Prerequisites

* Python 3.12
* uv
* pip
* Virtualenv (recommended)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rbannist/hexagonal-adk-ai-agent.git
    ```

2.  **Create and activate a virtual environment for each of the steps**
    ```bash
    cd <directory - e.g. hexagonal-adk-ai-agent/0>
    uv venv
    source .venv/bin/activate
    ```

3.  **Set up your environment variables:**
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and add your configuration details, such as API keys.

3.  **Follow the instructions in the given agent's directory/README.md:**
    - Step 0 Agent
        - [Readme](https://github.com/rbannist/hexagonal-adk-ai-agent/blob/main/0/README.md)
    - Step 1 Agent
        - [Readme](https://github.com/rbannist/hexagonal-adk-ai-agent/blob/main/1/README.md)
    - Step 2 Agent
        - [Readme](https://github.com/rbannist/hexagonal-adk-ai-agent/blob/main/2/README.md)

-----------------------------------------------------------------------------------------------------------

## Roadmap / Future Intentions

| Step | What's Being Introduced | Why It's Valuable |
| :--- | :--- | :--- |
| **3** | **Foundational Infrastructure & Governance** | This step prepares the agent for scalable, repeatable deployments and formalises our architectural principles. |
| | <ul> <li>Terraform Google Cloud resource deployment.</li> <li>Documented Quality Attributes & ADRs fed into code and deployment concerns.</li> </ul> | <ul> <li>**Terraform IaC** allows us to automatically and reliably deploy the cloud infrastructure - e.g. storage for images, container runtime, etc. -  needed to run our agent. </li> <li>**ADRs** and defined **Quality Attributes** - e.g. performance, security, reliability, observability, etc. - force us to make conscious decisions, ensuring the architecture can handle what's required of it.</li> </ul> |
| **4** | **Production-Grade Observability** | We can't fix or improve what we can't see.  This step gives us deep insight into how image generation requests are performing. |
| | <ul> <li>Structured Logging.</li> <li>End-to-End Tracing (ADK + Traditional).</li> </ul> | <ul> <li>**Tracing** lets us follow a single request from the initial prompt to the final output, pinpointing bottlenecks or errors in the process. </li> <li>**Structured Logs** provide the rich, machine-readable details at each step of the trace, answering *why* a problem occurred.</li> </ul> |
| **5** | **Core Agent Performance & Statefulness** | This focuses on making the single agent faster, smarter, and more capable of handling complex, long-running tasks. |
| | <ul> <li>Async end-to-end processing.</li> <li>Vertex AI Agent Engine (Memory & Sessions).</li> <li>ADK Artifact Storage advancements.</li> </ul> | <ul> <li>**Async processing** makes the whole agent service non-blocking, so it can start generating a complex image while remaining responsive to other users.</li> <li>**Memory & Sessions** allow the agent to remember context from a user's previous requests - e.g. "Use the same colour palette as last time", leading to more coherent and useful images. </li> <li>Advanced **Artifact Storage** improves how we manage the terabytes of generated images, drafts, and assets.</li> </ul> |
| **6** | **Advanced Multi-Agent System Architecture** | This evolves our single agent into a sophisticated system of collaborating specialist agents, enabling complex, automated marketing workflows. |
| | <ul> <li>An **Agent / A2A Registry**.</li> <li>Multi-agent patterns - i.e. CQRS, Sagas, Event Sourcing, Claim-Check, etc. </li> </ul> | <ul> <li>We can now have specialised agents. The **Registry** allows them to discover and talk to each other.</li> <li>Patterns like **Choreography Sagas** and **Event Sourcing** enable reliable, multi-step workflows - e.g. draft image -> get legal approval -> publish to social media - without a central point of failure. The **Claim-Check** pattern is used to pass large data, like high-resolution images, between them efficiently.</li> </ul> |