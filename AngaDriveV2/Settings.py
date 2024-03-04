import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *

def index():
    return site_template(
        "Settings",
        rx.text("hello world!")
    )