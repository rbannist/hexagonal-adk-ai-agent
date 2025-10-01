import os
import io
from google import genai
from google.genai import types

from ....application.ports.generate_marketing_image_genai_output_port import MarketingImageImageGenerationOutputPort


class MarketingImageGoogleImagenGenAIAdapter(MarketingImageImageGenerationOutputPort):
    """
    This class implements the interface for generating marketing images using the Vertex AI Imagen 4.0 Fast Generate model.
    """

    SUPPORTED_GENERATION_DIMENSIONS = {
        "1:1": (1024, 1024),
        "4:3": (1024, 768),
        "3:4": (768, 1024),
        "16:9": (1024, 576),
        "9:16": (576, 1024),
    }
    DEFAULT_GENERATION_ASPECT_RATIO = "1:1"
    DEFAULT_GENERATION_WIDTH = 1024
    DEFAULT_GENERATION_HEIGHT = 1024


    def __init__(self, google_cloud_project: str = None, ai_model_location: str = None, ai_model_name: str = None):
        if not google_cloud_project:
            self.google_cloud_project = os.getenv("GOOGLE_CLOUD_GENAI_IMAGE_ADAPTER_PROJECT", "rbal-assisted-prj1")
        else:
            self.google_cloud_project = google_cloud_project
        
        if not ai_model_location:
            self.ai_model_location = os.getenv("GOOGLE_CLOUD_GENAI_IMAGEN_IMAGE_ADAPTER_MODEL_LOCATION", "europe-west4")
        else:
            self.ai_model_location = ai_model_location
        
        if not ai_model_name:
            self.ai_model_name = os.getenv("GOOGLE_CLOUD_GENAI_IMAGEN_IMAGE_ADAPTER_MODEL_NAME", "imagen-4.0-fast-generate-001")
        else:
            self.ai_model_name = ai_model_name
        
        self.genai_images_client = genai.Client(
            vertexai=True,
            project=self.google_cloud_project,
            location=self.ai_model_location,
            http_options=types.HttpOptions(api_version='v1')
        )

    def _get_closest_generation_aspect_ratio_and_dimensions(self, min_dimensions: dict = None, max_dimensions: dict = None) -> tuple[int, int, str]:
        """
        Determines the closest supported aspect ratio string and its corresponding "1K" dimensions
        based on the provided min and max dimensions.
        Returns (width, height, aspect_ratio_string) for generation.
        """
        target_width = self.DEFAULT_GENERATION_WIDTH
        target_height = self.DEFAULT_GENERATION_HEIGHT

        # Prioritise max_dimensions for determining the target aspect ratio
        if max_dimensions and max_dimensions.get("width") and max_dimensions.get("height"):
            target_width = max_dimensions["width"]
            target_height = max_dimensions["height"]
        elif min_dimensions and min_dimensions.get("width") and min_dimensions.get("height"):
            target_width = min_dimensions["width"]
            target_height = min_dimensions["height"]
        
        if not target_width or not target_height:
            return self.DEFAULT_GENERATION_WIDTH, self.DEFAULT_GENERATION_HEIGHT, self.DEFAULT_GENERATION_ASPECT_RATIO

        input_ratio = target_width / target_height
        
        closest_ar_str = self.DEFAULT_GENERATION_ASPECT_RATIO
        min_diff = float('inf')

        for ar_str, (ar_width, ar_height) in self.SUPPORTED_GENERATION_DIMENSIONS.items():
            current_ar_val = ar_width / ar_height
            diff = abs(input_ratio - current_ar_val)
            if diff < min_diff:
                min_diff = diff
                closest_ar_str = ar_str
        
        # Return the dimensions corresponding to the closest aspect ratio
        chosen_width, chosen_height = self.SUPPORTED_GENERATION_DIMENSIONS[closest_ar_str]
        return chosen_width, chosen_height, closest_ar_str

    def generate_marketing_image(self, prompt: str, min_dimensions: dict = None, max_dimensions: dict = None, mime_type: str = "image/png") -> dict:
        """
        Generates a marketing image using AI.

        Args:
            prompt: The prompt to generate the marketing image.
            min_dimensions: The minimum dimensions of the generated image.
            max_dimensions: The maximum dimensions of the generated image.
            mime_type: The MIME type of the generated image - e.g. "image/png" "image/jpeg".

        Returns:
            A dictionary containing:
                image_data: The data/bytes of the generated marketing image.
                mime_type: The MIME type of the generated marketing image.
                generation_model: The name of the model used for generation.
                image_dimensions: A dictionary containing the dimensions of th generated marketing image (height, width).
        """
        # Determine the aspect ratio and actual dimensions for the AI generatin
        generated_width, generated_height, aspect_ratio_for_generation = self._get_closest_generation_aspect_ratio_and_dimensions(min_dimensions, max_dimensions)

        response = self.genai_images_client.models.generate_images(
            model=self.ai_model_name,
            prompt=prompt,
            config=types.GenerateImagesConfig( # type: ignore
                number_of_images=1,
                image_size="1K", # This implies the largest dimension will be 024, and the other scaled by aspect_ratio
                aspect_ratio=aspect_ratio_for_generation,
                person_generation="allow_adult",
                output_mime_type=mime_type,
            ),
        )

        generated_image = response.generated_images[0]
        generated_image_image_bytes = generated_image.image.image_bytes
        generated_image_mime_type = generated_image.image.mime_type
        print(f"Generated image with size {len(generated_image_image_bytes)} bytes and MIME type {generated_image_mime_type}")

        # Get image dimensions from the generated image data
        # The model should have generated an image with dimensions (generated_width, generated_height)
        # based on the aspect_ratio_for_generation and image_size="1K".
        img_width, img_height = generated_width, generated_height # Assume generated dimensions match our chosen ones
        pil_image = None # Initialise pil_image
        try:
            from PIL import Image as PILImage
            from PIL import ImageOps as PILImageOps
            pil_image = PILImage.open(io.BytesIO(generated_image.image.image_bytes))
            
            # Verify actual generated dimensions
            actual_gen_width, actual_gen_height = pil_image.size
            if actual_gen_width != generated_width or actual_gen_height != generated_height:
                print(f"Warning: Generated image dimensions ({actual_gen_width}x{actual_gen_height}) do not match expected ({generated_width}x{generated_height}) for aspect ratio {aspect_ratio_for_generation}. Using actual.")
                img_width, img_height = actual_gen_width, actual_gen_height

            # Apply post-generation resizing if max_dimensions are provided and the generated image exceeds them
            if max_dimensions and max_dimensions.get("width") and max_dimensions.get("height"):
                max_w = max_dimensions["width"]
                max_h = max_dimensions["height"]
                if img_width > max_w or img_height > max_h:
                    pil_image = PILImageOps.contain(pil_image, (max_w, max_h))
                    img_width, img_height = pil_image.size # Update dimensions after resize
        except ImportError:
            # PIL not installed, dimensions will remain as assumed generated_width, generated_height
            pass

        # Convert the final PIL image to bytes
        image_data = None
        if pil_image: # Only proceed if PIL image was successfully created
            with io.BytesIO() as output:
                format_str = mime_type.split('/')[-1].upper()
                if format_str == "JPG": # PIL uses JPEG for image/jpeg
                    format_str = "JPEG"
                try:
                    pil_image.save(output, format=format_str)
                except KeyError: # Fallback if format_str is not directly supported by PIL save
                    print(f"Warning: PIL does not directly support saving to format '{format_str}'. Attempting PNG.")
                    pil_image.save(output, format="PNG") # Default to PNG
                image_data = output.getvalue()
        else:
            # Fallback to raw data if PIL processing was skipped (e.g. due to ImportError or if PIL is not installed)
            image_data = generated_image_image_bytes # Use the original generated bytes

        return {
            "image_data": image_data,
            "mime_type": mime_type,
            "generation_model": self.ai_model_name,
            "image_dimensions": {
                "height": img_height,
                "width": img_width,
            },
        }