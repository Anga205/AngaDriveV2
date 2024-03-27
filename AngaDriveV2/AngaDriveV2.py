import reflex as rx
import AngaDriveV2.mydrive, AngaDriveV2.collection_manager, AngaDriveV2.dashboard, AngaDriveV2.flowinity
from AngaDriveV2.State import State
import AngaDriveV2.page_not_found as page_not_found
import os, AngaDriveV2.DBMS, AngaDriveV2.common
from fastapi import HTTPException, Response, File
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse, FileResponse

async def get_file(file_path: str):
    AngaDriveV2.DBMS.add_timestamp_to_activity() # add to the homepage graph every time a file is viewed
    if not os.path.exists(os.path.join(AngaDriveV2.common.file_directory, file_path)):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(os.path.join(AngaDriveV2.common.file_directory, file_path))

async def get_file_preserve_name(obfuscated_file_name: str, actual_file_name:str):
    AngaDriveV2.DBMS.add_timestamp_to_activity() # add to the homepage graph every time a file is viewed
    file_path = obfuscated_file_name + (("."+actual_file_name.split(".")[-1]) if "." in actual_file_name else "")   # add back file extension if it was there in the original name
    if not os.path.exists(os.path.join(AngaDriveV2.common.file_directory, file_path)):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(os.path.join(AngaDriveV2.common.file_directory, file_path))


async def redirect():
    return RedirectResponse(url = AngaDriveV2.common.app_link)


async def download_file(file_path: str, response: Response):
    full_file_path = os.path.join(os.getcwd(), AngaDriveV2.common.file_directory, file_path)
    print(full_file_path, AngaDriveV2.DBMS.get_file_name(file_path))
    print(os.path.exists(full_file_path))

    if os.path.exists(full_file_path):
        return FileResponse(full_file_path, media_type='application/octet-stream', filename=AngaDriveV2.DBMS.get_file_name(file_path))
    else:
        response.status_code = 404
        return {"error": "File not found"}


app = rx.App()
app.add_page(AngaDriveV2.dashboard.index, on_load=State.load_index_page, title="Homepage | DriveV2", route="/")
app.add_page(AngaDriveV2.collection_manager.index, on_load=State.load_any_page, title="My Collections | DriveV2", route="/my_collections")
app.add_page(AngaDriveV2.mydrive.index, on_load=State.load_files_page, title="My Files | DriveV2", route="/my_drive")
app.add_custom_404_page(page_not_found.index, title="404 | AngaDrive", on_load=State.load_any_page)
app.api.add_api_route("/i/{file_path}",get_file)
app.api.add_api_route("/i/{obfuscated_file_name}/{actual_file_name}",get_file_preserve_name)
app.api.add_api_route("/download/{file_path}",download_file)
app.add_page(AngaDriveV2.flowinity.verifier, route="/flowinitylogin", on_load=AngaDriveV2.flowinity.VerifierState.load_verifier_page)
app.api.add_api_route("/",redirect)