from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os, AngaDriveV2.DBMS

app = FastAPI()
ASSETS_DIR = "./assets"

@app.get("/i/{file_path:path}")
async def get_file(file_path: str):
    AngaDriveV2.DBMS.add_timestamp_to_activity() # add to the homepage graph every time a file is viewed
    if not os.path.exists(os.path.join(ASSETS_DIR, file_path)):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(os.path.join(ASSETS_DIR, file_path))
