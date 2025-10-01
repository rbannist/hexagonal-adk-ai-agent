import os
import io
from google import genai

from ....application.ports.generate_marketing_image_genai_output_port import MarketingImageImageGenerationOutputPort


class MarketingImageGoogleGeminiFlash2dot5ImageGenAIAdapter(MarketingImageImageGenerationOutputPort):
    """
    This class implements the interface for generating marketing images using the Vertex AI Gemini Flash 2.5 Image model.

    * https://ai.google.dev/docs/gemini_api_overview#gemini-2.5-flash-image
    * Currently preview
    * Supported MIME types: image/png, image/jpeg, image/webp
    * Maximum images per prompt: 3
    * Maximum image size: 7 MB
    * Supported regions: global
    """

    def __init__(self, google_cloud_project: str = None, ai_model_location: str = None, ai_model_name: str = None):
        if not google_cloud_project:
            self.google_cloud_project = os.getenv("GOOGLE_CLOUD_GENAI_IMAGE_ADAPTER_PROJECT", "rbal-assisted-prj1")
        else:
            self.google_cloud_project = google_cloud_project
        
        if not ai_model_location:
            self.ai_model_location = os.getenv("GOOGLE_CLOUD_GENAI_GEMINI_IMAGE_ADAPTER_MODEL_LOCATION", "global")
        else:
            self.ai_model_location = ai_model_location
        
        if not ai_model_name:
            self.ai_model_name = os.getenv("GOOGLE_CLOUD_GENAI_GEMINI_IMAGE_ADAPTER_MODEL_NAME", "gemini-2.5-flash-image-preview")
        else:
            self.ai_model_name = ai_model_name
        
        self.genai_client = genai.Client(
            vertexai=True, project=self.google_cloud_project, location=self.ai_model_location
        )

    def generate_marketing_image(self, prompt: str, min_dimensions: dict = None, max_dimensions: dict = None, mime_type: str = "image/png") -> dict:
        """
        Generates a marketing image using AI.

        Args:
            prompt: The prompt to generate the marketing image.
            mime_type: The MIME type of the generated image - e.g. "image/png" "image/jpeg".
            min_dimensions: A dictionary containing the minimum dimensions of the generated image (height, width).
            max_dimensions: A dictionary containing the maximum dimensions of the generated image (height, width).

        Returns:
            A dictionary containing:
                image_data: The data/bytes of the generated marketing image.
                mime_type: The MIME type of the generated marketing image.
                generation_model: The name of the model used for generation.
                image_dimensions: A dictionary containing the dimensions of the generated marketing image (height, width).
        """

        response = self.genai_client.models.generate_content(model=self.ai_model_name, contents=prompt)

        image_parts = [
            part.inline_data.data
            for part in response.candidates[0].content.parts
            if part.inline_data
        ]

        if not image_parts:
            raise ValueError("Image generation failed, no image data received from the API.")

        generated_image_bytes = image_parts[0]
        print(f"Generated image with size {len(generated_image_bytes)} bytes")

        img_width, img_height = 0, 0

        try:
            from PIL import Image as PILImage

            with PILImage.open(io.BytesIO(generated_image_bytes)) as pil_image:
                img_width, img_height = pil_image.size

        except ImportError:
            print("Warning: Pillow (PIL) is not installed. Cannot determine image dimensions. Returning raw image data.")
            pass
        except Exception as e:
            print(f"Warning: Could not process image with Pillow: {e}. Returning raw image data.")
            pass

        return {
            "image_data": generated_image_bytes,
            "mime_type": "image/png",
            "generation_model": self.ai_model_name,
            "image_dimensions": {
                "height": img_height,
                "width": img_width,
            },
        }