import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *


def collection_accordian():
    return rx.chakra.text("HELLO WORLD") # TODO:MAKE A CARD FOR COLLECTIONS



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
                            rx.chakra.hstack(
                                rx.chakra.spacer(),
                                rx.chakra.button(
                                    "Create new collection", 
                                    height="60px",
                                    color_scheme="cyan",
                                    opacity="0.3",
                                    _hover={"opacity":"1"}
                                    ),
                                height="0vh",
                                width="100%"
                            ),
                            rx.chakra.vstack(
                                collection_accordian(),
                                width="98%"
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