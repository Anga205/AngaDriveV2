import reflex as rx
from AngaDriveV2.presets import *

def shared_navbar() -> rx.Component:
    return rx.chakra.hstack(
        rx.chakra.box(
            width="0.5vh"
            ),
        rx.chakra.image(
            src="/logo.png", 
            height="5vh", 
            width="auto"
            ),
        rx.chakra.heading(
            "DriveV2", 
            font_size="2.5vh"
            ),
        rx.chakra.spacer(),
        rx.chakra.popover(
            rx.chakra.popover_trigger(
                rx.chakra.icon(
                    tag="bell", 
                    color="WHITE", 
                    font_size="2.5vh"
                    )
                ),
            rx.chakra.popover_content(
                rx.chakra.vstack(
                    rx.chakra.heading(
                        "Notifications", 
                        color="BLUE"
                        ),
                    rx.chakra.divider(border_color="GRAY"),
                    notification(),
                    color="WHITE",
                    bg="BLACK",
                    border_width="1vh",
                    border_radius="0.5vh",
                    border_color="BLACK",
                ),
            ),
        ),
        rx.chakra.box(
            width="0.5vh"
        ),
        color="white",
        height="5vh",
        bg = "black",
        spacing = "1vh",
        width="100%",
    )

def shared_sidebar():
    return rx.chakra.vstack(
        rx.chakra.box(
            height="1vh",
        ),
        height="100vh",
        bg="BLACK"
    )