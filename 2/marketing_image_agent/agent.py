import os
from google.adk.agents import Agent

from config import Container
from marketing_image_agent.tools import MarketingImageGenerator as MarketingImageGeneratorTool


def generate_image_tool(prompt: str) -> dict:
    """Generates an image using a tool that generates an image, stores it in object storage, commits an aggregate to a repository, and then returns information related to the image - i.e. url, metadata, etc.

    Returns:
        A dictionary containing the result of the image generation process.
    """
    response = marketing_image_generator_tool.generate_image(prompt)
    return response

def accept_image_tool(image_id: str) -> dict:
    return {"feature":"to_be_implemented", "image_id": image_id}

def reject_image_tool(image_id: str) -> dict:
    return {"feature":"to_be_implemented", "image_id": image_id}

def remove_image_tool(image_id: str) -> dict:
    return {"feature":"to_be_implemented", "image_id": image_id}

def change_image_metadata_tool(image_id: str, new_description: str, new_keywords: list[str]) -> dict:
    return {"feature":"to_be_implemented", "image_id": image_id}


marketing_image_generator_tool: MarketingImageGeneratorTool


def create_agent(container: Container) -> Agent:
    agent = Agent(
        name=container.config.genai.adk.agent_1.name(),
        model=container.config.genai.adk.model_1.name(),
        description=container.config.genai.adk.agent_1.description(),
        instruction=container.config.genai.adk.agent_1.instruction(),
        tools=[generate_image_tool, accept_image_tool, reject_image_tool, remove_image_tool, change_image_metadata_tool],
    )
    global marketing_image_generator_tool
    marketing_image_generator_tool = MarketingImageGeneratorTool(container)

    return agent

# The following is added to support the `adk web` command.
# It instantiates the container and creates the agent, assigning it to `root_agent`.
container = Container()

# Construct the absolute path to the config.yaml file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'config.yaml') # Go up one level to the project root

# Load configuration
container.config.from_yaml(config_path, required=True)

root_agent = create_agent(container)