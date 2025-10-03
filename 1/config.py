import os
from dotenv import load_dotenv

class Config:
    def __init__(
        self,
        port=None,
        host=None,
        app_url=None,
        service_1_name=None,
        service_1_description=None,
        domain_event_prefix=None,
        google_cloud_project=None,
        google_cloud_location=None,
        google_cloud_use_vertex_ai_or_ai_studio=None,
        ai_adk_model_1_name=None,
        ai_adk_agent_1_artifact_storage_bucket_name=None,
        ai_adk_agent_1_name=None,
        ai_adk_agent_1_description=None,
        ai_adk_agent_1_instruction=None,
        ai_image_model_1_name=None,
        ai_image_model_1_location=None,
        storage_bucket_name=None,
        repository_db_location=None,
        repository_db_name=None,
        repository_aggregate_collection_name=None,
        repository_domain_event_collection_name=None,
    ):
        load_dotenv()
        def _get_config(arg_val, env_var, default):
            return arg_val if arg_val is not None else os.getenv(env_var, default)

        self.port = _get_config(
            port, "PORT", 8080
        )
        self.host = _get_config(
            host, "HOST", "0.0.0.0"
        )
        self.app_url = _get_config(
            app_url, "APP_URL", f"http://{self.host}:{self.port}"
        )

        self.service_1_name = _get_config(
            service_1_name, "SERVICE_1_NAME", "marketing-creative-agent"
        )
        self.service_1_description = _get_config(
            service_1_description, "SERVICE_1_DESCRIPTION", "A marketing creative AI agent that helps users generate images and then manage the business lifecycle of them."
        )

        self.google_cloud_project = _get_config(
            google_cloud_project, "GOOGLE_CLOUD_PROJECT", "rbal-assisted-prj1"
        )
        self.google_cloud_location = _get_config(
            google_cloud_location, "GOOGLE_CLOUD_LOCATION", "europe-west4"
        )
        self.google_cloud_use_vertex_ai_or_ai_studio = _get_config(
            google_cloud_use_vertex_ai_or_ai_studio, "GOOGLE_GENAI_USE_VERTEXAI", "TRUE"
        )

        self.domain_event_prefix = _get_config(
            domain_event_prefix, "DOMAIN_EVENT_PREFIX", "ai.dev.domain-event.marketing-image"
        )

        self.ai_adk_model_1_name = _get_config(
            ai_adk_model_1_name, "ADK_MODEL_1_NAME", "gemini-2.5-flash"
        )
        self.ai_adk_agent_1_artifact_storage_bucket_name = _get_config(
            ai_adk_agent_1_artifact_storage_bucket_name,
            "ADK_AGENT_1_ARTIFACT_STORAGE_BUCKET_NAME",
            "rbal-assisted-csew4sb2",
        )
        self.ai_adk_agent_1_name = _get_config(
            ai_adk_agent_1_name, "ADK_AGENT_1_NAME", "marketing_creative_image_lifecycle_agent"
        )
        self.ai_adk_agent_1_description = _get_config(
            ai_adk_agent_1_description,
            "ADK_AGENT_1_DESCRIPTION",
            "You are helpful assistant that helps users in a marketing department of a supermarket retailer generate, accept, reject, remove, and change the metadata (description and keywords) of images.",
        )
        self.ai_adk_agent_1_instruction = _get_config(
            ai_adk_agent_1_instruction,
            "ADK_AGENT_1_INSTRUCTION",
            "Firstly, determine whether the user wishes to generate, accept, reject, remove, or change the metadata of an image.  In the absence of a clear intention, assume the user wants to generate an image - i.e. unless they request to accept, reject, remove, or change metadata, assume they want to generate an image.  The user will signal a desire to change image metadata by asking to change metadata or specific metadata keys.  The metadata keys they are able to change are description, dimensions, url, size, and keywords.  keywords should be captured as a comma-separated list.  If the user wants to generate an image, create a prompt based on what the user asks for as verbatim as possible and then pass the prompt to the generate_image tool.  After the tool responds, pass the response back to the user to conclude the interaction.  You should always include the image_storage_url value in the response.  If the user specifically asks to accept, reject, remove, or change the metadata of an image, use the appropriate tool to complete that request.  Pass back the tool's response to the user once it responds.",
        )
        self.ai_image_model_1_location = _get_config(
            ai_image_model_1_location, self.google_cloud_location, "europe-west4"
        )
        self.ai_image_model_1_name = _get_config(
            ai_image_model_1_name,
            "GOOGLE_CLOUD_GENAI_IMAGE_MODEL_1_NAME",
            "imagen-4.0-fast-generate-001",
        )
        self.storage_bucket_name = _get_config(
            storage_bucket_name, "GOOGLE_CLOUD_STORAGE_BUCKET", "rbal-assisted-csew4sb2"
        )

        self.repository_db_location = _get_config(
            repository_db_location, "GOOGLE_CLOUD_REPOSITORY_LOCATION", "europe-west4"
        )
        self.repository_db_name = _get_config(
            repository_db_name, "GOOGLE_CLOUD_FIRESTORE_REPOSITORY_DATABASE", "claim-check-ew4-1"
        )
        self.repository_aggregate_collection_name = _get_config(
            repository_aggregate_collection_name, "GOOGLE_CLOUD_FIRESTORE_REPOSITORY_COLLECTION_MARKETING_IMAGES", "marketing-image-aggregates"
        )
        self.repository_domain_event_collection_name = _get_config(
            repository_domain_event_collection_name, "GOOGLE_CLOUD_FIRESTORE_REPOSITORY_COLLECTION_MARKETING_IMAGE_EVENTS", "marketing-image-domain-events"
        )