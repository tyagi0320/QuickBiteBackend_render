import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return filename
