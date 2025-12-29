import shutil
import os
import uuid
from fastapi import UploadFile, HTTPException
from pathlib import Path

# valid extensions
SUPPORTED_EXTENSIONS = {".wav", ".mp3"}

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {ext}. Supported: {SUPPORTED_EXTENSIONS}"
        )

def save_upload_file_tmp(upload_file: UploadFile) -> str:
    try:
        tmp_dir = Path("/tmp/whisper_uploads")
        tmp_dir.mkdir(parents=True, exist_ok=True)

        file_ext = os.path.splitext(upload_file.filename)[1]
        unique_name = f"{uuid.uuid4()}{file_ext}"
        file_path = tmp_dir / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

def delete_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temp file: {file_path}")
    except Exception as e:
        print(f"Error deleting temp file {file_path}: {e}")