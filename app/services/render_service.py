import os
import uuid
from PIL import Image, ImageEnhance, ImageFilter

OUTPUT_DIR = "storage/outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def enhance_render_mock(
    input_path: str,
    scene_type: str,
    mood: str,
    realism_level: str,
    geometry_lock: str,
) -> str:
    image = Image.open(input_path).convert("RGB")

    image = ImageEnhance.Sharpness(image).enhance(1.25)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(1.04)

    if mood == "golden-hour":
        image = ImageEnhance.Color(image).enhance(1.12)
        image = ImageEnhance.Contrast(image).enhance(1.06)

    if mood == "night":
        image = ImageEnhance.Brightness(image).enhance(0.82)
        image = ImageEnhance.Contrast(image).enhance(1.15)

    if realism_level == "high":
        image = image.filter(ImageFilter.SHARPEN)

    output_filename = f"{uuid.uuid4()}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    image.save(output_path, quality=95)

    return output_path.replace("\\", "/")