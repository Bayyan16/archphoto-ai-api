from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.storage_service import save_upload_file
from app.services.render_service import create_render_job

router = APIRouter()

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def build_public_url(path: str) -> str:
    normalized_path = path.replace("\\", "/")
    return f"http://localhost:8000/{normalized_path}"


@router.post("/enhance")
async def enhance_render(
    image: UploadFile = File(...),
    scene_type: str = Form(...),
    mood: str = Form(...),
    realism_level: str = Form(...),
    geometry_lock: str = Form(...),
):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "error_code": "INVALID_FILE_TYPE",
                "message": "Only JPG, PNG, or WEBP images are allowed.",
            },
        )

    file_bytes = await image.read()

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail={
                "status": "error",
                "error_code": "FILE_TOO_LARGE",
                "message": f"Maximum file size is {MAX_FILE_SIZE_MB}MB.",
            },
        )

    await image.seek(0)
    upload_path = await save_upload_file(image)

    render_job = create_render_job(
        input_path=upload_path,
        scene_type=scene_type,
        mood=mood,
        realism_level=realism_level,
        geometry_lock=geometry_lock,
    )

    original_url = build_public_url(render_job["original_path"])
    output_url = build_public_url(render_job["output_path"])

    return {
        "status": "success",
        "message": "Render enhanced successfully.",
        "data": {
            "job_id": render_job["job_id"],
            "job_status": render_job["status"],
            "original_url": original_url,
            "output_url": output_url,
            "scene_type": scene_type,
            "mood": mood,
            "realism_level": realism_level,
            "geometry_lock": geometry_lock,
            "engine": render_job["engine"],
            "engine_status": render_job["engine_status"],
            "preservation_mode": geometry_lock,
            "prompt_debug": {
                "positive_prompt": render_job["prompt_package"]["positive_prompt"],
                "negative_prompt": render_job["prompt_package"]["negative_prompt"],
                "preservation_instruction": render_job["prompt_package"]["preservation_instruction"],
            },
        },
    }
