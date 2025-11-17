import os
from config import UPLOAD_DIR


def save_file(filename: str, content: bytes):
    """Save file to the uploads directory"""

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path
