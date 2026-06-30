import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "storage/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_upload_file(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1].lower()
    safe_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return file_path.replace("\\", "/")
