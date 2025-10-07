import os
import json

from google.cloud import pubsub_v1

from ....application.ports.marketing_image_integration_event_messaging_output_port import MarketingImageIntegrationEventMessagingOutputPort
from ....application.outbound_integration_events.base_outbound_integration_event import IntegrationEvent
from ....application.factories.marketing_image_thin_integration_event_factory import MarketingImageIntegrationEventsFactory


class MarketingImageIntegrationEventMessagingGoogleCloudEventarcStandardAdapter(MarketingImageIntegrationEventMessagingOutputPort):
    """
    Google Cloud Eventarc Standard (Pub/Sub) implementation of the MarketingImageIntegrationEventMessagingOutputPort.
    """

    def __init__(self, google_cloud_project: str = None, topic_location: str = None, topic_name: str = None, ):
        if not google_cloud_project:
            self.google_cloud_project = os.getenv("GOOGLE_CLOUD_INTEGRATION_EVENT_MESSAGING_ADAPTER_PROJECT", "rbal-assisted-prj1")
        else:
            self.google_cloud_project = google_cloud_project
        
        if not topic_location:
            self.topic_location = os.getenv("GOOGLE_CLOUD_EVENTARC_STANDARD_INTEGRATION_EVENT_MESSAGING_ADAPTER_LOCATION", "global")
        else:
            self.topic_location = topic_location
        
        if not topic_name:
            self.topic_name = os.getenv("GOOGLE_CLOUD_EVENTARC_STANDARD_INTEGRATION_EVENT_MESSAGING_ADAPTER_TOPIC", "rbal-assisted-psiemit1")
        else:
            self.topic_name = topic_name

        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.google_cloud_project, self.topic_name)
    
    def publish(self, integration_event: IntegrationEvent) -> dict:
        """
        Publishes an integration event to a Google Cloud Pub/Sub topic.

        Args:
            integration_event: The integration event to publish.

        Returns:
            A dictionary with the status of the operation and the message ID if successful.
        """
        try:
            # Convert the integration event to a dictionary
            integration_event_dict = MarketingImageIntegrationEventsFactory().to_dict(integration_event)

            # The 'data' field of the event will be the message body
            message_data_dict = integration_event_dict.pop("data", {})
            message_data = json.dumps(message_data_dict).encode("utf-8")

            # The other top-level fields will be message attributes.
            # Pub/Sub attributes must be strings.
            attributes = {}
            for key, value in integration_event_dict.items():
                if isinstance(value, (dict, list)):
                    attributes[key] = json.dumps(value)
                else:
                    attributes[key] = str(value)

            # Publish the message with data and attributes
            future = self.publisher.publish(
                self.topic_path, 
                data=message_data, 
                **attributes
            )
            message_id = future.result()
            print(f"Successfully published message with ID: {message_id} to topic: {self.topic_path}")
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            print(f"Error publishing event to Pub/Sub topic {self.topic_path}: {e}")
            return {"status": "failure", "error": str(e)}