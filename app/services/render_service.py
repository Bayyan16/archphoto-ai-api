import uuid
from typing import Dict

from app.services.ai_service import enhance_image_with_ai_engine
from app.services.prompt_builder import build_archviz_prompt


def create_render_job(
    input_path: str,
    scene_type: str,
    mood: str,
    realism_level: str,
    geometry_lock: str,
) -> Dict[str, object]:
    """
    Main render orchestration service.

    Flow:
    1. Create job_id
    2. Build archviz prompt package
    3. Send image + prompt package to AI service boundary
    4. Return normalized job result
    """

    job_id = f"render_{uuid.uuid4().hex}"

    prompt_package = build_archviz_prompt(
        scene_type=scene_type,
        mood=mood,
        realism_level=realism_level,
        geometry_lock=geometry_lock,
    )

    ai_result = enhance_image_with_ai_engine(
        input_path=input_path,
        prompt_package=prompt_package,
        scene_type=scene_type,
        mood=mood,
        realism_level=realism_level,
        geometry_lock=geometry_lock,
    )

    return {
        "job_id": job_id,
        "status": "completed",
        "original_path": input_path.replace("\\", "/"),
        "output_path": ai_result["output_path"],
        "engine": ai_result["engine"],
        "engine_status": ai_result["engine_status"],
        "settings": ai_result["settings"],
        "prompt_package": ai_result["prompt_package"],
    }
