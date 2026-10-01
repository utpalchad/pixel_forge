from __future__ import annotations

import asyncio

from google import genai
from google.genai import types

from app.config import Settings
from app.models.schemas import ImageAnalysis
from app.services.vision_openai import SYSTEM_PROMPT


class GeminiVisionService:
    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def enabled(self) -> bool:
        return bool(self.settings.gemini_api_key)

    async def analyze(
        self,
        image_bytes: bytes,
        mime_type: str,
        *,
        user_description: str = "",
    ) -> ImageAnalysis:
        if not self.enabled:
            raise RuntimeError("Gemini is not configured.")

        client = genai.Client(api_key=self.settings.gemini_api_key)
        prompt = SYSTEM_PROMPT
        if user_description.strip():
            prompt += (
                "\nThe user also supplied this description. Treat it as guidance, "
                f"not guaranteed visual truth:\n{user_description.strip()}"
            )

        def _call():
            return client.models.generate_content(
                model=self.settings.gemini_model,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ImageAnalysis,
                    temperature=0.2,
                ),
            )

        response = await asyncio.to_thread(_call)
        if not response.text:
            raise RuntimeError("Gemini returned an empty analysis.")

        return ImageAnalysis.model_validate_json(response.text)
