import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *


def static_data_box() -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.heading(
            "DriveV2 - Site Data",
            color="#f0f0ff",
            font_size="3.5vh"
            ),
        rx.chakra.divider(
            border_color="GRAY"
            ),
        rx.chakra.hstack(
            site_data_card(
                "Files hosted", 
                State.files_hosted,
                height="100%"
                ),
            site_data_card(
                "Registered Accounts", 
                State.registered_accounts,
                height="100%"
                ),
            site_data_card(
                "Total Accounts", 
                State.total_accounts,
                height="100%"
                ),
            width="100%",
            height="100%",
            spacing="0.75vh",
        ),
        card(
            "Site activity over past week",
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key="times_opened",
                    stroke = "#0000ff",
                    fill = "#0000ff",
                ),
                rx.recharts.x_axis(data_key="date"),
                rx.recharts.y_axis(),
                rx.recharts.cartesian_grid(stroke_dasharray="1 1"),
                rx.recharts.graphing_tooltip(),
                data=State.site_activity,
                color="BLACK",
            ),
            width = "100%",
            height="250%"
        ),
        rx.chakra.box(
            rx.moment(
                interval=1000, 
                on_change=State.increment_time
                ), 
            display="none"
            ),
        rx.chakra.flex(
            site_data_card("Space Used", State.space_used, width="50%", height="100%"),
            rx.chakra.box(width="1vh"),
            site_data_card("Uptime",State.uptime, width = "50%", height="100%"),
            width="100%",
            height="100%"
        ),
        bg="#0f0f1f",
        border_width="1vh",
        border_radius = "1vh",
        border_color="#0f0f1f",
        spacing="0.75vh",
        height="250%",
    )

def login_button_group() -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.hstack(
            rx.chakra.button(
                "Sign Up",
                height="100%",
                width="55%",
                font_size="1.4vh",
                bg="#0f1f0f",
                color="white",
                border_radius="1vh 0vh 0vh 0vh",
                _hover={"bg":"#0f1f0f","color":"#11cc11"}
            ),
            rx.chakra.button(
                "Login",
                height="100%",
                width="45%",
                bg="#1f0f0f",
                color="WHITE",
                font_size="1.4vh",
                border_radius="0vh 1vh 0vh 0vh",
                _hover={"bg":"#1f0f0f","color":"#cc1111"}
            ),
            height="50%",
            spacing="0vh",
            width="100%"
        ),
        tpu_signup_button(
            height="50%",
            width="100%",
            font_size="1.4vh",
            border_radius="0vh 0vh 1vh 1vh"
        ),
        height="100%",
        spacing="0vh",
        width="40%",
    )

def account_manager(logged_in : bool = False):
    if not logged_in:
        return rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.heading(
                    "You are anonymous!",
                    color="WHITE",
                    font_size="4vh"
                ),
                rx.chakra.image(
                    src = "/anonymous.png",
                    height="10vh",
                    border_radius="5vh",
                    border="0.2vh solid WHITE",
                    width="auto",
                ),
                spacing="0.75vh"
            ),
            rx.chakra.divider(
                border_color="GRAY"
            ),
            rx.chakra.hstack(
                login_button_group(),
                rx.chakra.vstack(
                    rx.chakra.heading(
                        "No account was found",
                        font_size="1.65vh"
                        ),
                    rx.chakra.vstack(
                        rx.chakra.text(
                            "But don't worry!, all the core features should still work the same,",
                            ),
                        rx.chakra.text(
                            "just remember that without an account, you wont be able to",
                            ),
                        rx.chakra.text(
                            "modify or delete uploaded files from other devices and/or browsers",
                        ),
                        spacing="0vh",
                        font_size="1.2vh",
                    ),
                    color="WHITE",
                    border_color="#111111",
                    border_radius="1vh",
                    border_width="1vh",
                    width="100%",
                    bg="#111111",
                    height="100%",
                    spacing="0.75vh"
                ),
                width="100%",
                height="100%"
            ),
            bg = "BLACK",
            spacing="0.75vh",
            height="100%",
            width="100%",
            border_color="BLACK",
            border_radius="1vh",
            border_width="0.75vh"
        )


def static_account_info():
    background_color = "#0f1f0f"
    return rx.chakra.vstack(
        rx.chakra.heading(
            "My Account",
            color="WHITE",
            font_size="3.5vh"
            ),
        rx.chakra.divider(
            border_color="#f0fff0"
            ),
        rx.chakra.hstack(
            rx.chakra.vstack(
                user_data_card(
                    "Your files",
                    State.user_file_count,
                    width="100%",
                    height="100%"
                ),
                user_data_card(
                    "Your Storage",
                    State.user_storage_amount,
                    width="21.5vh",
                    height="100%"
                ),
                height="100%",
                spacing="0.75vh"
            ),
            account_manager(),
            width="100%",
            height="100%",
            spacing="0.75vh"
        ),
        bg=background_color,
        border_color=background_color,
        height="100%",
        width="100%",
        spacing="0.75vh",
        border_radius="1vh",
        border_width="1vh"
    )

def index():
    return rx.chakra.hstack(
        rx.chakra.vstack(
            shared_navbar(),
            rx.chakra.hstack(
                shared_sidebar(),
                rx.chakra.vstack(
                    static_account_info(),
                    static_data_box(),
                    height="98%",
                    spacing="0.75vh",
                    ),
                spacing="5vh", 
                width="99%", 
                height="95vh",
                bg="#0f0f0f"
            ),
            width="100%",
            spacing="0vh",
            bg="#0f0f0f",
            height="100vh",
        ),
        spacing="0vh"
    )
