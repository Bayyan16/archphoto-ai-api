from dataclasses import dataclass


@dataclass
class PromptPackage:
    positive_prompt: str
    negative_prompt: str
    preservation_instruction: str
    scene_instruction: str
    mood_instruction: str


SCENE_INSTRUCTIONS = {
    "exterior": (
        "Scene type: exterior architecture. Prioritize facade realism, glass reflections, "
        "natural sky, believable sunlight, realistic vegetation, clean roads, and professional "
        "commercial architectural photography."
    ),
    "interior": (
        "Scene type: interior architecture. Prioritize natural window light, realistic material "
        "textures, soft shadows, fabric realism, wood grain, stone detail, and editorial interior photography."
    ),
    "masterplan": (
        "Scene type: masterplan or bird-eye architecture. Prioritize realistic aerial photography, "
        "urban scale, road markings, landscape realism, atmospheric depth, and coherent site composition."
    ),
    "landscape": (
        "Scene type: landscape architecture. Prioritize realistic planting, grass, trees, water, "
        "paving materials, natural lighting, and outdoor environmental atmosphere."
    ),
}


MOOD_INSTRUCTIONS = {
    "daylight": (
        "Mood: clean daylight. Use natural daylight, balanced exposure, soft realistic shadows, "
        "neutral color grading, clean sky, and a premium ArchDaily-style photographic look."
    ),
    "golden-hour": (
        "Mood: golden hour premium. Use warm low-angle sunlight, long soft shadows, realistic "
        "glass highlights, warm exterior lighting, and high-end real estate photography atmosphere."
    ),
    "blue-hour": (
        "Mood: blue hour editorial. Use soft twilight ambience, balanced warm interior lights, "
        "cool exterior atmosphere, realistic reflections, and cinematic architectural photography."
    ),
    "night": (
        "Mood: luxury night. Use realistic artificial lighting, warm interior glow, controlled "
        "contrast, natural reflections, detailed shadows, and premium night architecture photography."
    ),
    "dramatic": (
        "Mood: dramatic editorial. Use stronger contrast, atmospheric depth, cinematic lighting, "
        "but keep the image realistic, professional, and not fantasy or over-stylized."
    ),
}


REALISM_INSTRUCTIONS = {
    "low": (
        "Enhancement strength: subtle. Improve realism gently while keeping the input image very close "
        "to the original render."
    ),
    "medium": (
        "Enhancement strength: balanced. Improve realism, material quality, lighting, and atmosphere "
        "without changing the original design."
    ),
    "high": (
        "Enhancement strength: strong photorealism. Make the image look like professional architecture "
        "photography, while strictly preserving design geometry and camera composition."
    ),
}


GEOMETRY_LOCK_INSTRUCTIONS = {
    "low": (
        "Geometry preservation: low. Minor creative improvements are allowed, but do not change the main "
        "architectural identity."
    ),
    "medium": (
        "Geometry preservation: medium. Preserve camera angle, main massing, facade rhythm, road layout, "
        "and landscape composition. Avoid major design changes."
    ),
    "high": (
        "Geometry preservation: high. Strictly preserve camera angle, building geometry, massing, facade "
        "composition, window positions, roof shape, floor count, road layout, landscape layout, and overall "
        "architectural identity."
    ),
}


def build_preservation_instruction(geometry_lock: str) -> str:
    return GEOMETRY_LOCK_INSTRUCTIONS.get(
        geometry_lock,
        GEOMETRY_LOCK_INSTRUCTIONS["high"],
    )


def build_scene_instruction(scene_type: str) -> str:
    return SCENE_INSTRUCTIONS.get(
        scene_type,
        SCENE_INSTRUCTIONS["exterior"],
    )


def build_mood_instruction(mood: str) -> str:
    return MOOD_INSTRUCTIONS.get(
        mood,
        MOOD_INSTRUCTIONS["daylight"],
    )


def build_realism_instruction(realism_level: str) -> str:
    return REALISM_INSTRUCTIONS.get(
        realism_level,
        REALISM_INSTRUCTIONS["medium"],
    )


def build_negative_prompt() -> str:
    return (
        "changed building design, changed camera angle, changed perspective, distorted architecture, "
        "warped facade, melted geometry, extra floors, missing floors, wrong window positions, "
        "changed roof shape, changed massing, broken road layout, altered landscape layout, fake signage, "
        "unreadable text, cartoon, illustration, anime, fantasy, surreal, plastic materials, over-saturated, "
        "over-sharpened, unrealistic CGI, low quality, blurry, noisy, artifacts, deformed people, "
        "bad reflections, unnatural shadows, inconsistent lighting"
    )


def build_archviz_prompt(
    scene_type: str,
    mood: str,
    realism_level: str,
    geometry_lock: str,
) -> PromptPackage:
    scene_instruction = build_scene_instruction(scene_type)
    mood_instruction = build_mood_instruction(mood)
    realism_instruction = build_realism_instruction(realism_level)
    preservation_instruction = build_preservation_instruction(geometry_lock)

    positive_prompt = (
        "Enhance this raw architectural render into a highly realistic professional architectural photograph. "
        "The output must look like real photography, not CGI and not an artificial render. "
        f"{scene_instruction} "
        f"{mood_instruction} "
        f"{realism_instruction} "
        f"{preservation_instruction} "
        "Improve only lighting quality, material realism, texture detail, glass reflections, realistic shadows, "
        "vegetation realism, sky realism, atmosphere, depth, color grading, exposure, and photographic clarity. "
        "Keep the original design intent, original composition, original camera framing, and architectural identity. "
        "Use natural lens behavior, believable exposure, realistic dynamic range, clean professional color grading, "
        "and premium commercial architecture photography quality."
    )

    return PromptPackage(
        positive_prompt=positive_prompt,
        negative_prompt=build_negative_prompt(),
        preservation_instruction=preservation_instruction,
        scene_instruction=scene_instruction,
        mood_instruction=mood_instruction,
    )
