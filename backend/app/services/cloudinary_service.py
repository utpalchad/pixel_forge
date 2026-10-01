from __future__ import annotations

import asyncio
from uuid import uuid4

import cloudinary
import cloudinary.uploader
import cloudinary.utils

from app.config import Settings


class CloudinaryService:
    def __init__(self, settings: Settings):
        self.settings = settings
        if settings.cloudinary_enabled:
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True,
            )

    @property
    def enabled(self) -> bool:
        return self.settings.cloudinary_enabled

    async def upload_image(self, data: bytes, *, filename_hint: str = "image") -> str:
        if not self.enabled:
            raise RuntimeError("Cloudinary is not configured.")

        def _upload() -> dict:
            return cloudinary.uploader.upload(
                data,
                folder="pixel-forge/source-images",
                public_id=f"{filename_hint}-{uuid4().hex}",
                overwrite=False,
                resource_type="image",
            )

        result = await asyncio.to_thread(_upload)
        public_id = result["public_id"]

        transformed_url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            secure=True,
            transformation=[
                {
                    "width": 1024,
                    "height": 1024,
                    "crop": "limit",
                    "quality": "auto:good",
                    "fetch_format": "auto",
                }
            ],
        )
        return transformed_url
