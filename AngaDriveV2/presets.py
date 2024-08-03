import reflex as rx
from AngaDriveV2.flowinity import client_secret

def card(heading, content, **kwargs):
    return rx.chakra.vstack(
        rx.chakra.heading(heading, color="BLUE", font_size="3vh"),
        rx.spacer(),
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

def tpu_signup_button(**kwargs):
    return rx.chakra.button(
        rx.chakra.hstack(
            rx.chakra.image(
                src="/flowinity.svg",
                custom_attrs={"draggable":"false"},
                height="2vh",
                width="auto",
                ),
            rx.chakra.text("Flowinity Oauth"),
            font_size="1.75vh",
            height="100%"
        ),
        bg="rgb(20, 10, 30)",
        color="WHITE",
        on_click=rx.redirect(f"https://privateuploader.com/oauth/{client_secret}"),
        _hover={"bg":"#0f0f1f","color":"#1111cc"},
        **kwargs
    )