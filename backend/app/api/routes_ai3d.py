import asyncio

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.models.schemas import JobResponse, VisionProvider
from app.services.cloudinary_service import CloudinaryService
from app.services.jobs import job_store
from app.services.threews import ThreeWSService
from app.services.vision_router import VisionRouter
from app.utils.files import read_validated_image

router = APIRouter(prefix="/ai3d", tags=["ai-3d"])


@router.post("/generate", response_model=JobResponse)
async def generate_ai_3d(
    files: list[UploadFile] = File(...),
    vision_provider: VisionProvider = Form(VisionProvider.auto),
    description: str = Form(""),
    tier: str = Form("draft"),
    analyze_image: bool = Form(True),
):
    settings = get_settings()

    if not 1 <= len(files) <= 6:
        raise HTTPException(status_code=422, detail="Upload between 1 and 6 image views.")

    if tier not in {"draft", "standard", "high"}:
        raise HTTPException(
            status_code=422,
            detail="tier must be draft, standard, or high.",
        )

    cloudinary_service = CloudinaryService(settings)
    if not cloudinary_service.enabled:
        raise HTTPException(
            status_code=503,
            detail=(
                "Cloudinary is required for AI 3D generation because the external "
                "reconstruction service needs public reference-image URLs."
            ),
        )

    validated: list[tuple[bytes, str, str]] = []
    for upload in files:
        data, mime = await read_validated_image(upload, settings.max_upload_mb)
        validated.append((data, mime, upload.filename or "view"))

    generation_prompt = description.strip()
    if analyze_image:
        vision = VisionRouter(settings)
        try:
            _, analysis = await vision.analyze(
                validated[0][0],
                validated[0][1],
                provider=vision_provider,
                user_description=description,
            )
            generation_prompt = analysis.generation_prompt
            if analysis.negative_prompt:
                generation_prompt += (
                    "\nAvoid: " + analysis.negative_prompt
                )
        except Exception as exc:
            if not generation_prompt:
                raise HTTPException(
                    status_code=502,
                    detail=f"Image analysis failed and no manual description was supplied: {exc}",
                ) from exc

    try:
        source_urls = await asyncio.gather(
            *[
                cloudinary_service.upload_image(data, filename_hint=filename.rsplit(".", 1)[0])
                for data, _, filename in validated
            ]
        )
        threews = ThreeWSService(settings)
        submitted = await threews.submit(
            source_urls,
            prompt=generation_prompt,
            tier=tier,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI 3D submission failed: {exc}") from exc

    normalized_status = submitted.status.lower()
    if submitted.glb_url or normalized_status == "done":
        status = "done"
    elif normalized_status == "failed":
        status = "failed"
    else:
        status = "queued"

    record = job_store.create(
        provider="three.ws",
        prompt=generation_prompt,
        remote_job_id=submitted.job_id,
        status=status,
        glb_url=str(submitted.glb_url) if submitted.glb_url else None,
        viewer_url=(
            str(submitted.viewer_url)
            if submitted.viewer_url
            else (
                threews.viewer_url_for(str(submitted.glb_url))
                if submitted.glb_url
                else None
            )
        ),
    )
    if status == "failed":
        job_store.update(record.id, error="The external 3D provider reported a failure.")

    return job_store.response(record)
