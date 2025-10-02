import io
import uuid
import logging
from PIL import Image as PILImage
from google.adk.agents import Agent
from google import genai
from google.genai import types
from typing import Tuple, Optional
from google.cloud import storage

from config import Config


config = Config()

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
        self,
        image_data: bytes,
        file_name: str,
        content_type: str,
        metadata: dict = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Saves image data to Google Cloud Storage.

        Args:
            image_data: The byte data of the image.
            file_name: The desired file name for the image in GCS.
            content_type: The content type of the image - e.g. 'image/png'.
            metadata: A dictionary of custom metadata to set on the object.

        Returns:
            A tuple containing the public URL and the base64-encoded MD5 checksum
            of the saved image.
        """
        blob = self.storage_bucket.blob(file_name)
        public_url = None
        checksum = None
        if metadata:
            blob.metadata = metadata       
        try:
            blob.upload_from_string(image_data, content_type=content_type)

            public_url = blob.public_url
            checksum = blob.md5_hash  # This is populated after the upload

            return public_url, checksum
        except Exception as e:
            logger.error(f"Error uploading image to GCS: {e}")
            return public_url, checksum

    def update_marketing_image_metadata(
        self, file_name: str, metadata: dict
    ) -> bool:
        """
        Updates custom metadata for an existing object in Google Cloud Storage.

        Args:
            file_name: The name of the file in GCS.
            metadata: A dictionary containing the metadata to update.

        Returns:
            True if the update was successful, False otherwise.
        """
        blob = self.storage_bucket.blob(file_name)
        try:
            blob.patch()  # Fetch the latest metadata
            current_metadata = blob.metadata or {}
            current_metadata.update(metadata)
            blob.metadata = current_metadata
            blob.patch()
            logger.info(f"Updated metadata for {file_name}: {metadata}")
            return True
        except Exception as e:
            logger.error(f"Error updating metadata for {file_name}: {e}")
            return False

    def delete_marketing_image_object(self, file_name: str):
        """Deletes an object from Google Cloud Storage."""
        blob = self.storage_bucket.blob(file_name)
        blob.delete()
        logger.info(f"Deleted {file_name} from bucket {self.storage_bucket_name}.")


storage_client = GoogleCloudStorage(
    config.google_cloud_project, config.storage_bucket_name
)


def generate_image_tool(prompt: str) -> dict:
    """Generates an image using Vertex AI and the Imagen 4.0 Fast Generate model, stores it in a Google Cloud Storage bucket, and gives the object's information to the user.

    Returns:
        A dictionary containing the result of the image generation process.
    """

    image_id = str(uuid.uuid4())
    file_name = f"marketing-{image_id}.png"
    mime_type = "image/png"
    image_storage_region = config.ai_image_model_1_location
    genai_image_model_region = config.ai_image_model_1_location
    img_width, img_height = 0, 0

    genai_images_client = genai.Client(
        vertexai=True,
        project=config.google_cloud_project,
        location=genai_image_model_region,
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

    initial_metadata = {
        "approvalStatus": "pending",
        "description": prompt,
        "keywords": "",
    }    

    public_url, checksum = storage_client.save_marketing_image_object(
        image_data=generated_image_bytes,
        file_name=file_name,
        content_type=generated_image_mime_type,
        metadata=initial_metadata,
    )
    image_storage_url = public_url

    if image_storage_url:
        logger.info(
            f"File named {file_name} with checksum {checksum} saved at {image_storage_url}"
        )
    else:
        logger.error(f"Failed to upload file {file_name} to cloud storage.")

    return {
        "image_id": image_id,
        "image_storage_region": image_storage_region,
        "image_storage_url": image_storage_url
    }


def accept_image_tool(image_id: str) -> dict:
    file_name = f"marketing-{image_id}.png"
    metadata = {"approvalStatus": "accepted"}
    if storage_client.update_marketing_image_metadata(file_name, metadata):
        return {
            "image_id": image_id,
            "message": "image approval status set as accepted",
        }
    else:
        return {"image_id": image_id, "message": "failed to set image approval status"}

def reject_image_tool(image_id: str) -> dict:
    file_name = f"marketing-{image_id}.png"
    metadata = {"approvalStatus": "rejected"}
    if storage_client.update_marketing_image_metadata(file_name, metadata):
        return {
            "image_id": image_id,
            "message": "image approval status set as rejected",
        }
    else:
        return {"image_id": image_id, "message": "failed to set image approval status"}


def remove_image_tool(image_id: str) -> dict:
    file_name = f"marketing-{image_id}.png"
    try:
        storage_client.delete_marketing_image_object(file_name)
        return {"image_id": image_id, "message": "image object removed from storage"}
    except Exception as e:
        logger.error(f"Failed to remove image {image_id}: {e}")
        return {"image_id": image_id, "message": "failed to remove image object from storage"}


def change_image_metadata_tool(image_id: str, new_description: Optional[str] = None, new_keywords: Optional[list[str]] = None) -> dict:
    file_name = f"marketing-{image_id}.png"
    metadata_to_update = {}
    changed_fields = []

    if new_description is not None:
        metadata_to_update["description"] = new_description
        changed_fields.append("description")

    if new_keywords is not None:
        metadata_to_update["keywords"] = ",".join(new_keywords)
        changed_fields.append("keywords")

    if not metadata_to_update:
        return {"image_id": image_id, "message": "image object metadata not changed"}

    if storage_client.update_marketing_image_metadata(file_name, metadata_to_update):
        message = f"image object { ' and '.join(changed_fields) } changed"
        return {"image_id": image_id, "message": message}
    else:
        return {"image_id": image_id, "message": "failed to change image object metadata"}



def create_agent(config: Config) -> Agent:
    agent = Agent(
        name=config.ai_adk_agent_1_name,
        model=config.ai_adk_model_1_name,
        description=config.ai_adk_agent_1_description,
        instruction=config.ai_adk_agent_1_instruction,
        tools=[generate_image_tool, accept_image_tool, reject_image_tool, remove_image_tool, change_image_metadata_tool],
    )
    return agent


agent = create_agent(config)

root_agent = agent