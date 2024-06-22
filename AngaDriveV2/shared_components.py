import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
from AngaDriveV2.common import *


class SystemHealthState(State):
    show_system_health:bool = False

    _n_tasks:int = 0
    @rx.background
    async def tick_health(self, date):
        async with self:
            if self._n_tasks>0:
                return
            if self.load_system_health_checker==False:
                return
            self._n_tasks+=1
        async with self:
            self.uptime = format_time(round(time.time() - self.local_start_time))
            system_info = get_system_info()
            self.ram_usage = system_info["ram_usage_percentage"]
            self.cpu_usage = system_info["cpu_usage"]
            self.temperature_available = on_rpi
            self.temperature = system_info["temperature"]
            self._n_tasks-=1

    load_system_health_checker:bool =False
    def open_system_health(self):
        self.show_system_health = True
        self.load_system_health_checker = True
    
    def close_system_health_no_params(self):
        self.show_system_health = False
        self.load_system_health_checker = False

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
                            rx.cond(
                                State.temperature_available,
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
                                empty_component()
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
                open = SystemHealthState.show_system_health,
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
        on_drop=upload_handler_spec,
        width="100%",
        spacing="0vh",
        padding="0px",
        border="solid 0px #000000",
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


def file_name_header(file_obj, **kwargs):
    return rx.chakra.hstack(
        rx.chakra.spacer(),
        rx.chakra.tooltip(
            rx.text(
                file_obj["truncated_name"], # truncated original file name like sample.png
                font_size="20px",
                color="WHITE"
            ),
            label=file_obj["original_name"]
        ),
        rx.chakra.spacer(),
        bg="#1c1c1c",
        border_color="#1c1c1c",
        border_width="1vh",
        width="100%",
        height="55px",
        **kwargs
    )

def file_details(file_obj, **kwargs):
    return rx.chakra.vstack(
        rx.chakra.box(
            rx.cond(
                file_obj["previewable"],
                rx.el.object(
                    data=file_obj["file_link"],
                    fallback=rx.text("failed to load"),
                    opacity="0.7",
                    custom_attrs={"draggable":"false"},
                    height="65%",
                    width="auto",
                ),
                rx.chakra.image(
                    src="/document.png",
                    opacity="0.4",
                    custom_attrs={"draggable":"false"}, 
                    height="65%",
                    width="auto"
                )
            ),
            height="225px",
            display="flex",
            justify_content="center",
            align_items="center",
            overflow="hidden",
            width="100%",
            color="WHITE"
        ),
        rx.chakra.hstack(
            rx.chakra.spacer(),
            rx.chakra.vstack(
                rx.chakra.text(
                    "Uploaded Name:"
                ),
                rx.chakra.text(
                    "Timestamp:"
                ),
                rx.chakra.text(
                    "File Size:"
                ),
                spacing="0vh",
                justify="start",
                align_items="start",
            ),
            rx.chakra.vstack(
                rx.chakra.text(
                    file_obj["file_path"] # file directory like 9487br483.png
                ),
                rx.chakra.text(
                    file_obj["timestamp"] # timestamp like time.ctime
                ),
                rx.chakra.text(
                    file_obj["size"] # file size like 32KB
                ),
                spacing="0vh",
                justify="start",
                align_items="start",
            ),
            rx.chakra.spacer(),
            font_size="11px",
            width="100%",
            color="GRAY",
        ),
        rx.chakra.box(
            height="1vh"
        ),
        spacing="0.75vh",
        border_color="#1c1c1c",
        border_width="0.2vh",
        width="100%",
        **kwargs
    )

def file_editor_menu(file_obj, **kwargs):
    return rx.chakra.hstack(
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.icon(
                    tag="delete"
                ),
                color="#ee0000",
                bg = "#260000",
                _hover = {"bg":"#420000","color":"#ff0000"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click=State.delete_file(file_obj)
            ),
            label = "Delete"
        ),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.icon(
                    tag="copy"
                ),
                color="#00a799",
                bg = "#002321",
                _hover = {"bg":"#003432","color":"#11b8aa"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click = lambda: State.copy_file_link(file_obj),
            ),
            label="Copy Link"
        ),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.icon(
                    tag="download"
                ),
                color="#12a1fb",
                bg = "#11222f",
                _hover = {"bg":"#223340","color":"#22c9bb"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click = State.download_file(file_obj),
            ),
            label="Download File"
        ),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.image(
                    src="/eye.png",
                    width="100%",
                    height="auto",
                    custom_attrs={"draggable":"false"}
                ),
                color="#ffb100",
                bg = "#302400",
                _hover = {"bg":"#413511","color":"#ffc200"},
                border_radius="2vh",
                height="30px",
                width="17%",
                on_click=rx.redirect(file_obj["file_link"], external=True)
            ),
            label="View file"
        ),
        justify_content="center",
        align_items="center",
        height="42px",
        spacing="20px",
        width="100%",
        border_color="#1c1c1c",
        **kwargs,
    ),


file_card_context_menu_wrapper = (
        lambda component, file_obj:
        rx.context_menu.root(
            rx.context_menu.trigger(
                component
            ),
            rx.context_menu.content(
                rx.context_menu.item("Copy shortened path", on_click=lambda: State.copy_file_path(file_obj)),
                rx.context_menu.item("Copy download link", on_click=lambda: State.copy_download_link(file_obj)),
            )
        )
    )

def file_card(file_obj):
    return file_card_context_menu_wrapper(
    rx.chakra.vstack(
        file_name_header(
            file_obj,
            border_radius="1vh 1vh 0vh 0vh"
        ),
        file_details(
            file_obj,
            border_radius="0vh 0vh 0vh 0vh"
        ),
        file_editor_menu(
            file_obj,
            border_width="0vh 0.2vh 0.2vh 0.2vh",
            border_radius= "0vh 0vh 1vh 1vh"
        ),
        width="290px",
        spacing="0px"
    ),
    file_obj
)

def conditional_render(condition, true_component):
    return rx.cond(
        condition,
        true_component,
        rx.chakra.box(
            display="none",
            width="0px",
            height="0px"
        )
    )

def view_under_construction():
    return rx.vstack(
        rx.spacer(),
        rx.heading("Mobile view is not supported (yet)", size="9"),
        rx.spacer(),
        height="100vh",
        width="100%"
    )

def empty_component(width="0px", height="0px"):
    return rx.box(
        width=width,
        height=height,
    )