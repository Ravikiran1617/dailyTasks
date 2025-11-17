from fastapi import FastAPI, File, UploadFile
from validators import validate_file_type, validate_file_size
from utils import save_file

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file with structured validation and saving
    """

    # Step 1: Validate file type
    validate_file_type(file)

    # Step 2: Read and validate file size
    content = await file.read()
    validate_file_size(content)

    # Step 3: Save file
    file_path = save_file(file.filename, content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "saved_to": file_path,
        "message": "File uploaded successfully!"
    }
