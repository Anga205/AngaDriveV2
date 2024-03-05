import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *


def collection_accordian():
    card_color="#1c1c1c"
    return rx.chakra.box(
        rx.chakra.accordion(
            rx.chakra.accordion_item(
                rx.chakra.accordion_button(
                    rx.chakra.vstack(
                        rx.chakra.hstack(
                            rx.chakra.text(
                                "Collection1 name",
                                font_size="30px"
                            ),
                            rx.chakra.accordion_icon(),
                        ),
                        rx.chakra.divider(
                            border_color="GRAY"
                        ),
                        rx.chakra.box(
                            height="10px"
                        ),
                        rx.chakra.hstack(
                            rx.chakra.vstack(
                                rx.chakra.text("File Count: "),
                                rx.chakra.text("Total Size: "),
                                rx.chakra.text("Editors: "),
                                spacing="5px",
                                align_items="start"
                            ),
                            rx.chakra.vstack(
                                rx.chakra.text("72"),
                                rx.chakra.text("1.2 GB"),
                                rx.chakra.text("12"),
                                spacing="5px",
                                align_items="start",
                            ),
                            font_size="15px",
                            color="#bbbbbb",
                            spacing="10px"
                        ),
                        spacing="0vh"
                    )
                ),
                rx.chakra.accordion_panel(
                    rx.chakra.hstack(
                        rx.chakra.tooltip(
                            rx.chakra.button(
                                rx.chakra.icon(
                                    tag="edit",
                                    font_size="20px"
                                ),
                                height="30px",
                                width="40px",
                                border_radius="15px",
                                bg="rgb(0, 75, 75)",
                                color="rgb(0, 200, 200)",
                                _hover={"bg":"rgb(0, 100, 100)", "color": "rgb(0, 255, 255)"}
                            ),
                            label="Edit Files"
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.tooltip(
                            rx.chakra.button(
                                rx.chakra.icon(
                                    tag="delete",
                                    font_size="20px"
                                ),
                                height="30px",
                                width="40px",
                                border_radius="15px",
                                bg="rgb(75, 0, 0)",
                                color="rgb(200, 0, 0)",
                                _hover={"bg":"rgb(100, 0, 0)", "color": "rgb(255, 0, 0)"}
                            ),
                            label="Delete Collection"
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.tooltip(
                            rx.chakra.button(
                                rx.chakra.icon(
                                    tag="copy",
                                    font_size="20px"
                                ),
                                height="30px",
                                width="40px",
                                border_radius="15px",
                                bg="rgb(75, 0, 75)",
                                color="rgb(200, 0, 200)",
                                _hover={"bg":"rgb(100, 100, 0)", "color": "rgb(255, 255, 0)"}
                            ),
                            label="Share Collection"
                        ),
                        width="100%"
                    )
                )
            ),
            allow_toggle=True,
            border_color=card_color
        ),
        bg=card_color,
        border_color=card_color,
        border_radius="5px",
        border_width="5px"
    )



def index():
    return site_template(
        "Collections",
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.tabs(
                    rx.chakra.tab_list(
                        rx.chakra.tab("My Collections"),
                        rx.chakra.tab("Shared with me"),
                    ),
                    rx.chakra.tab_panels(
                        rx.chakra.tab_panel(
                            rx.chakra.box(
                                height="2vh"
                                ),
                            rx.chakra.wrap(
                                collection_accordian(),
                                width="100%"
                            ),
                            spacing="0vh"
                        ),
                        rx.chakra.tab_panel(
                            rx.chakra.text("test2")
                        ),
                    ),
                    color="WHITE",
                    width="100%",
                    variant="line",
                    color_scheme="cyan",
                    height="100%",
                    is_fitted=True
                ),
                width="100%",
                height="100%",
            ),
            width="100%",
            height="100%"
        )
    )