from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

ASSETS_DIR = "./assets"


@app.get("/i/{file_path:path}")
async def get_file(file_path: str):
    file_location = os.path.join(ASSETS_DIR, file_path)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)
