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

def signup_button():
    return rx.cond(
        State.token,
        rx.chakra.button(
            "Sign Up and merge",
            color_scheme = "purple",
            height="100%"
            ),
        rx.chakra.button(
            "Sign Up",
            color_scheme = "purple",
            height="100%"
            )
    )

def login_button():
    return rx.cond(
        State.token,
        rx.chakra.button(
            "Log in and merge",
            color_scheme="facebook",
            height="100%"
            ),
        rx.chakra.button(
            "Log In",
            color_scheme="facebook",
            height="100%"
            )
    )

def tpu_signup_button():
    return rx.chakra.button(
        rx.chakra.hstack(
            rx.chakra.image(
                src="/TPU-logo.png",
                height="60%",
                width="auto"
                ),
            rx.cond(
                State.token,
                rx.chakra.text("Merge with TPU"),
                rx.chakra.text("Sign up with TPU")
            ),
            height="100%"
        ),
        bg="BLACK",
        color="WHITE",
        height="100%",
        _hover={"bg":"#0f0f1f","color":"#1111cc"}
    )