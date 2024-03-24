import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State

def shared_navbar() -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.hstack(
            rx.chakra.box(
                width="0.5vh"
                ),
            rx.chakra.image(
                src="/logo.png", 
                height="5vh", 
                custom_attrs={"draggable":"false"},
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
            height="4.9vh",
            bg = "black",
            spacing = "1vh",
            width="100%",
        ),
        rx.chakra.progress(
            value = State.upload_progress,
            width = "100%",
            bg="BLACK"
        ),
        bg="BLACK",
        height="5vh",
        width="100%",
        spacing="0vh"
    )

def shared_sidebar(opened_page, **kwargs):
    buttons = ["Home", "Files", "Settings", "Collections"]
    button_bg = "BLACK"
    selected_button_bg = "#1f1f1f"

    button_colors = {name:button_bg for name in buttons}
    button_colors[opened_page] = selected_button_bg

    def sidebar_button(image, text, redirect_to = "/404"):
        button_on_hover = {"bg": "#101010"}

        return rx.chakra.button(
                rx.chakra.image(
                    src=image,
                    height="60%",
                    custom_attrs={"draggable":"false"},
                    width="auto"
                ),
                rx.chakra.box(
                    width="1vh"
                ),
                rx.chakra.text(
                    text
                ),
                rx.chakra.spacer(),
                width="100%",
                height="5vh",
                spacing="0vh",
                font_size="1.65vh",
                border_radius="0vh",
                on_click=rx.redirect(redirect_to),
                bg=button_colors[text],
                color="WHITE",
                _hover=button_on_hover
                )
    

    return rx.chakra.vstack(
        rx.chakra.box(
            width="0vh",
            height="2vh"
        ),
        sidebar_button(
            "/home.png",
            "Home",
            "/"
        ),
        sidebar_button(
            "/folders.png",
            "Files",
            "/my_drive"
        ),
        sidebar_button(
            "/collection.png",
            "Collections",
            "/my_collections"
        ),
        sidebar_button(
            "/gears.png",
            "Settings",
            "/my_settings"
        ),
        height="100%",
        width="12%",
        spacing="0vh",
        position="fixed",
        bg="BLACK",
        **kwargs
    )

def upload_container(component):
    upload_handler_spec = State.handle_upload(
        rx.upload_files(
            upload_id="upload1",
            on_upload_progress=State.upload_progressbar
        ),
    )
    return rx.upload(
        component,
        rx.moment(
            interval=rx.cond(
                rx.selected_files("upload1") & ~State.is_uploading,
                500,
                0,
            ),
            on_change=lambda _: upload_handler_spec,
            display="none",
        ),
        width="100%",
        spacing="0vh",
        id="upload1",
        no_click=True,
        no_keyboard=True
    )

def site_template(page_opened, components=rx.spacer()):
    return upload_container(
        rx.chakra.hstack(
            shared_sidebar(opened_page=page_opened),
            rx.chakra.box(width="12%"),
            rx.chakra.vstack(
                shared_navbar(),
                components,
                spacing="0.75vh",
                height="100vh",
                width="88%",
                bg="#0f0f0f"
            ),  
            bg="#0f0f0f",
            spacing="0vh",
            height="100vh",
            width="100%"
        )
    )