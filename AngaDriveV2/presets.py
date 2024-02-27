import reflex as rx
import time
from AngaDriveV2.library import time_ago
from AngaDriveV2.State import State

def card(heading, content, **kwargs):
    return rx.chakra.vstack(
        rx.chakra.heading(heading, color="BLUE", font_size="3vh"),
        content,
        border_color="black",
        border_width="1.5vh",
        border_radius="0.5vh",
        align="center",
        color="WHITE",
        spacing="0.75vh",
        bg="BLACK",
        **kwargs
    )

def site_data_card(heading = "Sample heading", content="Sample content", **kwargs):
    return card(
        heading, 
        rx.chakra.text(content, font_size="2.5vh", _as="b"),
        **kwargs
    )

def user_data_card(heading = "Sample heading", content="Sample content", **kwargs):
    return rx.chakra.vstack(
        rx.chakra.heading(heading, color="GREEN", font_size="3vh"),
        rx.chakra.text(content, font_size="2.5vh", _as="b"),
        border_color="black",
        border_width="1.5vh",
        border_radius="0.5vh",
        spacing="0.75vh",
        align="center",
        color="WHITE",
        bg="BLACK",
        **kwargs
    )

def notification(heading = "New notification", description = "An error occured displaying this notification", timestamp = time.time()-3600, *content):
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.heading(heading, font_size="2vh", color="#eeeeff"),
            rx.chakra.text(description, font_size="1.65vh", color="#bbbbcc"),
            rx.chakra.hstack(
                rx.chakra.spacer(),
                rx.chakra.text(
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

def tpu_signup_button(**kwargs):
    return rx.chakra.button(
        rx.chakra.hstack(
            rx.chakra.image(
                src="/flowinity.svg",
                height="2vh",
                width="auto"
                ),
            rx.chakra.text("Flowinity Oauth"),
            height="100%"
        ),
        bg="rgb(20, 10, 30)",
        color="WHITE",
        on_click=rx.redirect("/tpulogin"),
        _hover={"bg":"#0f0f1f","color":"#1111cc"},
        **kwargs
    )