import io
import uuid
import logging
from typing import Tuple, Optional, List
from datetime import datetime
from PIL import Image as PILImage
from google.adk.agents import Agent
from google import genai as genai_images
from google.genai import types as genai_types
from google.cloud import storage, firestore

from config import Config

from marketing_image_agent.shared.utils import DataManipulationUtils

from marketing_image_agent.domain.entities.marketing_image_aggregate import MarketingImage
from marketing_image_agent.domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from marketing_image_agent.domain.factories.marketing_image_domain_events_factory import MarketingImageDomainEventsFactory


config = Config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


aggregate_factory = MarketingImageAggregateFactory()


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


class GoogleCloudFirestoreRepository:
    """
    A class to interact with Google Cloud Firestore.
    """

    def __init__(self, google_cloud_project: str, repository_db_location: str, repository_db_name: str, repository_aggregate_collection_name: str, repository_domain_event_collection_name: str):
        """
        Initialises the GoogleCloudFirestoreRepository class.
        """
        self.google_cloud_project = google_cloud_project
        self.repository_db_location = repository_db_location
        self.repository_db_name = repository_db_name
        self.repository_aggregate_collection_name = repository_aggregate_collection_name
        self.repository_domain_event_collection_name = repository_domain_event_collection_name
        self.aggregate_factory = aggregate_factory
        self.domain_events_factory = MarketingImageDomainEventsFactory()
        self.repository_db = firestore.Client(project=self.google_cloud_project, database=self.repository_db_name)
    
    def _convert_keys_snake_to_camel_case(self, data: dict) -> dict:
        return DataManipulationUtils.convert_keys_snake_to_camel_case(data)

    def _convert_keys_camel_to_snake_case(self, data: dict) -> dict:
        return {DataManipulationUtils.camel_to_snake_case(k): v for k, v in data.items()}

    def _pre_persist_processing(self, data: dict) -> dict:
        """
        Processes the data to convert datetime objects to ISO format strings
        and handles timestamp strings by parsing them into datetime objects.
        """
        processed_data = data.copy()
        for k, v in processed_data.items():
            if isinstance(v, datetime):
                processed_data[k] = v.isoformat()  # Convert datetime to ISO format string
            elif isinstance(v, str):
                try:
                    processed_data[k] = datetime.fromisoformat(v)  # Attempt to parse timestamp strings
                except ValueError:
                    pass  # If parsing fails, assume it's not a timestamp and leave it as is
        return processed_data

    def save(self, marketing_image: MarketingImage) -> None:
        """
        Saves a marketing image aggregate and its domain events to Firestore.
        This method uses a batch write to ensure atomicity and handles both
        the creation of new aggregates and the update of existing ones.
        """
        batch = self.repository_db.batch()

        aggregate_doc_id = str(marketing_image.id)
        aggregate_type = marketing_image.__class__.__name__

        print(f"Saving marketing image aggregate with ID {aggregate_doc_id}")

        # 1. Save/Update the aggregate state
        aggregate_ref = self.repository_db.collection(self.repository_aggregate_collection_name).document(aggregate_doc_id)
        aggregate_data = self.aggregate_factory.to_dict(marketing_image)

        domain_events = aggregate_data.pop("events_list", [])

        if "events_list" in aggregate_data:
            del aggregate_data["events_list"]

        aggregate_data_camel_case = self._convert_keys_snake_to_camel_case(aggregate_data)

        processed_aggregate_data = self._pre_persist_processing(aggregate_data_camel_case)
        batch.set(aggregate_ref, processed_aggregate_data)

        # 2. Save any new domain events to their own collection
        event_id_list = []
        for event in domain_events:
            domain_event_type = event["type"]
            event_doc_id = str(event["id"])
            print(f"Saving {domain_event_type} event with ID {event_doc_id}")
            event_id_list.append(event_doc_id)
            event_ref = self.repository_db.collection(self.repository_domain_event_collection_name).document(event_doc_id)

            if isinstance(event, dict):
                event_data = self._convert_keys_snake_to_camel_case(event)
            else:
                event_data = self._convert_keys_snake_to_camel_case(self.domain_events_factory.to_dict(event))

            processed_event_data = self._pre_persist_processing(event_data)

            batch.set(event_ref, processed_event_data)

        # 3. Commit the transaction
        batch.commit()

        # 4. Clear events from the aggregate instance after they have been persisted
        marketing_image.clear_domain_events()

        print(f"Saved {aggregate_type} {aggregate_doc_id} and its {len(event_id_list)} domain events (IDs: {', '.join(event_id_list)})")

        return marketing_image

    def retrieve_by_id(self, id: uuid.UUID) -> Optional[MarketingImage]:
        """
        Retrieves a marketing image aggregate from Firestore by its ID.
        """
        doc_ref = self.repository_db.collection(self.repository_aggregate_collection_name).document(str(id))
        doc = doc_ref.get()
        if doc.exists:
            data = self._convert_keys_camel_to_snake_case(doc.to_dict())
            return self.aggregate_factory.from_dict(data)
        return None

    def retrieve_all(self) -> List[MarketingImage]:
        """
        Retrieves all marketing image aggregates from Firestore.
        """
        docs = self.repository_db.collection(self.repository_aggregate_collection_name).stream()
        marketing_images = []
        for doc in docs:
            data = self._convert_keys_camel_to_snake_case(doc.to_dict())
            marketing_images.append(self.aggregate_factory.from_dict(data))
        return marketing_images

    def remove(self, id: uuid.UUID) -> None:
        """
        Performs a hard delete of a marketing image aggregate from Firestore.
        """
        doc_ref = self.repository_db.collection(self.repository_aggregate_collection_name).document(str(id))
        doc_ref.delete()


repository = GoogleCloudFirestoreRepository(
    config.google_cloud_project, config.repository_db_location, config.repository_db_name, config.repository_aggregate_collection_name, config.repository_domain_event_collection_name 
)
        

def generate_image_tool(prompt: str) -> dict:
    """Generates an image using Vertex AI and the Imagen 4.0 Fast Generate model, 
    stores it in a Google Cloud Storage bucket, 
    creates or loads an instance of an aggregate, 
    saves the aggregate state to Firestore, 
    and then gives the object's URL to the user.

    Args:
        prompt (str): The prompt for the image generation.

    Returns:
        A dictionary containing the result of the image generation process.
    """

    file_name = f"marketing-{uuid.uuid4()}.png"
    mime_type = "image/png"
    img_width, img_height = 0, 0

    genai_images_client = genai_images.Client(
        vertexai=True,
        project=config.google_cloud_project,
        location=config.ai_image_model_1_location,
        http_options=genai_types.HttpOptions(api_version="v1"),
    )

    generation_parameters = {
        "number_of_images": 1,
        "image_size": "1K",
        "aspect_ratio": "1:1",
        "person_generation": "allow_adult",
        "output_mime_type": mime_type,
    }

    response = genai_images_client.models.generate_images(
        model=config.ai_image_model_1_name,
        prompt=prompt,
        config=genai_types.GenerateImagesConfig(**generation_parameters),
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
    
    image_data = {
        "id": str(uuid.uuid4()),
        "url": image_storage_url,
        "description": prompt,
        "keywords": ["retail"],
        "generation_model": config.ai_image_model_1_name,
        "generation_parameters": generation_parameters,
        "dimensions": {"width": img_width, "height": img_height},
        "size": int(len(generated_image_bytes)),
        "mime_type": generated_image_mime_type,
        "checksum": checksum,
        "created_by": str(uuid.uuid4()), # This could be passed in from the agent context in the future
        "status": "GENERATED",
    }

    marketing_image_aggregate = aggregate_factory.from_dict(image_data)
    marketing_image_aggregate.generate()

    # Persist the aggregate and its events
    repository.save(marketing_image_aggregate)

    return {"image_storage_url": image_storage_url}


def create_agent(config: Config) -> Agent:
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