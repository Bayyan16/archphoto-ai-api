from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.storage_service import save_upload_file
from app.services.render_service import enhance_render_mock

router = APIRouter()


@router.post("/enhance")
async def enhance_render(
    image: UploadFile = File(...),
    scene_type: str = Form(...),
    mood: str = Form(...),
    realism_level: str = Form(...),
    geometry_lock: str = Form(...),
):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, or WEBP images are allowed.",
        )

    upload_path = await save_upload_file(image)

    output_path = enhance_render_mock(
        input_path=upload_path,
        scene_type=scene_type,
        mood=mood,
        realism_level=realism_level,
        geometry_lock=geometry_lock,
    )

    return {
        "status": "success",
        "message": "Render enhanced successfully.",
        "data": {
            "original_url": f"http://localhost:8000/{upload_path}",
            "output_url": f"http://localhost:8000/{output_path}",
            "scene_type": scene_type,
            "mood": mood,
            "realism_level": realism_level,
            "geometry_lock": geometry_lock,
        },
    }