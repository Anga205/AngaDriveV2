import reflex as rx
import time
from AngaDriveV2.library import time_ago

def card(heading, content, **kwargs):
    return rx.vstack(
        rx.heading(heading, color="BLUE", font_size="3vh"),
        content,
        border_color="black",
        border_width="1.5vh",
        border_radius="0.5vh",
        align="center",
        color="WHITE",
        bg="BLACK",
        **kwargs
    )

def data_card(heading = "Sample heading", content="Sample content", **kwargs):
    return card(
        heading, 
        rx.text(content, font_size="2.5vh", _as="b"),
        **kwargs
    )

def notification(heading = "New notification", description = "An error occured displaying this notification", timestamp = time.time()-3600, *content):
    return rx.box(
        rx.vstack(
            rx.heading(heading, font_size="2vh", color="#eeeeff"),
            rx.text(description, font_size="1.65vh", color="#bbbbcc"),
            rx.hstack(
                rx.spacer(),
                rx.text(
                    time_ago(timestamp), 
                    color="GRAY", 
                    font_size="1.4vh"
                    ),
                width="100%"
            ),
            border_width="0.3vh",
            border_radius="0.3vh",
            border_color="#101020",
            bg="#101020"
        ),
    )