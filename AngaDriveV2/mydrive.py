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
            width="10vh",
            border_radius="1vh",
            _hover={"bg":"#0000aa"}
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(
                "Upload Files"
                ),
            rx.alert_dialog.description(
                rx.upload(
                    rx.cond(
                        rx.selected_files("file_page_upload"),
                        rx.chakra.vstack(
                            rx.chakra.box(
                                height="5vh"
                                ),
                            rx.foreach(
                                rx.selected_files("file_page_upload"),
                                rx.chakra.text
                                ),
                            rx.chakra.box(
                                height="5vh"
                                )
                            ),
                        rx.chakra.vstack(
                            rx.spacer(),
                            rx.chakra.text("Drag and drop files here or click to select files"),
                            rx.spacer(),
                            height="15vh"
                            ),
                    ),
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
                        _hover={"bg":"#000033"},
                        on_click=rx.clear_selected_files("file_page_upload")
                        )
                    ),
                rx.spacer(),
                rx.cond(
                    rx.selected_files("file_page_upload"),
                    rx.alert_dialog.cancel(
                        rx.chakra.button(
                            "Upload",
                            bg="#113322",
                            color="WHITE",
                            _hover={"bg":"#224433"},
                            on_click=State.handle_file_page_upload(rx.upload_files(upload_id="file_page_upload"))
                        )
                    ),
                    rx.box(
                        width="0px", 
                        height="0px"
                        ),
                ),
                width="100%"
                ),
            bg="#111111",
            color="WHITE"
            ),
        )

def file_card(file_obj):
    rx = reflex.chakra
    return rx.vstack(
        rx.hstack(
            rx.spacer(),
            rx.text(
                file_obj[0], # original file name like sample.png
                font_size="23px",
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
                height="225px",
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
                        file_obj[1] # file directory like 9487br483.png
                    ),
                    rx.text(
                        file_obj[3] # timestamp like time.ctime
                    ),
                    rx.text(
                        file_obj[2] # file size like 32KB
                    ),
                    spacing="0vh",
                    justify="start",
                    align_items="start",
                ),
                rx.spacer(),
                font_size="11px",
                width="100%",
                color="GRAY",
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
            rx.tooltip(
                rx.button(
                    rx.icon(
                        tag="delete"
                    ),
                    color="#ee0000",
                    bg = "#260000",
                    _hover = {"bg":"#420000","color":"#ff0000"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
                    on_click=State.delete_file(file_obj)
                ),
                label = "Delete"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon(
                        tag="copy"
                    ),
                    color="#00a799",
                    bg = "#002321",
                    _hover = {"bg":"#003432","color":"#11b8aa"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
                    on_click = lambda: State.copy_file_link(file_obj),
                ),
                label="Copy Link"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon(
                        tag="download"
                    ),
                    color="#12a1fb",
                    bg = "#11222f",
                    _hover = {"bg":"#223340","color":"#22c9bb"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
                    on_click = State.download_file(file_obj),
                ),
                label="Download File"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon(
                        tag="plus_square",
                        width="5vh"
                    ),
                    color="#ffb100",
                    bg = "#302400",
                    _hover = {"bg":"#413511","color":"#ffc200"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
                ),
                label="Add to collection"
            ),
            justify_content="center",
            align_items="center",
            height="42px",
            spacing="15px",
            width="100%",
            border_color="#1c1c1c",
            border_width="0vh 0.2vh 0.2vh 0.2vh",
            border_radius="0vh 0vh 1vh 1vh"
        ),
        width="225px",
        spacing="0px"
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
            rx.cond(
                State.user_files,
                rx.chakra.wrap(
                    rx.foreach(
                        State.user_files,
                        file_card
                    ),
                ),
                rx.chakra.vstack(
                    rx.chakra.spacer(),
                    rx.chakra.alert(
                        rx.chakra.alert_icon(),
                        rx.chakra.alert(
                            "Drag and drop files here, of click the 'Upload' button on the top right", 
                            bg="#000033", 
                            color="WHITE"
                        ),
                        border_radius="2vh",
                        bg="#000033",
                        border_color="#0000aa",
                        border_width="0.2vh"
                    ),
                    rx.chakra.spacer(),
                    height="50vh",
                )
            ),
            bg="#0f0f0f",
            width="100%"
        )
    )