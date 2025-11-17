from fastapi import HTTPException
from config import ALLOWED_TYPES, MAX_FILE_SIZE


def validate_file_type(file):
    """Check if file type is allowed"""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed types: {ALLOWED_TYPES}"
        )


def validate_file_size(content):
    """Check if file size does not exceed limit"""
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large! Maximum allowed size is {MAX_FILE_SIZE / (1024 * 1024)} MB"
        )
