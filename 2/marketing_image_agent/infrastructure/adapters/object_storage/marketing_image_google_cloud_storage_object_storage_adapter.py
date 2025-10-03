import os
from google.cloud import storage
from typing import Mapping, Optional, Tuple

from ....shared.utils import DataManipulationUtils
from ....application.ports.marketing_image_object_storage_output_port import MarketingImageObjectStorageOutputPort


class MarketingImageGoogleCloudStorageObjectStorageAdapter(MarketingImageObjectStorageOutputPort):
    """
    A concrete implementation of MarketingImageObjectStorageOutputPort that interacts with Google Cloud Storage.
    """
    def __init__(self, google_cloud_project: str = None, bucket_location: str = None, bucket_name: str = None):
        if not google_cloud_project:
            self.google_cloud_project = os.getenv("GOOGLE_CLOUD_MARKETING_IMAGE_OBJECT_STORAGE_ADAPTER_PROJECT", "rbal-assisted-prj1")
        else:
            self.google_cloud_project = google_cloud_project

        if not bucket_location:
            self.bucket_location = os.getenv("GOOGLE_CLOUD_STORAGE_MARKETING_IMAGE_ADAPTER_LOCATION", "europe-west4")
        else:
            self.bucket_location = bucket_location

        if not bucket_name:
            self.bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_MARKETING_IMAGE_ADAPTER_BUCKET", "rbal-assisted-csew4sb1")
        else:
            self.bucket_name = bucket_name

        self.client = storage.Client(project=self.google_cloud_project)
        self.bucket = self.client.bucket(self.bucket_name)

    def save_marketing_image_object(self, image_data: bytes, file_name: str, content_type: str, fixed_key_metadata: Optional[Mapping[str, str]] = None, custom_metadata: Optional[Mapping[str, str]] = None) -> Tuple[str, str]:
        """
        Saves image data to Google Cloud Storage with specified metadata.

        This function uploads an image file and sets two types of metadata:
        1.  **Fixed-Key Metadata**: Standard GCS object properties like caching
            behaviour, content language, etc.
        2.  **Custom Metadata**: User-defined key-value pairs.

        Args:
            image_data: The byte data of the image.
            file_name: The desired file name for the image in GCS.
            content_type: The content type of the image - e.g. 'image/png'.
                          This can be overridden by the 'content_type' key in
                          `fixed_key_metadata`.
            fixed_key_metadata: Optional dictionary for GCS's fixed-key metadata.
                                Supported keys include 'cache_control', 'content_disposition',
                                'content_encoding', 'content_language', 'content_type',
                                and 'custom_time'.
            custom_metadata: Optional dictionary for any custom metadata key-value pairs (snake_case mapped to hyphenated compounds).

        Returns:
            A tuple containing the public URL and the base64-encoded MD5 checksum
            of the saved image.
        """
        try:
            # Ensure metadata dictionaries are not None to simplify access        
            fixed_meta = fixed_key_metadata or {}
            custom_meta = custom_metadata or {}

            # Convert keys in fixed_meta and custom_meta to hyphenated compounds
            if fixed_meta:
                fixed_meta = {DataManipulationUtils.snake_case_to_hyphenated_compounds(k): v for k, v in fixed_meta.items()}
            if custom_meta:
                custom_meta = {DataManipulationUtils.snake_case_to_hyphenated_compounds(k): v for k, v in custom_meta.items()}     
            blob = self.bucket.blob(file_name)

            # Debugging: Print the content of fixed_meta and custom_meta
            print(f"Attempting to save {file_name} to {self.bucket_name} with content type {content_type}")
            print(f"Object fixed metadata: {fixed_meta}")
            print(f"Object custom metadata: {custom_meta}")

            effective_content_type = fixed_meta.get("Content-Type", content_type)

            # Set blob attributes from metadata dictionaries
            # 1. Custom metadata
            blob.metadata = custom_meta

            # 2. Fixed-key metadata (direct attributes on the blob object)
            # Set default values as required
            blob.cache_control = fixed_meta.get("Cache-Control", "private, max-age=0")
            blob.content_language = fixed_meta.get("Content-Language", "en")

            # Use the value from the metadata dict if present, otherwise use the param
            blob.content_type = effective_content_type

            # Set other optional fixed-key attributes if they are provided
            if "Content-Disposition" in fixed_meta:
                blob.content_disposition = fixed_meta["Content-Disposition"]
            if "Content-Encoding" in fixed_meta:
                blob.content_encoding = fixed_meta["Content-Encoding"]
            if "Custom-Time" in fixed_meta:
                blob.custom_time = fixed_meta["Custom-Time"]

            # Upload the data. The blob object's attributes (metadata, cache_control, etc.)
            # are used in the upload request.
            blob.upload_from_string(image_data, content_type=effective_content_type)

            public_url = blob.public_url
            checksum = blob.md5_hash  # This is populated after the upload

            print(f"Saved {file_name} at URL: {public_url}")

            return public_url, checksum
        except Exception as e:
            # You can log the exception here
            print(f"An error occurred while saving the image: {e}")
            raise # Re-raise the exception or handle it as per your application's error handling policy
        else:
            # This block is executed if no exception occurs in the try block
            print(f"Image {file_name} saved successfully.")

    def retrieve_marketing_image_metadata(self, file_name: str) -> Optional[Mapping[str, str]]:
        """
        Retrieves marketing image metadata from Google Cloud Storage.

        Args:
            file_name: The file name of the image in GCS.

        Returns:
            A dictionary containing the image's metadata, or None if not found.
        """
        try:
            blob = self.bucket.blob(file_name)
            blob.reload()  # Fetch the latest metadata
            if blob.exists:
                metadata = {
                    "cache_control": blob.cache_control,
                    "content_disposition": blob.content_disposition,
                    "content_encoding": blob.content_encoding,
                    "content_language": blob.content_language,
                    "content_type": blob.content_type,
                    "custom_time": blob.custom_time.isoformat() if blob.custom_time else None,
                    "etag": blob.etag,
                    "generation": blob.generation,
                    "id": blob.id,
                    "md5_hash": blob.md5_hash,
                    "media_link": blob.media_link,
                    "metageneration": blob.metageneration,
                    "name": blob.name,
                    "self_link": blob.self_link,
                    "size": blob.size,
                    "storage_class": blob.storage_class,
                    "time_created": blob.time_created.isoformat() if blob.time_created else None,
                    "time_deleted": blob.time_deleted.isoformat() if blob.time_deleted else None,
                    "updated": blob.updated.isoformat() if blob.updated else None,
                    "crc32c": blob.crc32c,
                    "retention_expiration_time": blob.retention_expiration_time.isoformat() if blob.retention_expiration_time else None,
                }
                return metadata
            else:
                return None
        except Exception as e:
            print(f"Error retrieving metadata for {file_name} from Google Cloud Storage: {e}")
            return None

    def retrieve_marketing_image_object(self, file_name: str) -> bytes:
        """
        Retrieves a marketing image object's data from Google Cloud Storage.

        Args:
            file_name: The file name of the image in GCS.

        Returns:
            The byte data of the image.
        """
        try:
            blob = self.bucket.blob(file_name)
            return blob.download_as_bytes()
        except Exception as e:
            print(f"Error retrieving {file_name} from Google Cloud Storage: {e}")
            return None

    def remove_marketing_image_object(self, file_name: str) -> bool:
        """
        Removes a marketing image from Google Cloud Storage.

        Args:
            file_name: The file name of the image to remove.
        """
        try:
            blob = self.bucket.blob(file_name)
            blob.delete()
            return True
        except Exception as e:
            print(f"Error removing {file_name} from Google Cloud Storage: {e}")
            return False