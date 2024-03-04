import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *

def index():
    return site_template(
        "Collections",
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.text("Lorem Ipsum dolor")
            ),
            width="100%",
            height="100%"
        )
    )