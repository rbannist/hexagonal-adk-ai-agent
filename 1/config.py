import os
from dotenv import load_dotenv


class Config:
    def __init__(
        self,
        service_name=None,
        domain_event_prefix=None,
        port=None,
        host=None,
        app_url=None,
        google_cloud_project=None,
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

        self.service_name = _get_config(
            service_name, "SERVICE_NAME", "marketing-creative-agent"
        )
        self.domain_event_prefix = _get_config(
            domain_event_prefix, "DOMAIN_EVENT_PREFIX", "ai.dev.domain-event.marketing-image"
        )

        self.port = _get_config(
            port, "PORT", 8080
        )
        self.host = _get_config(
            host, "HOST", "0.0.0.0"
        )
        self.app_url = _get_config(
            app_url, "APP_URL", f"http://{self.host}:{self.port}"
        )

        self.google_cloud_project = _get_config(
            google_cloud_project, "GOOGLE_CLOUD_PROJECT", "rbal-assisted-prj1"
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