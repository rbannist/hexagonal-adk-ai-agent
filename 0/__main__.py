import asyncio
import logging

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

from config import Config
from agent_executor import ADKAgentExecutor
from marketing_image_agent.agent import agent as marketing_image_agent

config=Config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if config.ai_adk_agent_1_artifact_storage_bucket_name is not None:
    print(f"Initialising ADK Agent with Artifact Storage Bucket: {config.ai_adk_agent_1_artifact_storage_bucket_name}")


async def main():
    host = config.host
    port = int(config.port)

    agent_card = AgentCard(
        name=config.ai_adk_agent_1_name,
        description=config.service_1_description,
        version="1.0.0",
        url=config.app_url,
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
            artifact_storage_bucket_name=config.ai_adk_agent_1_artifact_storage_bucket_name,
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
