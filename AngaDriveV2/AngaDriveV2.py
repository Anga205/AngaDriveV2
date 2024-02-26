import reflex as rx
from AngaDriveV2.dashboard import index
from AngaDriveV2.State import State
import AngaDriveV2.page_not_found as page_not_found

# Create app instance and add index page.
app = rx.App()
app.add_page(index, on_load=State.load_index_page, title="Homepage | DriveV2")
app.add_custom_404_page(page_not_found.index, title="404 | AngaDrive", on_load=State.load_any_page)