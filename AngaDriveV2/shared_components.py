import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
from AngaDriveV2.common import *


class SystemHealthState(State):
    show_system_heath:bool = False

    _n_tasks:int = 0
    @rx.background
    async def tick_health(self, date):
        async with self:
            if self._n_tasks>0:
                return
            if self.show_system_heath==False:
                return
            self._n_tasks+=1
        async with self:
            self.uptime = format_time(round(time.time() - self.local_start_time))
            system_info = get_system_info()
            self.temperature = system_info["temperature"]
            self.ram_usage = system_info["ram_usage_percentage"]
            self.cpu_usage = system_info["cpu_usage"]
            self._n_tasks-=1

    def open_system_health(self):
        self.show_system_heath = True
    
    def close_system_health_no_params(self):
        self.show_system_heath = False

    def close_system_health(self, junk=False):
        self.close_system_health_no_params()

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
                width="auto",
                on_click=rx.redirect("/")
                ),
            rx.chakra.heading(
                "DriveV2", 
                font_size="2.5vh",
                on_click=rx.redirect("/")
                ),
            rx.chakra.spacer(),
            rx.popover.root(
                rx.popover.trigger(
                    rx.chakra.image(
                        src="/health.png",
                        custom_attrs={"draggable":"false"},
                        color="WHITE", 
                        height="2vh",
                        on_click = SystemHealthState.open_system_health
                        )
                    ),
                rx.popover.content(
                    rx.chakra.vstack(
                        rx.chakra.heading(
                            "System Health", 
                            color="RED",
                            font_size="3.5vh"
                            ),
                        rx.chakra.divider(border_color="GRAY"),
                        rx.chakra.box(
                            rx.moment(
                                interval=500, 
                                on_change=SystemHealthState.tick_health
                            ), 
                            display="none"
                        ),
                        rx.chakra.box(
                            rx.chakra.heading(
                                rx.chakra.span(
                                    "Uptime: ",
                                    color="rgb(0, 100, 100)"
                                ),
                                rx.chakra.span(
                                    State.uptime,
                                    color="WHITE"
                                ),
                                font_size="2vh",
                            ),
                            rx.chakra.heading(
                                rx.chakra.span(
                                    "Temperature: ",
                                    color="rgb(0, 100, 100)"
                                ),
                                rx.chakra.span(
                                    State.temperature,
                                    color="WHITE"
                                ),
                                font_size="2vh",
                            ),
                            rx.chakra.hstack(
                                rx.chakra.circular_progress(
                                    rx.chakra.circular_progress_label("RAM"),
                                    value=State.ram_usage,
                                    size="10vh"
                                ),
                                rx.chakra.circular_progress(
                                    rx.chakra.circular_progress_label("CPU"),
                                    value=State.cpu_usage,
                                    size="10vh"
                                )
                            ),
                            border_radius="0.5vh",
                            width="100%"
                        ),
                        color="WHITE",
                        bg="BLACK",
                        border_width="0px",
                        border_radius="0.5vh",
                        border_color="BLACK",
                    ),
                    bg="BLACK",
                    border_color="WHITE",
                    border_width="1px",
                    on_escape_key_down = SystemHealthState.close_system_health,
                    on_pointer_down_outside= SystemHealthState.close_system_health,
                    on_focus_outside= SystemHealthState.close_system_health,
                    on_interact_outside=SystemHealthState.close_system_health,
                ),
                open = SystemHealthState.show_system_heath,
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
    buttons = ["Home", "Files", "Collections"]
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