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

from dotenv import load_dotenv
from starlette.applications import Starlette

from agent_executor import ADKAgentExecutor
from marketing_image_agent.agent import agent as marketing_image_agent

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))

    agent_card = AgentCard(
        name=marketing_image_agent.name,
        description=marketing_image_agent.description,
        version="1.0.0",
        url=os.environ.get("APP_URL", f"http://{host}:{port}"),
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
                ],
            )
        ],
    )

    task_store = InMemoryTaskStore()

    request_handler = DefaultRequestHandler(
        agent_executor=ADKAgentExecutor(
            agent=marketing_image_agent,
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

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
