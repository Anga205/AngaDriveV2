import reflex as rx
import AngaDriveV2.mydrive, AngaDriveV2.collection_manager, AngaDriveV2.dashboard, AngaDriveV2.flowinity, AngaDriveV2.view_collection
from AngaDriveV2.State import State
import AngaDriveV2.page_not_found as page_not_found
import os, AngaDriveV2.DBMS, AngaDriveV2.common
from fastapi import HTTPException, Response
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse, FileResponse
from fastapi.requests import Request

async def get_file(file_path: str, request: Request):
    AngaDriveV2.DBMS.add_timestamp_to_activity() # add to the homepage graph every time a file is viewed
    if os.path.exists(os.path.join(AngaDriveV2.common.file_directory, file_path)):
        if request.base_url==AngaDriveV2.common.server_config["cache_url"]:
            if not AngaDriveV2.common.file_data[file_path]["cached"]:
                raise HTTPException(status_code=405, detail="URL not allowed")
            else:
                return FileResponse(os.path.join(AngaDriveV2.common.file_directory, file_path), status_code=200)
        else:
            return FileResponse(os.path.join(AngaDriveV2.common.file_directory, file_path), status_code=200)
    raise HTTPException(status_code=404, detail="File not found")
    

async def get_file_preserve_name(obfuscated_file_name: str, actual_file_name:str, request: Request):
    file_path = obfuscated_file_name + (("."+actual_file_name.split(".")[-1]) if "." in actual_file_name else "")   # add back file extension if it was there in the original name
    return await get_file(file_path, request)

async def redirect():
    return RedirectResponse(url = AngaDriveV2.common.app_link)


async def download_file(file_path: str, response: Response):
    full_file_path = os.path.join(os.getcwd(), AngaDriveV2.common.file_directory, file_path)

    if os.path.exists(full_file_path):
        return FileResponse(full_file_path, media_type='application/octet-stream', filename=AngaDriveV2.DBMS.get_file_name(file_path))
    else:
        response.status_code = 404
        return {"error": "File not found"}

# async def backup_download():
#     folder_path = AngaDriveV2.common.app_data_dir_function()
#     zip_filename = os.path.join(folder_path, "backup")
#     if not os.path.exists(folder_path):
#         raise HTTPException(status_code=404, detail="Folder not found")
#     try:
#         os.remove(zip_filename)
#     except:
#         pass

#     try:
#         shutil.make_archive(zip_filename, 'zip', folder_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to create zip file: {str(e)}")
    
#     return FileResponse(zip_filename+".zip", media_type="application/zip", filename="driveBackup.zip")


app = rx.App()
app.add_page(AngaDriveV2.dashboard.index, on_load=State.load_index_page, title="Homepage | DriveV2", route="/")
app.add_page(AngaDriveV2.collection_manager.index, on_load=AngaDriveV2.collection_manager.CollectionState.load_collections_page, title="My Collections | DriveV2", route="/my_collections")
app.add_page(AngaDriveV2.mydrive.index, on_load=State.load_files_page, title="My Files | DriveV2", route="/my_drive")
app.add_page(AngaDriveV2.view_collection.index, on_load=AngaDriveV2.view_collection.ViewCollectionState.load_collection_viewer, title="View Collection | DriveV2", route="/collection")
app.add_custom_404_page(page_not_found.index, title="404 | AngaDrive", on_load=State.load_any_page)
app.api.add_api_route("/i/{file_path}",get_file)
app.api.add_api_route("/i/{obfuscated_file_name}/{actual_file_name}",get_file_preserve_name)
app.api.add_api_route("/download/{file_path}",download_file)
app.add_page(AngaDriveV2.flowinity.verifier, route="/flowinitylogin", on_load=AngaDriveV2.flowinity.VerifierState.load_verifier_page)
app.api.add_api_route("/",redirect)
app.register_lifespan_task(AngaDriveV2.DBMS.lifespan)
# app.api.add_api_route("/backup", backup_download)