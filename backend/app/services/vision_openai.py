from __future__ import annotations

import base64

from openai import AsyncOpenAI

from app.config import Settings
from app.models.schemas import ImageAnalysis


SYSTEM_PROMPT = """You are Pixel Forge's 3D reconstruction analyst.
Inspect the reference image and produce precise geometry-oriented information for an image-to-3D system.
Focus on shape, proportions, orientation, materials, visible features, likely symmetry, and genuinely unknown/occluded geometry.
Do not invent hidden details as facts. Put uncertain/hidden areas in unknown_geometry.
The generation_prompt should tell a 3D model generator what to preserve and how to complete unseen surfaces coherently.
The negative_prompt should discourage duplicated parts, broken topology, floating geometry, distorted proportions, text, and artifacts.
"""


class OpenAIVisionService:
    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def enabled(self) -> bool:
        return bool(self.settings.openai_api_key)

    async def analyze(
        self,
        image_bytes: bytes,
        mime_type: str,
        *,
        user_description: str = "",
    ) -> ImageAnalysis:
        if not self.enabled:
            raise RuntimeError("OpenAI is not configured.")

        client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        data_url = (
            f"data:{mime_type};base64,"
            + base64.b64encode(image_bytes).decode("ascii")
        )
        user_text = SYSTEM_PROMPT
        if user_description.strip():
            user_text += (
                "\nThe user also supplied this description. Treat it as guidance, "
                f"not guaranteed visual truth:\n{user_description.strip()}"
            )

        response = await client.responses.create(
            model=self.settings.openai_model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_text},
                        {"type": "input_image", "image_url": data_url},
                    ],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "pixel_forge_image_analysis",
                    "strict": True,
                    "schema": ImageAnalysis.model_json_schema(),
                }
            },
        )

        if not response.output_text:
            raise RuntimeError("OpenAI returned an empty analysis.")

        return ImageAnalysis.model_validate_json(response.output_text)
