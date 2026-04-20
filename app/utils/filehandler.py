# import os
# from uuid import uuid4
# from fastapi import UploadFile

# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# def save_file(file: UploadFile) -> str:
#     ext = file.filename.split(".")[-1]
#     filename = f"{uuid4()}.{ext}"
#     file_path = os.path.join(UPLOAD_DIR, filename)

#     with open(file_path, "wb") as f:
#         f.write(file.file.read())

#     return filename

import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

# These will be provided by your Cloudinary Dashboard
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

def save_file(file: UploadFile) -> str:
    """
    Takes the uploaded file, sends it to Cloudinary,
    and returns the permanent URL.
    """
    try:
        # We upload directly to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file.file, 
            folder="quickbite_items"
        )
        # This URL is what you will store in your Postgres 'image_url' column
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload failed: {e}")
        return ""

