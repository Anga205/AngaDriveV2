import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State

def static_navbar() -> rx.Component:
    return rx.chakra.hstack(
        rx.chakra.image(src="/logo.png", height="5vh", width="auto"),
        rx.chakra.heading("DriveV2", font_size="2.5vh"),
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
            data_card("Files hosted", State.files_hosted),
            rx.chakra.box(width="1vh"),
            data_card("Registered Accounts", State.registered_accounts),
            rx.chakra.box(width="1vh"),
            data_card("Total Accounts", State.total_accounts),
            width="100%"
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
            data_card("Space Used", State.space_used, width="50%"),
            rx.chakra.box(width="1vh"),
            data_card("Uptime",State.uptime, width = "50%"),
            width="100%"
        ),
        bg="#0f0f1f",
        border_width="1vh",
        border_radius = "1vh",
        border_color="#0f0f1f"
    )



def account_manager():
    return rx.chakra.vstack(
        rx.cond(
            State.is_logged_in,
            rx.chakra.heading("Welcome back!"),
            rx.chakra.vstack(
                rx.chakra.heading(
                    "Welcome to DriveV2",
                    color="#f0fff0",
                    font_size="3.5vh"
                    ),
                rx.chakra.divider(
                    border_color="#f0fff0"
                    ),
                rx.chakra.vstack(
                    rx.chakra.text(
                        "Cant find your data? Try logging into your account: ",
                        color="WHITE",
                        font_size="1.65vh"
                        ),
                    rx.chakra.button_group(
                        login_button(),
                        signup_button(),
                        tpu_signup_button(),
                        is_attached=True,
                        height="4vh"
                    ),
                    rx.chakra.badge(
                        "Any files you upload anonymously will be transferred to your account after you log in",
                        variant="subtle",
                        color_scheme="red"
                    )
                ),
                width="100%"
            )
        ),
        bg="#0f1f0f",
        border_radius="1vh",
        border_width="1vh",
        border_color="#0f1f0f",
        height="30vh",
        width="100%",
    )


def index():
    return rx.chakra.hstack(
        rx.chakra.vstack(
            static_navbar(),
            rx.chakra.hstack(
                rx.chakra.vstack(),
                rx.chakra.vstack(
                    account_manager(),
                    static_data_box(),
                    ),
                spacing="5vh",
                bg="#0f0f0f", 
                width="100%", 
                height="95vh"
            ),
            width="100%",
            spacing="0vh",
            height="100vh",
        ),
        spacing="0vh"
    )
