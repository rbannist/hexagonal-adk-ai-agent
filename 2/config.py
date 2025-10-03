from dependency_injector import containers, providers

# Application Services
from marketing_image_agent.application.services.generate_marketing_image_driving_service import GenerateMarketingImageDrivingService
from marketing_image_agent.application.services.generate_marketing_image_core_service import GenerateMarketingImageCoreService
from marketing_image_agent.application.services.generate_marketing_image_driven_service import GenerateMarketingImageDrivenService

# Command Handlers (Application)
from marketing_image_agent.application.command_handlers.generate_marketing_image_command_handler import GenerateMarketingImageCommandHandler
 
# Domain Event Handlers (Application)
from marketing_image_agent.application.domain_event_handlers.marketing_image_generated_domain_event_handler import MarketingImageGeneratedDomainEventHandler

# Adapters inc. Dispatchers (Infrastructure)
from marketing_image_agent.infrastructure.adapters.dispatching.in_memory_command_dispatcher import InMemoryCommandDispatcher
from marketing_image_agent.infrastructure.adapters.dispatching.in_memory_domain_event_dispatcher import InMemoryDomainEventDispatcher
# from marketing_image_agent.infrastructure.adapters.dispatching.eventarc_standard_command_dispatcher impventarcStandardCommandDispatcher  # Placeholder for future adapter
# from marketing_image_agent.infrastructure.adapters.dispatching.eventarc_standard_domain_event_dispatcheort EventarcStandardDomainEventDispatcher  # Placeholder for future adapter
from marketing_image_agent.infrastructure.adapters.repository.marketing_image_aggregate_firestore_repository import MarketingImageAggregateFirestoreRepository
from marketing_image_agent.infrastructure.adapters.object_storage.marketing_image_google_cloud_storage_object_storage_adapter import MarketingImageGoogleCloudStorageObjectStorageAdapter
from marketing_image_agent.infrastructure.adapters.generative_ai.marketing_image_google_cloud_vertex_ai_imagen_adapter import MarketingImageGoogleImagenGenAIAdapter
from marketing_image_agent.infrastructure.adapters.generative_ai.marketing_image_google_cloud_vertex_ai_gemini_flash_2dot5_adapter import MarketingImageGoogleGeminiFlash2dot5ImageGenAIAdapter
from marketing_image_agent.infrastructure.adapters.messaging.marketing_image_integration_event_messaging_google_cloud_eventarc_standard_adapter import MarketingImageIntegrationEventMessagingGoogleCloudEventarcStandardAdapter

# Factories (Domain)
from marketing_image_agent.domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory


## Wire everything up
class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    # Override with environment variables if they exist.
    # This provides a mapping from environment variable names to the configuration keys.
    config.service.name.from_env("SERVICE_1_NAME")
    config.service.host.from_env("HOST")
    config.service.port.from_env("PORT")
    config.service.app_url.from_env("APP_URL")

    config.gcp.project_id.from_env("GOOGLE_CLOUD_PROJECT")
    config.gcp.location.from_env("GOOGLE_CLOUD_LOCATION")
    config.gcp.image_generation_model_family.from_env("IMAGE_GENERATION_MODEL_FAMILY")
    
    config.dispatcher.command.prefix.from_env("COMMAND_PREFIX")
    config.dispatcher.command.type.from_env("COMMAND_DISPATCHER_TYPE")
    config.dispatcher.domain_event.prefix.from_env("DOMAIN_EVENT_PREFIX")
    config.dispatcher.domain_event.type.from_env("DOMAIN_EVENT_DISPATCHER_TYPE")
    config.dispatcher.integration_event.prefix.from_env("INTEGRATION_EVENT_PREFIX")

    config.repository.firestore.project_id.from_env("GOOGLE_CLOUD_REPOSITORY_ADAPTER_PROJECT")
    config.repository.firestore.location.from_env("GOOGLE_CLOUD_REPOSITORY_ADAPTER_LOCATION")
    config.repository.firestore.database.from_env("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_DATABASE")
    config.repository.firestore.marketing_images_collection.from_env("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_COLLECTION_MARKETING_IMAGES")
    config.repository.firestore.domain_events_collection.from_env("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_COLLECTION_MARKETING_IMAGE_EVENTS")

    config.object_storage.gcs.project_id.from_env("GOOGLE_CLOUD_MARKETING_IMAGE_OBJECT_STORAGE_ADAPTER_PROJECT")
    config.object_storage.gcs.location.from_env("GOOGLE_CLOUD_STORAGE_MARKETING_IMAGE_ADAPTER_LOCATION")
    config.object_storage.gcs.bucket.from_env("GOOGLE_CLOUD_STORAGE_MARKETING_IMAGE_ADAPTER_BUCKET")

    config.genai.vertex_ai.image.project_id.from_env("GOOGLE_CLOUD_GENAI_IMAGE_ADAPTER_PROJECT")
    config.genai.vertex_ai.image.imagen_model_location.from_env("GOOGLE_CLOUD_GENAI_IMAGEN_IMAGE_ADAPTER_MODEL_LOCATION")
    config.genai.vertex_ai.image.imagen_model_name.from_env("GOOGLE_CLOUD_GENAI_IMAGEN_IMAGE_ADAPTER_MODEL_NAME")
    config.genai.vertex_ai.image.gemini_model_location.from_env("GOOGLE_CLOUD_GENAI_GEMINI_IMAGE_ADAPTER_MODEL_LOCATION")
    config.genai.vertex_ai.image.gemini_model_name.from_env("GOOGLE_CLOUD_GENAI_GEMINI_IMAGE_ADAPTER_MODEL_NAME")
    config.genai.vertex_ai.multimodal.project_id.from_env("GOOGLE_CLOUD_GENAI_MULTIMODAL_ADAPTER_MODEL_PROJECT")
    config.genai.vertex_ai.multimodal.model_location.from_env("GOOGLE_CLOUD_GENAI_MULTIMODAL_ADAPTER_MODEL_LOCATION")
    config.genai.vertex_ai.multimodal.model_name.from_env("GOOGLE_CLOUD_GENAI_MULTIMODAL_ADAPTER_MODEL_NAME")

    config.messaging.eventarc_standard.project_id.from_env("GOOGLE_CLOUD_INTEGRATION_EVENT_MESSAGING_ADAPTER_PROJECT")
    config.messaging.eventarc_standard.location.from_env("GOOGLE_CLOUD_EVENTARC_STANDARD_INTEGRATION_EVENT_MESSAGING_ADAPTER_LOCATION")
    config.messaging.eventarc_standard.topic.from_env("GOOGLE_CLOUD_EVENTARC_STANDARD_INTEGRATION_EVENT_MESSAGING_ADAPTER_TOPIC")

    # Factories (Domain)
    marketing_image_aggregate_factory = providers.Singleton(MarketingImageAggregateFactory)

    # Adapters (Infrastructure)
    command_dispatcher = providers.Selector(
        config.dispatcher.command.type,
        in_memory=providers.Singleton(InMemoryCommandDispatcher),
        # pubsub=providers.Singleton(
        #     PubSubCommandDispatcher,
        #     project_id=config.gcp.project_id,  # Example of further config needed
        # ),
    )
    domain_event_dispatcher = providers.Selector(
        config.dispatcher.domain_event.type,
        in_memory=providers.Singleton(InMemoryDomainEventDispatcher),
        # pubsub=providers.Singleton(
        #     PubSubDomainEventDispatcher,
        #     project_id=config.gcp.project_id,  # Example of further config needed
        # ),
    )
    marketing_image_repository = providers.Factory(
        MarketingImageAggregateFirestoreRepository,
        google_cloud_project=config.repository.firestore.project_id,
        db_location=config.repository.firestore.location,
        db_name=config.repository.firestore.database,
        aggregate_collection_name=config.repository.firestore.marketing_images_collection,
        domain_event_collection_name=config.repository.firestore.domain_events_collection,
    )
    marketing_image_object_storage = providers.Factory(
        MarketingImageGoogleCloudStorageObjectStorageAdapter,
        google_cloud_project=config.object_storage.gcs.project_id,
        bucket_location=config.object_storage.gcs.location,
        bucket_name=config.object_storage.gcs.bucket,
    )
    marketing_image_genai_adapter = providers.Selector(
        config.gcp.image_generation_model_family,
        imagen=providers.Factory(
            MarketingImageGoogleImagenGenAIAdapter,
            google_cloud_project=config.genai.vertex_ai.image.project_id,
            ai_model_location=config.genai.vertex_ai.image.imagen_model_location,
            ai_model_name=config.genai.vertex_ai.image.imagen_model_name,
        ),
        gemini=providers.Factory(
            MarketingImageGoogleGeminiFlash2dot5ImageGenAIAdapter,
            google_cloud_project=config.genai.vertex_ai.image.project_id,
            ai_model_location=config.genai.vertex_ai.image.gemini_model_location,
            ai_model_name=config.genai.vertex_ai.image.gemini_model_name,
        ),
    )
    marketing_image_integration_event_messaging = providers.Factory(
        MarketingImageIntegrationEventMessagingGoogleCloudEventarcStandardAdapter,
        google_cloud_project=config.messaging.eventarc_standard.project_id,
        topic_location=config.messaging.eventarc_standard.location,
        topic_name=config.messaging.eventarc_standard.topic,
    )

    # Driving Services (Application)
    generate_marketing_image_driving_service = providers.Factory(
        GenerateMarketingImageDrivingService,
        command_dispatcher=command_dispatcher,
        command_prefix=config.dispatcher.command.prefix,
    )

    # Core Services (Application)
    generate_marketing_image_core_service = providers.Factory(
        GenerateMarketingImageCoreService,
        marketing_image_repository=marketing_image_repository,
        marketing_image_object_storage=marketing_image_object_storage,
        marketing_image_genai_generator=marketing_image_genai_adapter,
        domain_event_prefix=config.dispatcher.domain_event.prefix,
        domain_event_dispatcher=domain_event_dispatcher,
    )

    # Driven Services (Application)
    generate_marketing_image_driven_service = providers.Factory(
        GenerateMarketingImageDrivenService,
        integration_event_prefix=config.dispatcher.integration_event.prefix,
        marketing_image_integration_event_messaging=marketing_image_integration_event_messaging,
    )

    # Command Handlers (Application) - Eagerly instantiated in main.py to register themselves
    generate_marketing_image_command_handler = providers.Singleton(
        GenerateMarketingImageCommandHandler,
        core_service=generate_marketing_image_core_service,
        command_dispatcher=command_dispatcher,
    )

    # Domain Event Handlers (Application) - Eagerly instantiated in main.py to register themselves
    marketing_image_generated_domain_event_handler = providers.Singleton(
        MarketingImageGeneratedDomainEventHandler,
        driven_service=generate_marketing_image_driven_service,
        domain_event_dispatcher=domain_event_dispatcher,
    )