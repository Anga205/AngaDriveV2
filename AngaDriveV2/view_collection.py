import reflex as rx
from AngaDriveV2.shared_components import *
from AngaDriveV2.State import State


def file_card():
    context_menu_wrapper = (
        lambda component:
        rx.context_menu.root(
            rx.context_menu.trigger(
                component
            ),
            rx.context_menu.content(
                rx.context_menu.item("Copy shortened path"), #on_click=lambda: State.copy_file_path(file_obj)),
                rx.context_menu.item("Copy download link"), #on_click=lambda: State.copy_download_link(file_obj)),
            )
        )
    )
    return context_menu_wrapper(
    rx.chakra.vstack(
        rx.chakra.hstack(
            rx.chakra.spacer(),
            rx.chakra.text(
                "Sample.png", # original file name like sample.png
                font_size="20px",
                color="WHITE"
                ),
            rx.chakra.spacer(),
            bg="#1c1c1c",
            border_radius = "1vh 1vh 0vh 0vh",
            border_color="#1c1c1c",
            border_width="1vh",
            width="100%",
            height="55px"
        ),
        rx.chakra.vstack(
            rx.chakra.box(
                rx.cond(
                    State.true,    # bool value for wether or not item is loadable
                    rx.el.object(
                        data="/document.png", # here we would have file link like https://api.anga.pro/ipuvobew.png
                        fallback=rx.text("failed to load"),
                        opacity="0.7",
                        custom_attrs={"draggable":"false"},
                        height="65%",
                        width="auto",
                    ),
                    rx.chakra.image(
                        src="/document.png",
                        opacity="0.4",
                        custom_attrs={"draggable":"false"}, 
                        height="65%",
                        width="auto"
                    )
                ),
                height="225px",
                display="flex",
                justify_content="center",
                align_items="center",
                width="100%",
                color="WHITE"
            ),
            rx.chakra.hstack(
                rx.chakra.spacer(),
                rx.chakra.vstack(
                    rx.chakra.text(
                        "Uploaded Name:"
                    ),
                    rx.chakra.text(
                        "Timestamp:"
                    ),
                    rx.chakra.text(
                        "File Size:"
                    ),
                    spacing="0vh",
                    justify="start",
                    align_items="start",
                ),
                rx.chakra.vstack(
                    rx.chakra.text(
                        "g08bdiv.png" # file directory like 9487br483.png
                    ),
                    rx.chakra.text(
                        time.ctime(time.time()) # timestamp like time.ctime
                    ),
                    rx.chakra.text(
                        "32KB" # file size like 32KB
                    ),
                    spacing="0vh",
                    justify="start",
                    align_items="start",
                ),
                rx.chakra.spacer(),
                font_size="11px",
                width="100%",
                color="GRAY",
            ),
            rx.chakra.box(
                height="1vh"
            ),
            spacing="0.75vh",
            border_color="#1c1c1c",
            border_width="0.2vh",
            width="100%"
        ),
        rx.chakra.hstack(
            rx.chakra.tooltip(
                rx.chakra.button(
                    rx.chakra.icon(
                        tag="delete"
                    ),
                    color="#ee0000",
                    bg = "#260000",
                    _hover = {"bg":"#420000","color":"#ff0000"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
#                    on_click=State.delete_file(file_obj)
                ),
                label = "Delete"
            ),
            rx.chakra.tooltip(
                rx.chakra.button(
                    rx.chakra.icon(
                        tag="copy"
                    ),
                    color="#00a799",
                    bg = "#002321",
                    _hover = {"bg":"#003432","color":"#11b8aa"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
#                    on_click = lambda: State.copy_file_link(file_obj),
                ),
                label="Copy Link"
            ),
            rx.chakra.tooltip(
                rx.chakra.button(
                    rx.chakra.icon(
                        tag="download"
                    ),
                    color="#12a1fb",
                    bg = "#11222f",
                    _hover = {"bg":"#223340","color":"#22c9bb"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
#                    on_click = State.download_file(file_obj),
                ),
                label="Download File"
            ),
            rx.chakra.tooltip(
                rx.chakra.button(
                    rx.chakra.icon(
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
            spacing="20px",
            width="100%",
            border_color="#1c1c1c",
            border_width="0vh 0.2vh 0.2vh 0.2vh",
            border_radius="0vh 0vh 1vh 1vh"
        ),
        width="290px",
        spacing="0px"
    )
)


def index():
    return rx.chakra.vstack(
        shared_navbar(),
        rx.chakra.hstack(
            rx.chakra.box(
                width = "5px"
            ),
            file_card(),
            rx.chakra.box(
                width = "5px"
            ),
            spacing="0px"
        ),
        rx.chakra.box(
            height="0px"
        ),
        spacing="5px",
        bg = "#0f0f0f",
        height="100vh",
        width="100%"
    )