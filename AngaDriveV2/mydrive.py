import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *


def upload_button():
    return rx.alert_dialog.root(
    rx.alert_dialog.trigger(
        rx.chakra.button(
            rx.chakra.image(
                src="/upload.png",
                height="2vh",
                custom_attrs={"draggable":"false"},
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
                            on_click=State.handle_file_page_upload(rx.upload_files(upload_id="file_page_upload", on_upload_progress=State.upload_progressbar))
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



def desktop_index():
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
            rx.chakra.hstack(
                rx.chakra.box(
                    width="5vh", 
                    height="0vh"
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
                spacing="0vh",
            ),
            bg="#0f0f0f",
            width="100%"
        )
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index()
        ),
        rx.mobile_and_tablet(
            view_under_construction()
        ),
        width="100%",
    )