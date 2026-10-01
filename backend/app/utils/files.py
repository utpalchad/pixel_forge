import io
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.config import Settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MIME_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


async def read_validated_image(upload: UploadFile, max_upload_mb: int) -> tuple[bytes, str]:
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Only JPG, PNG, and WebP images are supported.",
        )

    data = await upload.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    max_bytes = max_upload_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Image exceeds the {max_upload_mb} MB upload limit.",
        )

    try:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Invalid image file.") from exc

    return data, upload.content_type or "image/jpeg"


def save_public_source_image(
    data: bytes,
    mime_type: str,
    settings: Settings,
) -> str:
    """Persist a reference image under /files so external 3D providers can fetch it."""
    ext = MIME_EXTENSIONS.get(mime_type, ".jpg")
    source_dir: Path = settings.output_path / "sources"
    source_dir.mkdir(parents=True, exist_ok=True)

    filename = f"source-{uuid4().hex}{ext}"
    path = source_dir / filename
    path.write_bytes(data)

    base = settings.public_base_url.rstrip("/")
    return f"{base}/files/sources/{filename}"
