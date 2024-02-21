import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State

def static_navbar() -> rx.Component:
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
        color="white",
        height="5vh",
        bg = "black",
        spacing = "1vh",
        width="100%",
    )


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
        rx.chakra.flex(
            site_data_card("Files hosted", State.files_hosted),
            rx.chakra.box(width="1vh"),
            site_data_card("Registered Accounts", State.registered_accounts),
            rx.chakra.box(width="1vh"),
            site_data_card("Total Accounts", State.total_accounts),
            width="100%",
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
            height="30vh"
        ),
        rx.chakra.box(
            rx.moment(
                interval=1000, 
                on_change=State.increment_time
                ), 
            display="none"
            ),
        rx.chakra.flex(
            site_data_card("Space Used", State.space_used, width="50%"),
            rx.chakra.box(width="1vh"),
            site_data_card("Uptime",State.uptime, width = "50%"),
            width="100%"
        ),
        bg="#0f0f1f",
        border_width="1vh",
        border_radius = "1vh",
        border_color="#0f0f1f",
        spacing="0.75vh",
        height="100%"
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
                rx.chakra.card(
                    rx.chakra.text("but dont worry!, all the core features should still work the same, just remember that without an account, you wont be able to modify or delete uploaded files from other devices and/or browsers"),
                    header="No account was found",
                )
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
            static_navbar(),
            rx.chakra.hstack(
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
