import os
import uuid
from dataclasses import asdict
from typing import Dict

from PIL import Image, ImageEnhance, ImageFilter

from app.services.prompt_builder import PromptPackage

OUTPUT_DIR = "storage/outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def _apply_basic_photographic_enhancement(
    image: Image.Image,
    mood: str,
    realism_level: str,
) -> Image.Image:
    """
    Temporary local image enhancement.

    This is not the final AI engine.
    It keeps backend-output flow stable until a real image-to-image AI provider is integrated.
    """

    image = ImageEnhance.Sharpness(image).enhance(1.22)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(1.04)

    if mood == "golden-hour":
        image = ImageEnhance.Color(image).enhance(1.12)
        image = ImageEnhance.Contrast(image).enhance(1.06)
        image = ImageEnhance.Brightness(image).enhance(1.03)

    if mood == "blue-hour":
        image = ImageEnhance.Contrast(image).enhance(1.1)
        image = ImageEnhance.Brightness(image).enhance(0.96)

    if mood == "night":
        image = ImageEnhance.Brightness(image).enhance(0.82)
        image = ImageEnhance.Contrast(image).enhance(1.15)
        image = ImageEnhance.Color(image).enhance(1.08)

    if mood == "dramatic":
        image = ImageEnhance.Contrast(image).enhance(1.18)
        image = ImageEnhance.Sharpness(image).enhance(1.12)

    if realism_level == "high":
        image = image.filter(ImageFilter.SHARPEN)
        image = ImageEnhance.Contrast(image).enhance(1.06)

    if realism_level == "low":
        image = ImageEnhance.Contrast(image).enhance(0.98)

    return image


def enhance_image_with_ai_engine(
    input_path: str,
    prompt_package: PromptPackage,
    scene_type: str,
    mood: str,
    realism_level: str,
    geometry_lock: str,
    camera_lock: str,
    material_lock: str,
    facade_lock: str,
) -> Dict[str, object]:
    """
    AI engine boundary.

    Current mode:
    - Uses Pillow as a temporary local mock enhancer.

    Future mode:
    - Replace the internals of this function with image-to-image AI API calls.
    - Keep the function signature and return format stable so the route/frontend do not break.
    """

    image = Image.open(input_path).convert("RGB")

    enhanced_image = _apply_basic_photographic_enhancement(
        image=image,
        mood=mood,
        realism_level=realism_level,
    )

    output_filename = f"{uuid.uuid4()}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    enhanced_image.save(output_path, quality=95)

    return {
        "output_path": output_path.replace("\\", "/"),
        "engine": "local-pillow-mock",
        "engine_status": "mock_ready_for_ai_provider",
        "prompt_package": asdict(prompt_package),
        "settings": {
            "scene_type": scene_type,
            "mood": mood,
            "realism_level": realism_level,
            "geometry_lock": geometry_lock,
            "camera_lock": camera_lock,
            "material_lock": material_lock,
            "facade_lock": facade_lock,
        },
    }
