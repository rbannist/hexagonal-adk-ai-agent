import asyncio
import logging
import os

import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from starlette.applications import Starlette

from config import Container
from agent_executor import ADKAgentExecutor
from marketing_image_agent.agent import create_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

container = Container()

# Construct the absolute path to the config.yaml file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.yaml')

# Load configuration
container.config.from_yaml(config_path, required=True)

artifact_storage_type = container.config.genai.adk.agent_1.artifact_storage_type()
if artifact_storage_type == "gcs":
    if container.config.genai.adk.agent_1.artifact_storage_gcs_bucket_name() is not None:
       gcs_artifact_storage_bucket = container.config.genai.adk.agent_1.artifact_storage_gcs_bucket_name()
       print(f"Initialising ADK Agent with with {artifact_storage_type} Artifact Storage and Bucket: {gcs_artifact_storage_bucket}")
elif artifact_storage_type == "in_memory":
    print(f"Initialising ADK Agent with {artifact_storage_type} Artifact Storage")
else:
    raise ValueError

marketing_image_agent = create_agent(container)


async def main():
    host = container.config.service.host()
    port = int(container.config.service.port())

    agent_card = AgentCard(
        name=marketing_image_agent.name,
        description=marketing_image_agent.description,
        version="1.0.0",
        url=container.config.service.app_url(),
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="generate_marketing_image",
                name="Generate Marketing Image",
                description="Generates a marketing image based on a text prompt.",
                tags=["image", "generate", "marketing"],
                examples=[
                    "A shopping cart full of fresh vegetables.",
                    "Two pineapples in a supermarket frozen aisle.",
                    "Generate me an image of 3 happy beetroots",
                ],
            ),
            AgentSkill(
                id="accept_marketing_image",
                name="Accept Marketing Image",
                description="Marks a marketing image as accepted, using its ID.",
                tags=["image", "accept", "marketing"],
                examples=[
                    "Accept image with ID 123e4567-e89b-12d3-a456-426614174000",
                ],
            ),
            AgentSkill(
                id="reject_marketing_image",
                name="Reject Marketing Image",
                description="Marks a marketing image as rejected, using its ID.",
                tags=["image", "reject", "marketing"],
                examples=[
                    "Reject image with ID 123e4567-e89b-12d3-a456-426614174000",
                ],
            ),
            AgentSkill(
                id="remove_marketing_image",
                name="Remove Marketing Image",
                description="Marks a marketing image as removed, using its ID.",
                tags=["image", "remove", "delete", "marketing"],
                examples=[
                    "Remove image with ID 123e4567-e89b-12d3-a456-426614174000",
                ],
            ),
            AgentSkill(
                id="change_marketing_image_metadata",
                name="Change Marketing Image Metadata",
                description="Changes the description and keywords for a marketing image, using its ID.",
                tags=["image", "edit", "metadata", "marketing"],
                examples=[
                    "Update image 123e4567-e89b-12d3-a456-426614174000 with description 'A better description' and keywords 'new, keywords'",
                    "Update the record of image 123e4567-e89b-12d3-a456-426614174000 to have its actual dimensions of 512*512'",
                ],
            )
        ],
    )

    task_store = InMemoryTaskStore()

    request_handler = DefaultRequestHandler(
        agent_executor=ADKAgentExecutor(
            agent=marketing_image_agent,
            artifact_storage_bucket_name=container.config.genai.adk.agent_1.artifact_storage_gcs_bucket_name(),
        ),
        task_store=task_store,
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    routes = a2a_app.routes()
    app = Starlette(
        routes=routes,
        middleware=[],
    )

    server_config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(server_config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())