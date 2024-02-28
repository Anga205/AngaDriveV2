import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *

def index():
    return upload_container(
        rx.chakra.hstack(
            shared_sidebar(opened_page="Files"),
            rx.chakra.vstack(
                shared_navbar(),
                rx.chakra.spacer(),
                spacing="0.75vh",
                height="100vh",
                width="100%",
                bg="#0f0f0f"
            ),  
            spacing="0vh",
            height="100vh",
            width="100%"
        )
    )