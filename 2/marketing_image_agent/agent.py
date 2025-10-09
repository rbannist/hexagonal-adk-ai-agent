import os
from google.adk.agents import Agent
from dotenv import load_dotenv
from typing import Optional, List

from config import Container
from marketing_image_agent.tools import MarketingImageTools


def generate_image_tool(request_text: str) -> dict:
    """Generates a marketing image from a text prompt.

    This tool handles the end-to-end process of image generation.

    Args:
        request_text: The text prompt to generate the image from.

    Returns:
        A dictionary containing details of the generated image, such as its ID and URL.
    """
    response = marketing_image_tools.generate_image(request_text)
    return response

def change_image_approval_status_request_tool(image_id: str, status_request: str) -> dict:
    """Sends a request to change the approval status of a marketing image.

    Args:
        image_id: The unique identifier of the image to change the approval status for.
        status_request: The approval action to request. Must be 'approve' or 'reject'.

    Returns:
        A dictionary confirming the approval status.
    """
    if status_request not in ["approve", "reject"]:
        return {"error": "Invalid status. Must be 'approve' or 'reject'."}
    return marketing_image_tools.change_image_approval_status_request(image_id, status_request)

def remove_image_tool(image_id: str) -> dict:
    """Removes a marketing image.

    Args:
        image_id: The unique identifier of the image to remove.

    Returns:
        A dictionary confirming the removal.
    """
    return marketing_image_tools.remove_image(image_id)

def change_image_attributes_tool(
    image_id: str,
    new_description: Optional[str] = None,
    new_keywords: Optional[List[str]] = None,
    new_dimensions: Optional[dict] = None,
    new_url: Optional[str] = None,
    new_size: Optional[int] = None,
) -> dict:
    """Changes the attributes of a marketing image.

    Args:
        image_id: The unique identifier of the image to change.
        new_description: The new description for the image.
        new_keywords: A list of new keywords for the image.
        new_dimensions: The new dimensions of the image.
        new_url: The new URL for the image.
        new_size: The new size of the image in bytes.

    Returns:
        A dictionary confirming that the request to change an attribute/attributes  was received.
    """
    return marketing_image_tools.change_image_attributes(image_id, new_description, new_keywords, new_dimensions, new_url, new_size)


marketing_image_tools: MarketingImageTools


def create_agent(container: Container) -> Agent:
    agent = Agent(
        name=container.config.genai.adk.agent_1.name(),
        model=container.config.genai.adk.model_1.name(),
        description=container.config.genai.adk.agent_1.description(),
        instruction=container.config.genai.adk.agent_1.instruction(),
        tools=[generate_image_tool, change_image_approval_status_request_tool, remove_image_tool, change_image_attributes_tool],
    )
    global marketing_image_tools
    marketing_image_tools = MarketingImageTools(container)

    return agent

# The following is added to support the `adk web` command.
# It instantiates the container and creates the agent, assigning it to `root_agent`.
load_dotenv()

container = Container()

# Construct the absolute path to the config.yaml file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'config.yaml') # Go up one level to the project root

# Load configuration
container.config.from_yaml(config_path, required=True)

root_agent = create_agent(container)