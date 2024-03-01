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
            font_size="1.65vh",
            height="4vh",
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
        rx.hstack(
            rx.spacer(),
            rx.text(
                "Filename",
                font_size="2.5vh",
                color="WHITE"
                ),
            rx.spacer(),
            bg="#1c1c1c",
            border_radius = "1vh 1vh 0vh 0vh",
            border_color="#1c1c1c",
            border_width="1vh",
            width="100%"
        ),
        rx.vstack(
            rx.box(
                rx.image(
                    src="/document.png",
                    opacity="0.4",
                    height="65%",
                    width="auto"
                ),
                height="30vh",
                display="flex",
                justify_content="center",
                align_items="center",
                width="100%",
                color="WHITE"
            ),
            rx.hstack(
                rx.spacer(),
                rx.vstack(
                    rx.text(
                        "Uploaded Name:"
                    ),
                    rx.text(
                        "Timestamp:"
                    ),
                    rx.text(
                        "File Size:"
                    ),
                    spacing="0vh",
                    justify="start",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text(
                        "bgtr783nc8n5i.png"
                    ),
                    rx.text(
                        f"{time.ctime(time.time())}"
                    ),
                    rx.text(
                        "48.42 GB"
                    ),
                    spacing="0vh",
                    justify="start",
                    align_items="start",
                ),
                rx.spacer(),
                font_size="1.5vh",
                width="100%",
                color="GRAY",
                spacing="0.75vh"
            ),
            rx.box(
                height="1vh"
            ),
            spacing="0.75vh",
            border_color="#1c1c1c",
            border_width="0.2vh",
            width="100%"
        ),
        rx.hstack(
            rx.button(
                rx.icon(
                    tag="delete"
                ),
                color="#ee0000",
                bg = "#260000",
                _hover = {"bg":"#420000","color":"#ff0000"},
                border_radius="2vh",
                height="4.5vh",
                width="15%",
                font_size="1.65vh"
                ),
            rx.button(
                rx.icon(
                    tag="copy"
                ),
                color="#00a799",
                bg = "#002321",
                _hover = {"bg":"#003432","color":"#11b8aa"},
                border_radius="2vh",
                height="4.5vh",
                width="15%",
                font_size="1.65vh"
            ),
            rx.button(
                rx.icon(
                    tag="download"
                ),
                color="#12a1fb",
                bg = "#11222f",
                _hover = {"bg":"#223340","color":"#22c9bb"},
                border_radius="2vh",
                height="4.5vh",
                width="5vh",
                font_size="1.65vh"
            ),
            rx.button(
                rx.icon(
                    tag="plus_square",
                    width="5vh"
                ),
                color="#ffb100",
                bg = "#302400",
                _hover = {"bg":"#413511","color":"#ffc200"},
                border_radius="2vh",
                height="4.5vh",
                width="5vh",
                font_size="1.65vh"
            ),
            justify_content="center",
            align_items="center",
            height="6vh",
            spacing="5%",
            width="100%",
            border_color="#1c1c1c",
            border_width="0vh 0.2vh 0.2vh 0.2vh",
            border_radius="0vh 0vh 1vh 1vh"
        ),
        width="18%",
        spacing="0vh"
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