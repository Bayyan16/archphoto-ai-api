from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.core.config import (
    API_PUBLIC_BASE_URL,
    ALLOWED_IMAGE_TYPES,
    ALLOWED_LOCK_LEVELS,
    ALLOWED_MOODS,
    ALLOWED_REALISM_LEVELS,
    ALLOWED_SCENE_TYPES,
)
from app.services.storage_service import save_upload_file
from app.services.render_service import create_render_job

router = APIRouter()

MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def build_public_url(path: str) -> str:
    normalized_path = path.replace("\\", "/")
    return f"{API_PUBLIC_BASE_URL.rstrip('/')}/{normalized_path}"


def validate_choice(value: str, allowed_values: set[str], field_name: str) -> None:
    if value not in allowed_values:
        raise HTTPException(
            status_code=422,
            detail={
                "status": "error",
                "error_code": "INVALID_RENDER_SETTING",
                "message": f"Invalid {field_name}: {value}",
                "allowed_values": sorted(list(allowed_values)),
            },
        )


@router.post("/enhance")
async def enhance_render(
    image: UploadFile = File(...),
    scene_type: str = Form(...),
    mood: str = Form(...),
    realism_level: str = Form(...),
    geometry_lock: str = Form(...),
    camera_lock: str = Form("high"),
    material_lock: str = Form("high"),
    facade_lock: str = Form("high"),
):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "error_code": "INVALID_FILE_TYPE",
                "message": "Only JPG, PNG, or WEBP images are allowed.",
                "allowed_values": sorted(list(ALLOWED_IMAGE_TYPES)),
            },
        )

    validate_choice(scene_type, ALLOWED_SCENE_TYPES, "scene_type")
    validate_choice(mood, ALLOWED_MOODS, "mood")
    validate_choice(realism_level, ALLOWED_REALISM_LEVELS, "realism_level")
    validate_choice(geometry_lock, ALLOWED_LOCK_LEVELS, "geometry_lock")
    validate_choice(camera_lock, ALLOWED_LOCK_LEVELS, "camera_lock")
    validate_choice(material_lock, ALLOWED_LOCK_LEVELS, "material_lock")
    validate_choice(facade_lock, ALLOWED_LOCK_LEVELS, "facade_lock")

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
        camera_lock=camera_lock,
        material_lock=material_lock,
        facade_lock=facade_lock,
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
            "camera_lock": camera_lock,
            "material_lock": material_lock,
            "facade_lock": facade_lock,
            "engine": render_job["engine"],
            "engine_status": render_job["engine_status"],
            "preservation_mode": {
                "geometry_lock": geometry_lock,
                "camera_lock": camera_lock,
                "material_lock": material_lock,
                "facade_lock": facade_lock,
            },
            "prompt_debug": {
                "positive_prompt": render_job["prompt_package"]["positive_prompt"],
                "negative_prompt": render_job["prompt_package"]["negative_prompt"],
                "preservation_instruction": render_job["prompt_package"]["preservation_instruction"],
                "camera_instruction": render_job["prompt_package"]["camera_instruction"],
                "material_instruction": render_job["prompt_package"]["material_instruction"],
                "facade_instruction": render_job["prompt_package"]["facade_instruction"],
            },
        },
    }
