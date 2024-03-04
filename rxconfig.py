import reflex as rx
import subprocess


fastapi_startup_command = [
    "uvicorn", 
    "file_handler.main:app", 
    "--host", "0.0.0.0", 
    "--port", 
    "5000"
    ]

#subprocess.Popen(fastapi_startup_command)


config = rx.Config(
    app_name="AngaDriveV2",
)