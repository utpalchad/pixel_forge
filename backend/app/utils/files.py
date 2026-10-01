import io

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


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
