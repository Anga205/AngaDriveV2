import reflex as rx
import AngaDriveV2.mydrive, AngaDriveV2.Settings, AngaDriveV2.collections, AngaDriveV2.dashboard
from AngaDriveV2.State import State
import AngaDriveV2.page_not_found as page_not_found
import os, AngaDriveV2.DBMS, AngaDriveV2.common
from fastapi import HTTPException
from fastapi.responses import FileResponse

async def get_file(file_path: str):
    AngaDriveV2.DBMS.add_timestamp_to_activity() # add to the homepage graph every time a file is viewed
    if not os.path.exists(os.path.join(AngaDriveV2.common.file_directory, file_path)):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(os.path.join(AngaDriveV2.common.file_directory, file_path))


# Create app instance and add index page.
app = rx.App()
app.add_page(AngaDriveV2.dashboard.index, on_load=State.load_index_page, title="Homepage | DriveV2", route="/")
app.add_page(AngaDriveV2.collections.index, on_load=State.load_any_page, title="My Collections | DriveV2", route="/my_collections")
app.add_page(AngaDriveV2.mydrive.index, on_load=State.load_files_page, title="My Files | DriveV2", route="/my_drive")
app.add_page(AngaDriveV2.Settings.index, on_load=State.load_any_page, title="Settings | DriveV2", route="/my_settings")
app.add_custom_404_page(page_not_found.index, title="404 | AngaDrive", on_load=State.load_any_page)
app.api.add_api_route("/i/{file_path:path}",get_file)