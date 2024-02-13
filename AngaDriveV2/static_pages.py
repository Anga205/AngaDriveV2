import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State


def static_data_box() -> rx.Component:
    return rx.vstack(
        rx.flex(
            data_card("Files hosted", State.files_hosted),
            rx.box(width="1vh"),
            data_card("Registered Accounts", State.registered_accounts),
            rx.box(width="1vh"),
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
        rx.box(
            rx.moment(
                interval=1000, 
                on_change=State.increment_time
                ), 
            display="none"
            ),
        rx.flex(
            data_card("Space Used", State.space_used, width="50%"),
            rx.box(width="1vh"),
            data_card("Uptime",State.uptime, width = "50%"),
            width="100%"
        ),
        bg="#0f0f1f",
        border_width="1vh",
        border_radius = "1vh",
        border_color="#0f0f1f"
    )



def index():
    return rx.hstack(
        rx.vstack(
            "hello world",
            height="100vh",
            bg="black",
            width="12%",
        ),
        rx.vstack(
            rx.hstack(
                rx.image(src="/logo.png", height="5vh", width="auto"),
                rx.heading("AngaDriveV2", font_size="2.5vh"),
                rx.spacer(),
                rx.popover(
                    rx.popover_trigger(
                        rx.icon(
                            tag="bell", 
                            color="WHITE", 
                            font_size="2.5vh"
                            )
                        ),
                    rx.popover_content(
                        rx.vstack(
                            rx.heading(
                                "Notifications", 
                                color="BLUE"
                                ),
                            rx.divider(border_color="GRAY"),
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
                spacing = "0vh",
                width="100%",
            ),
            rx.hstack(
                rx.vstack(),
                static_data_box(),
                spacing="5vh",
                bg="#0f0f0f", 
                width="100%", 
                height="95vh"
            ),
            width="88%",
            spacing="0vh",
            height="100vh",
        ),
        spacing="0vh"
    )
