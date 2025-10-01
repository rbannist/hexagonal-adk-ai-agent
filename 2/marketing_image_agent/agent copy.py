from google.adk.agents import Agent

from .tools import MarketingImageGenerator as MarketingImageGeneratorTool

def generate_image_tool(prompt: str) -> dict:
    """Generates an image using a tool that generates an image, stores it in object storage, commits an aggregate to a repository, and then returns information related to the image - i.e. url, metadata, etc.

    Returns:
        A dictionary containing the result of the image generation process.
    """
    response = marketing_image_generator_tool.generate_image(prompt)
    return response

# def retrieve_image_tool(image_id: str):
#     """Retrieves the bytes for a generated image

#     Returns:
#         A string featuring the bytes for a image mime type
#     """
#     response = marketing_image_retrieval_tool.retrieve_image(image_id)
#     return response

marketing_image_generator_tool = MarketingImageGeneratorTool()
# marketing_image_retrieval_tool = MarketingImageRetrievalTool()

def create_agent() -> Agent:
    agent = Agent(
        name="marketing_image_generating_agent",
        model="gemini-2.5-flash",
        description="Agent to generate images for the marketing department within a supermarket retailer.",
        instruction="Create a prompt based on what the user asks for and then pass the prompt to the generate_image tool.  Pass the response from the tool back to the user to conclude each interaction",
        tools=[generate_image_tool]#,retrieve_image_tool]
    )
    return agent

agent = create_agent()

root_agent = agent