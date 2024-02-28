import reflex as rx
import reflex #importing it twice because my dumbass forgot reflex defaults to radix instead of chakra, i later on redefined reflex.chakra as rx inside a function
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *


def upload_button():
    return rx.alert_dialog.root(
    rx.alert_dialog.trigger(
        rx.chakra.button(
            rx.chakra.image(
                src="/upload.png",
                height="2vh",
                width="auto"
                ),
            "Upload",
            color="WHITE",
            bg="#000055",
            _hover={"bg":"#0000aa"}
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(
                "Upload Files"
                ),
            rx.alert_dialog.description(
                rx.upload(
                    rx.chakra.text(
                        "Drag and drop files here or click to select files"
                        ),
                    height="20vh",
                    display='flex',
                    justify_content= 'center',
                    align_items= 'center',
                    border="1px dotted #0000ff",
                    id="file_page_upload"
                    )
                ),
            rx.chakra.box(
                height="1vh"
                ),
            rx.chakra.hstack(
                rx.alert_dialog.cancel(
                    rx.chakra.button(
                        "Close",
                        bg="#440000",
                        color="WHITE",
                        _hover={"bg":"#000033"}
                        )
                    ),
                rx.spacer(),
                width="100%"
                ),
            bg="#111111",
            color="WHITE"
            ),
        )

def file_card():
    rx = reflex.chakra
    return rx.vstack(
        rx.heading(
            "TODO: CODE A CARD TO DISPLAY FILES"
            )
    )



def index():
    return site_template(
        "Files",
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.vstack(
                    rx.chakra.heading(
                        "My Files",
                        color="WHITE",
                        font_size="3.5vh"
                    ),
                    rx.chakra.spacer(),
                    spacing="0vh",
                    height="100%"
                ),
                rx.chakra.spacer(),
                rx.chakra.vstack(
                    rx.chakra.spacer(),
                    upload_button(),
                    spacing="0vh",
                    height="100%"
                    ),
                width="98%",
                height="8vh"
            ),
            file_card(),
            height="100%",
            width="100%"
        )
    )