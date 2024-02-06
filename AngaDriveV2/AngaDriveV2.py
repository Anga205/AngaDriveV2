import reflex as rx
from AngaDriveV2.static_pages import index
from AngaDriveV2.State import State


# Create app instance and add index page.
app = rx.App()
app.add_page(index, on_load=State.load_index_page)