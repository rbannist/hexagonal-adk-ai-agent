from dependency_injector import containers, providers

# Application Services
from .application.services.generate_marketing_image_driving_service import GenerateMarketingImageDrivingService
from .application.services.generate_marketing_image_core_service import GenerateMarketingImageCoreService
from .application.services.generate_marketing_image_driven_service import GenerateMarketingImageDrivenService

# Command Handlers (Application)
from .application.command_handlers.generate_marketing_image_command_handler import GenerateMarketingImageCommandHandler
 
# Domain Event Handlers (Application)
from .application.domain_event_handlers.marketing_image_generated_domain_event_handler import MarketingImageGeneratedDomainEventHandler

# Adapters inc. Dispatchers (Infrastructure)
from .infrastructure.adapters.dispatching.in_memory_command_dispatcher import InMemoryCommandDispatcher
from .infrastructure.adapters.dispatching.in_memory_domain_event_dispatcher import InMemoryDomainEventDispatcher
# from .infrastructure.adapters.dispatching.eventarc_standard_command_dispatcher import EventarcStandardCommandDispatcher  # Placeholder for future adapter
# from .infrastructure.adapters.dispatching.eventarc_standard_domain_event_dispatcher import EventarcStandardDomainEventDispatcher  # Placeholder for future adapter
from .infrastructure.adapters.repository.marketing_image_aggregate_firestore_repository import MarketingImageAggregateFirestoreRepository
from .infrastructure.adapters.object_storage.marketing_image_google_cloud_storage_object_storage_adapter import MarketingImageGoogleCloudStorageObjectStorageAdapter
from .infrastructure.adapters.generative_ai.marketing_image_google_cloud_vertex_ai_imagen_adapter import MarketingImageGoogleImagenGenAIAdapter
from .infrastructure.adapters.generative_ai.marketing_image_google_cloud_vertex_ai_gemini_flash_2dot5_adapter import MarketingImageGoogleGeminiFlash2dot5ImageGenAIAdapter
from .infrastructure.adapters.event_store.domain.marketing_image_domain_event_store_firestore import MarketingImageDomainEventEventStoreGoogleCloudFirestoreAdapter
from .infrastructure.adapters.event_store.integration.marketing_image_integration_event_event_store_google_cloud_firestore_adapter import MarketingImageIntegrationEventEventStoreGoogleCloudFirestoreAdapter
from .infrastructure.adapters.messaging.marketing_image_integration_event_messaging_google_cloud_eventarc_standard_adapter import MarketingImageIntegrationEventMessagingGoogleCloudEventarcStandardAdapter
from .infrastructure.adapters.read_view_projections.marketing_image_primary_read_view_google_cloud_firestore_adapter import MarketingImagePrimaryReadViewGoogleCloudFirestoreAdapter

# Factories (Domain)
from .domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory


## Wire everything up
class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    # Override with environment variables if they exist.
    # This provides a mapping from environment variable names to the configuration keys.
    config.gcp.service_name.from_env("SERVICE_NAME")
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

    config.event_store.domain.firestore.project_id.from_env("GOOGLE_CLOUD_DOMAIN_EVENT_STORE_ADAPTER_PROJECT")
    config.event_store.domain.firestore.location.from_env("GOOGLE_CLOUD_DOMAIN_EVENT_STORE_ADAPTER_LOCATION")
    config.event_store.domain.firestore.database.from_env("GOOGLE_CLOUD_FIRESTORE_DOMAIN_EVENT_STORE_ADAPTER_DATABASE")
    config.event_store.domain.firestore.collection.from_env("GOOGLE_CLOUD_FIRESTORE_DOMAIN_EVENT_STORE_ADAPTER_COLLECTION_MARKETING_IMAGE_EVENTS")

    config.event_store.integration.firestore.project_id.from_env("GOOGLE_CLOUD_INTEGRATION_EVENT_STORE_ADAPTER_PROJECT")
    config.event_store.integration.firestore.location.from_env("GOOGLE_CLOUD_INTEGRATION_EVENT_STORE_ADAPTER_LOCATION")
    config.event_store.integration.firestore.database.from_env("GOOGLE_CLOUD_FIRESTORE_INTEGRATION_EVENT_STORE_ADAPTER_DATABASE")
    config.event_store.integration.firestore.collection.from_env("GOOGLE_CLOUD_FIRESTORE_INTEGRATION_EVENT_STORE_ADAPTER_COLLECTION_MARKETING_IMAGE_EVENTS")

    config.primary_read_view.firestore.project_id.from_env("GOOGLE_CLOUD_PRIMARY_READ_VIEW_ADAPTER_PROJECT")
    config.primary_read_view.firestore.location.from_env("GOOGLE_CLOUD_PRIMARY_READ_VIEW_ADAPTER_LOCATION")
    config.primary_read_view.firestore.database.from_env("GOOGLE_CLOUD_FIRESTORE_PRIMARY_READ_VIEW_ADAPTER_DATABASE")
    config.primary_read_view.firestore.collection.from_env("GOOGLE_CLOUD_FIRESTORE_PRIMARY_READ_VIEW_ADAPTER_COLLECTION")

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
    marketing_image_domain_event_event_store = providers.Factory(
        MarketingImageDomainEventEventStoreGoogleCloudFirestoreAdapter,
        google_cloud_project=config.event_store.domain.firestore.project_id,
        db_location=config.event_store.domain.firestore.location,
        db_name=config.event_store.domain.firestore.database,
        domain_event_collection_name=config.event_store.domain.firestore.collection,
    )
    marketing_image_integration_event_event_store = providers.Factory(
        MarketingImageIntegrationEventEventStoreGoogleCloudFirestoreAdapter,
        google_cloud_project=config.event_store.integration.firestore.project_id,
        db_location=config.event_store.integration.firestore.location,
        db_name=config.event_store.integration.firestore.database,
        integration_event_collection_name=config.event_store.integration.firestore.collection,
    )
    marketing_image_integration_event_messaging = providers.Factory(
        MarketingImageIntegrationEventMessagingGoogleCloudEventarcStandardAdapter,
        google_cloud_project=config.messaging.eventarc_standard.project_id,
        topic_location=config.messaging.eventarc_standard.location,
        topic_name=config.messaging.eventarc_standard.topic,
    )
    marketing_image_primary_read_view = providers.Factory(
        MarketingImagePrimaryReadViewGoogleCloudFirestoreAdapter,
        google_cloud_project=config.primary_read_view.firestore.project_id,
        db_location=config.primary_read_view.firestore.location,
        db_name=config.primary_read_view.firestore.database,
        primary_read_view_collection_name=config.primary_read_view.firestore.collection,
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
        marketing_image_integration_event_event_store=marketing_image_integration_event_event_store,
        marketing_image_primary_read_view=marketing_image_primary_read_view,
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