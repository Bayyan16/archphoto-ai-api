import os

API_PUBLIC_BASE_URL = os.getenv("API_PUBLIC_BASE_URL", "http://localhost:8000")

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

ALLOWED_SCENE_TYPES = {
    "exterior",
    "interior",
    "masterplan",
    "landscape",
}

ALLOWED_MOODS = {
    "daylight",
    "golden-hour",
    "blue-hour",
    "night",
    "dramatic",
}

ALLOWED_REALISM_LEVELS = {
    "low",
    "medium",
    "high",
}

ALLOWED_LOCK_LEVELS = {
    "low",
    "medium",
    "high",
}
