import os
import io
import uuid
import logging
from dotenv import load_dotenv
from PIL import Image as PILImage
from google.adk.agents import Agent
from google import genai
from google.genai import types
from typing import Tuple, Optional
from google.cloud import storage


class EnvironmentConfiguration:
    def __init__(
        self,
        google_cloud_project=None,
        ai_adk_model_1_name=None,
        ai_adk_agent_1_name=None,
        ai_adk_agent_1_description=None,
        ai_adk_agent_1_instruction=None,
        ai_image_model_1_name=None,
        ai_image_model_1_location=None,
        storage_bucket_name=None,
    ):
        load_dotenv()

        def _get_config(arg_val, env_var, default):
            return arg_val if arg_val is not None else os.getenv(env_var, default)

        self.google_cloud_project = _get_config(
            google_cloud_project, "GOOGLE_CLOUD_PROJECT", "rbal-assisted-prj1"
        )
        self.ai_adk_model_1_name = _get_config(
            ai_adk_model_1_name, "ADK_MODEL_1_NAME", "gemini-1.5-flash"
        )
        self.ai_adk_agent_1_name = _get_config(
            ai_adk_agent_1_name, "ADK_AGENT_1_NAME", "marketing_image_generating_agent"
        )
        self.ai_adk_agent_1_description = _get_config(
            ai_adk_agent_1_description,
            "ADK_AGENT_1_DESCRIPTION",
            "Agent to generate images for the marketing department within a supermarket retailer.",
        )
        self.ai_adk_agent_1_instruction = _get_config(
            ai_adk_agent_1_instruction,
            "ADK_AGENT_1_INSTRUCTION",
            "Create a prompt based on what the user asks for and then pass the prompt to the generate_image tool.  Pass the response from the tool back to the user to conclude each interaction.",
        )
        self.ai_image_model_1_location = _get_config(
            ai_image_model_1_location, "GOOGLE_CLOUD_LOCATION", "europe-west4"
        )
        self.ai_image_model_1_name = _get_config(
            ai_image_model_1_name,
            "GOOGLE_CLOUD_GENAI_IMAGE_MODEL_1_NAME",
            "imagen-3.0-generate-fast-001",
        )
        self.storage_bucket_name = _get_config(
            storage_bucket_name, "GOOGLE_CLOUD_STORAGE_BUCKET", "rbal-assisted-csew4sb2"
        )


config = EnvironmentConfiguration()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCloudStorage:
    """
    A class to interact with Google Cloud Storage.
    """

    def __init__(self, google_cloud_project: str, storage_bucket_name: str):
        """
        Initialises the GoogleCloudStorage class.

        Args:
            google_cloud_project (str): The Google Cloud project ID.
            storage_bucket_name (str): The name of the bucket.
        """
        self.google_cloud_project = google_cloud_project
        self.storage_bucket_name = storage_bucket_name

        self.storage_client = storage.Client(project=self.google_cloud_project)
        self.storage_bucket = self.storage_client.bucket(self.storage_bucket_name)

    def save_marketing_image_object(
        self, image_data: bytes, file_name: str, content_type: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Saves image data to Google Cloud Storage.

        Args:
            image_data: The byte data of the image.
            file_name: The desired file name for the image in GCS.
            content_type: The content type of the image - e.g. 'image/png'.

        Returns:
            A tuple containing the public URL and the base64-encoded MD5 checksum
            of the saved image.
        """
        blob = self.storage_bucket.blob(file_name)
        public_url = None
        checksum = None
        try:
            blob.upload_from_string(image_data, content_type=content_type)

            public_url = blob.public_url
            checksum = blob.md5_hash  # This is populated after the upload

            return public_url, checksum
        except Exception as e:
            logger.error(f"Error uploading image to GCS: {e}")
            return public_url, checksum


storage_client = GoogleCloudStorage(
    config.google_cloud_project, config.storage_bucket_name
)


def generate_image_tool(prompt: str) -> dict:
    """Generates an image using Vertex AI and the Imagen 3.0 Fast Generate model, stores it in a Google Cloud Storage bucket, and gives the object's URL to the user.

    Returns:
        A dictionary containing the result of the image generation process.
    """

    file_name = f"marketing-{uuid.uuid4()}.png"
    mime_type = "image/png"
    img_width, img_height = 0, 0

    genai_images_client = genai.Client(
        vertexai=True,
        project=config.google_cloud_project,
        location=config.ai_image_model_1_location,
        http_options=types.HttpOptions(api_version="v1"),
    )

    response = genai_images_client.models.generate_images(
        model=config.ai_image_model_1_name,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            image_size="1K",  # This implies the largest dimension will be 1024, and the other scaled by aspect_ratio
            aspect_ratio="1:1",
            person_generation="allow_adult",
            output_mime_type=mime_type,
        ),
    )

    generated_image = response.generated_images[0]
    generated_image_bytes = generated_image.image.image_bytes
    generated_image_mime_type = generated_image.image.mime_type

    with PILImage.open(io.BytesIO(generated_image_bytes)) as pil_image:
        img_width, img_height = pil_image.size

    logger.info(
        f"Image generated using {config.ai_image_model_1_name} with size {len(generated_image_bytes)}, mime type {generated_image_mime_type}, and dimensions {img_height}*{img_width}"
    )

    public_url, checksum = storage_client.save_marketing_image_object(
        image_data=generated_image_bytes,
        file_name=file_name,
        content_type=generated_image_mime_type,
    )
    image_storage_url = public_url

    if image_storage_url:
        logger.info(
            f"File named {file_name} with checksum {checksum} saved at {image_storage_url}"
        )
    else:
        logger.error(f"Failed to upload file {file_name} to cloud storage.")

    return {"image_storage_url": image_storage_url}


def create_agent(config: EnvironmentConfiguration) -> Agent:
    agent = Agent(
        name=config.ai_adk_agent_1_name,
        model=config.ai_adk_model_1_name,
        description=config.ai_adk_agent_1_description,
        instruction=config.ai_adk_agent_1_instruction,
        tools=[generate_image_tool],
    )
    return agent


agent = create_agent(config)

root_agent = agent
