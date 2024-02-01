"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
from AngaDriveV2.static_pages import index
from AngaDriveV2.DBMS import *


# Create app instance and add index page.
app = rx.App()
app.add_page(index)
