import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
from AngaDriveV2.common import *
from AngaDriveV2.login_dialog import login_dialog, LoginState
import reflex_chakra as rx_chakra


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
            self.ram_percent = system_info["ram_usage_percentage"]
            self.total_ram = system_info["total_ram"]
            self.used_ram = system_info["used_ram"]
            self.cpu_usage = round(sum(system_info["cpu_usage"])/len(system_info["cpu_usage"])) or random.randint(2, 10)
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

def shared_navbar(**kwargs) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                width="0.5vh"
            ),
            rx.image(
                src="/logo.png", 
                height="5vh", 
                custom_attrs={"draggable":"false"},
                width="auto",
                on_click=rx.redirect("/"),
                _hover={"opacity":"0.5"}
            ),
            rx.heading(
                "DriveV2", 
                font_size="2.5vh",
                on_click=rx.redirect("/")
            ),
            rx.spacer(),
            rx.popover.root(
                rx.popover.trigger(
                    rx.icon(
                        "settings",
                        _hover={"color":"#777777"},
                        color="WHITE",
                        height="2.5vh"
                    )
                ),
                rx.popover.content(
                    rx.vstack(
                        rx.heading(
                            "Drive Settings"
                        ),
                        rx.divider(
                            color_scheme="gray",
                        ),
                        rx.hstack(
                            rx.text(
                                "Enable File Previews"
                            ),
                            rx.switch(
                                checked=State.enable_previews,
                                on_click=State.swap_previews
                            ),
                            align="center"
                        ),
                        width="100%",
                        spacing="1"
                    ),
                    bg="BLACK",
                )
            ),
            rx.box(
                width="0.5vh"
            ),
            color="white",
            height="4.9vh",
            bg = "black",
            spacing = "1vh",
            width="100%",
            align="center",
            justify="center"
        ),
        rx.progress(
            value = State.upload_progress,
            width = "100%",
            bg="BLACK"
        ),
        bg="BLACK",
        height="5vh",
        width="100%",
        spacing="0vh",
        **kwargs
    )

class AccountManagerState(State):

    new_username:str
    new_email:str
    account_update_password:str
    account_update_password_confirm:str
    display_password_inputs:bool = False
    dialog_bool:bool = False

    def open_dialog(self):
        self.new_username = self.username
        self.new_email = self.email
        self.display_password_inputs = False
        self.dialog_bool = True
        self.account_update_password = ""
        self.account_update_password_confirm = ""
    
    def close_dialog(self):
        self.dialog_bool = False
    
    def update_dialog(self):
        if (self.new_username != self.username) or (self.new_email != self.email):
            self.display_password_inputs = True
        else:
            self.display_password_inputs = False
    
    def account_manager_logout(self):
        self.logout()
        self.close_dialog()

    def set_new_username(self, new_username: str):
        new_username = new_username.strip()
        new_username = new_username[:30]
        new_username = new_username.replace(" ", "_")
        self.new_username = new_username # strip and truncate to 30 characters
        self.update_dialog()
        


def account_manager_wrapper(component, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(component),
        rx.dialog.content(
            rx.dialog.title("Account Manager"),
            rx.vstack(
                rx.input(
                    value=AccountManagerState.new_username,
                    on_change=AccountManagerState.set_new_username,
                    placeholder="Enter username here",
                    width="100%"
                ),
                rx.input(
                    value=AccountManagerState.new_email,
                    on_change=AccountManagerState.set_new_email,
                    placeholder="Enter email here",
                    width="100%"
                ),
                rx.hstack(
                    rx.button(
                        rx.icon(
                            "log-out",
                            height="60%"
                        ),
                        "Log out",
                        color_scheme="orange",
                        variant="soft",
                        on_click=AccountManagerState.account_manager_logout
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon(
                            "trash-2",
                            height="60%"
                        ),
                        "Delete Account",
                        color_scheme="red",
                        variant="soft",
                    ),
                    width="100%"
                ),
                width="100%"
            ),
            bg="#0f0f0f",
            on_escape_key_down=lambda _: AccountManagerState.close_dialog(),
            on_pointer_down_outside=lambda _: AccountManagerState.close_dialog(),
        ),
        open=AccountManagerState.dialog_bool,
    )



def sidebar_login_widget():
    return rx.vstack(
        rx.hstack(
            login_dialog(
                rx.button(
                    "Login",
                    style={"font-weight":"bold"},
                    color_scheme="blue",
                    variant="soft",
                    width="100%",
                    font_size="1.75vh",
                    on_click=LoginState.set_to_login_mode,
                    height="4vh",
                    border="1vh",
                    border_radius="0.5vh"
                ),
                width="49%",
            ),
            rx.spacer(),
            login_dialog(
                rx.button(
                    "Signup",
                    style={"font-weight":"bold"},
                    color_scheme="green",
                    variant="soft",
                    width="100%",
                    on_click=LoginState.set_to_signup_mode,
                    font_size="1.75vh",
                    height="4vh",
                    border="1vh",
                    border_radius="0.5vh"
                ),
                width="49%"
            ),
            spacing="0px",
            width="100%"
        ),
        tpu_signup_button(
            width="100%",
            height="4vh",
            border_radius="0.5vh",
        ),
        spacing="5px",
        width="100%",
    )

def sidebar_account_widget():
    return account_manager_wrapper(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    "user",
                    height="100%",
                    width="auto",
                    padding="3px"
                ),
                rx.vstack(
                    rx.text(
                        State.username,
                        font_size="1.8vh",
                        padding="0"
                    ),
                    rx.text(
                        State.email,
                        color="GRAY",
                        width="100%",
                        font_size="1.3vh",
                        padding="0"
                    ),
                    spacing="0",
                    overflow="hidden"
                ),
                width="100%",
                height="40px",
                spacing="0vh",
                font_size="1.65vh",
                border_radius="0vh",
                color="WHITE",
                align="center",
                padding="5px",
                _hover={"color":"#e0e0e0","bg":"#1f1f1f"},
                on_click=AccountManagerState.open_dialog
            )
        )
    )


def shared_sidebar(opened_page, **kwargs):
    buttons = ["Home", "Files", "Collections", "GitHub"]
    button_bg = "BLACK"
    selected_button_bg = "#1f1f1f"

    button_colors = {name:button_bg for name in buttons}
    button_colors[opened_page] = selected_button_bg

    def sidebar_button(icon_tag, text, redirect_to = "/404"):
        button_on_hover = {"bg": "#101010"}

        return rx.button(
                rx.icon(
                    tag=icon_tag,
                    height="60%",
                    width="auto"
                ),
                rx.text(
                    text
                ),
                rx.spacer(),
                width="100%",
                height="5vh",
                spacing="0vh",
                font_size="1.65vh",
                border_radius="0vh",
                font_weight="bold",
                on_click=rx.redirect(redirect_to),
                bg=button_colors[text],
                color="WHITE",
                _hover=button_on_hover
            )


    return rx.vstack(
        rx.box(
            width="0vh",
            height="2vh"
        ),
        sidebar_button(
            "Home",
            "Home",
            "/"
        ),
        sidebar_button(
            "File",
            "Files",
            "/my_drive"
        ),
        sidebar_button(
            "Folder",
            "Collections",
            "/my_collections"
        ),
        rx.link(
            sidebar_button(
                "github",
                "GitHub",
                ""
            ),
            width="100%",
            href="https://github.com/Anga205/AngaDriveV2",
            target="_blank"
        ),
        rx.spacer(),
        rx.box(
            rx.cond(
                State.is_logged_in,
                sidebar_account_widget(),
                sidebar_login_widget(),
            ),
            width="100%",
            padding="5px"
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
        rx.hstack(
            shared_sidebar(opened_page=page_opened),
            rx.box(width="12%"),
            rx.vstack(
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
    return rx.hstack(
        rx.tooltip(
            rx.text(
                file_obj["truncated_name"], # truncated original file name like sample.png
                font_size="20px",
                color="WHITE",
                font_weight="bold",
            ),
            content=file_obj["original_name"]
        ),
        align="center",
        justify="center",
        bg="#1c1c1c",
        border_color="#1c1c1c",
        border_width="1px",
        width="100%",
        height="55px",
        **kwargs
    )

def file_details(file_obj, **kwargs):
    return rx.vstack(
        rx.box(
            rx.cond(
                file_obj["previewable"] & State.enable_previews,
                rx.el.object(
                    data=file_obj["file_link"],
                    fallback=rx.text("failed to load"),
                    opacity="0.7",
                    loading="lazy",
                    custom_attrs={"draggable":"false"},
                    style={"max-height":"65%","max-width":"100%"}
                ),
                rx.icon(
                    tag="file-text",
                    opacity="0.4",
                    custom_attrs={"draggable":"false"}, 
                    height="65%",
                    width="auto",
                    stroke_width=0.75
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
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Uploaded Name:"
                ),
                rx.text(
                    "Timestamp:"
                ),
                rx.text(
                    "File Size:"
                ),
                spacing="0px",
                justify="start",
                align_items="start",
            ),
            rx.vstack(
                rx.text(
                    file_obj["file_path"] # file directory like 9487br483.png
                ),
                rx.text(
                    file_obj["timestamp"] # timestamp like time.ctime
                ),
                rx.text(
                    file_obj["size"] # file size like 32KB
                ),
                spacing="0px",
                justify="start",
                align_items="start",
            ),
            align="center",
            justify="center",
            font_size="11px",
            width="100%",
            color="GRAY",
        ),
        rx.box(
            height="5px"
        ),
        spacing="0.75vh",
        border_color="#1c1c1c",
        border_width="0.2vh",
        width="100%",
        **kwargs
    )

def file_editor_menu(file_obj, **kwargs):
    return rx.hstack(
        rx.tooltip(
            rx.button(
                rx.icon(
                    tag="trash-2",
                ),
                color="#ee0000",
                bg = "#260000",
                _hover = {"bg":"#420000","color":"#ff0000"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click=State.delete_file(file_obj)
            ),
            content = "Delete"
        ),
        rx.tooltip(
            rx.button(
                rx.icon(
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
            content="Copy Link"
        ),
        rx.tooltip(
            rx.button(
                rx.icon(
                    tag="arrow-down-to-line"
                ),
                color="#12a1fb",
                bg = "#11222f",
                _hover = {"bg":"#223340","color":"#22c9bb"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click = State.download_file(file_obj),
            ),
            content="Download File"
        ),
        rx.tooltip(
            rx.link(
                rx.button(
                    rx.icon(
                        "eye",
                    ),
                    color="#ffb100",
                    bg = "#302400",
                    _hover = {"bg":"#413511","color":"#ffc200"},
                    border_radius="2vh",
                    height="30px",
                ),
                href=file_obj["file_link_with_name"],
                target="_blank",
                width="15%"
            ),
            content="View file"
        ),
        justify_content="center",
        align_items="center",
        height="42px",
        spacing="20px",
        width="100%",
        border_color="#1c1c1c",
        **kwargs,
    ),

class FileCardState(State):
    def switch_caching(self, file_obj):
        switch_cache_status(file_obj["file_path"])
        for file in self.user_files:
            if file["file_path"] == file_obj["file_path"]:
                file["cached"] = not file["cached"]
                break

def file_card_context_menu_wrapper(component, file_obj):
    return rx.context_menu.root(
            rx.context_menu.trigger(
                component
            ),
            rx.context_menu.content(
                rx.cond(
                    file_obj["cached"],
                    rx.context_menu.item("Caching: Enabled", on_click = lambda: FileCardState.switch_caching(file_obj)),
                    rx.context_menu.item("Caching: Disabled", on_click = lambda: FileCardState.switch_caching(file_obj)),
                ),
                rx.context_menu.separator(),
                rx.context_menu.item("Copy shortened path", on_click=lambda: State.copy_file_path(file_obj)),
                rx.context_menu.item("Copy download link", on_click=lambda: State.copy_download_link(file_obj)),
            )
        )

def file_card(file_obj):
    return file_card_context_menu_wrapper(
    rx.vstack(
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
        empty_component()
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
        display="none" if (width=="0px" and height=="0px") else "inline"
    )


class TabletNavbarState(SystemHealthState):
    show_system_health_for_tablet:bool = False

    def open_system_health_for_tablet(self):
        self.show_system_health_for_tablet = True
        self.load_system_health_checker = True
    
    def close_system_health_no_params_for_tablet(self):
        self.show_system_health_for_tablet = False
        self.load_system_health_checker = False
    
    def close_system_health_for_tablet(self, discard_var=None):
        self.close_system_health_no_params_for_tablet()


def tablet_drawer(button, current_page):
    return rx.drawer.root(
    rx.drawer.trigger(button),
    rx.drawer.overlay(z_index="5"),
    rx.drawer.portal(
        rx.drawer.content(
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/logo.png", 
                        height="5vh", 
                        custom_attrs={"draggable":"false"},
                        width="auto",
                    ),
                    rx.heading(
                        "DriveV2", 
                        color="WHITE",
                        font_size="2.5vh",
                    ),
                    align="center",
                    justify="center"
                ),
                empty_component(height="1vh"),
                rx_chakra.button(
                    rx.icon(
                        tag="home",
                        height="50%",
                        width="auto"
                    ), 
                    rx_chakra.spacer(), 
                    "Home",
                    rx_chakra.spacer(),
                    bg = "#202020" if (current_page=="home") else "#0f0f0f", 
                    color="WHITE", 
                    width="100%", 
                    _hover={"bg": "#202020"},
                    **{"on_click":rx.redirect("/")} if current_page!="home" else {}
                ),
                rx_chakra.button(
                    rx.icon(
                        tag="File",
                        height="50%",
                        width="auto"
                    ),
                    rx_chakra.spacer(),
                    "Files",  
                    rx_chakra.spacer(),
                    bg = "#202020" if (current_page=="files") else "#0f0f0f", 
                    color="WHITE", 
                    width="100%", 
                    _hover={"bg": "#202020"},
                    **{"on_click":rx.redirect("/my_drive")} if current_page!="files" else {}
                ),
                rx_chakra.button(
                    rx.icon(
                        tag="Folder",
                        height="50%",
                        width="auto"
                    ),
                    rx_chakra.spacer(),
                    "Collections", 
                    rx_chakra.spacer(), 
                    bg = "#202020" if (current_page=="collections") else "#0f0f0f", 
                    color="WHITE", 
                    width="100%", 
                    _hover={"bg": "#202020"},
                    **{"on_click":rx.redirect("/my_collections")} if current_page!="collections" else {}
                ),
                rx.link(
                    rx_chakra.button(
                        rx.icon(
                            tag="github",
                            height="50%",
                            width="auto"
                        ),
                        rx_chakra.spacer(),
                        "Github", 
                        rx_chakra.spacer(), 
                        bg = "#0f0f0f", 
                        color="WHITE", 
                        width="100%", 
                        _hover={"bg": "#202020"},
                    ),
                    width="100%",
                    href="https://github.com/Anga205/AngaDrive",
                    target="_blank"
                ),
                rx.spacer(),
                rx.cond(
                    State.is_logged_in,
                    sidebar_account_widget(),
                    sidebar_login_widget(),
                ),
                align_items="start",
                direction="column",
                width="100%"
            ),
            top="auto",
            right="auto",
            height="100%",
            width="15em",
            padding="2em",
            background_color="#0f0f0f"
        ),
    ),
    direction="left",
)

def tablet_navbar(current_page):            # has a height of 50px
    return rx.box(
    rx.vstack(
        rx.hstack(
            empty_component(
                width="5px"
            ),
            tablet_drawer(
                rx.icon(
                    tag="menu",
                    color="#ffffff",
                    _active={"color":"#777777"},
                ),
                current_page
            ),
            rx.spacer(),
            rx.popover.root(
                rx.popover.trigger(
                    rx.icon(
                        tag="heart-pulse",
                        custom_attrs={"draggable":"false"},
                        color="WHITE", 
                        height="2vh",
                        on_click = TabletNavbarState.open_system_health_for_tablet
                    )
                ),
                rx.popover.content(
                    rx_chakra.vstack(
                        rx_chakra.heading(
                            "System Health", 
                            color="RED",
                            font_size="3.5vh"
                            ),
                        rx_chakra.divider(border_color="GRAY"),
                        rx_chakra.box(
                            rx_chakra.heading(
                                rx_chakra.span(
                                    "Server Uptime: ",
                                    color="rgb(0, 100, 100)"
                                ),
                                rx_chakra.span(
                                    State.uptime,
                                    color="WHITE"
                                ),
                                font_size="2vh",
                            ),
                            rx.cond(
                                State.temperature_available,
                                rx_chakra.heading(
                                    rx_chakra.span(
                                        "Temperature: ",
                                        color="rgb(0, 100, 100)"
                                    ),
                                    rx_chakra.span(
                                        State.temperature,
                                        color="WHITE"
                                    ),
                                    font_size="2vh",
                                ),
                                empty_component()
                            ),
                            rx_chakra.hstack(
                                rx_chakra.circular_progress(
                                    rx_chakra.circular_progress_label("RAM"),
                                    value=State.ram_percent,
                                    size="10vh"
                                ),
                                rx_chakra.circular_progress(
                                    rx_chakra.circular_progress_label("CPU"),
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
                    on_escape_key_down=TabletNavbarState.close_system_health_for_tablet,
                    on_pointer_down_outside=TabletNavbarState.close_system_health_for_tablet,
                    on_focus_outside=TabletNavbarState.close_system_health_for_tablet,
                    on_interact_outside=TabletNavbarState.close_system_health_for_tablet
                ),
                open = TabletNavbarState.show_system_health_for_tablet
            ),
            empty_component(
                width="10px"
            ),
            spacing="2",
            align="center",
            bg="BLACK",
            justify="center",
            height="4.9vh",
            width="100%",
        ),
        rx.progress(
            value = State.upload_progress,
            width="100%",
            bg="BLACK",
            height="0.1vh",
        ),
        spacing="0",
        position="fixed",
        height="5vh",
        width="100%",
        align="center",
        justify="center"
    ),
    height="5vh",
    width="100%",
    align="center",
    justify="center"
)

def mobile_file_card(file_obj):
    return rx.vstack(
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
    width="90%",
    spacing='0'
)

def desktop_collection_card(collection_obj, copy_function=rx.set_clipboard("ERROR"), button3=None, button3_condition=True):
    def sample_button():
        return rx.button(
            rx.icon("vault"),
            color_scheme="blue",
            radius="large",
            variant="soft"
        )

    if button3==None:
        button3 = sample_button()
    return rx.vstack(
        rx.heading(
            collection_obj["name"],
            color="WHITE",
        ),
        rx_chakra.divider(border_color="GRAY"),
        rx.hstack(
            rx.vstack(
                rx.text("Size:"),
                rx.text("File Count:"),
                rx.text("Folder count:"),
                rx.text("Editors:"),
                width="100px"
            ),
            rx.vstack(
                rx.text(collection_obj["size"]),
                rx.text(collection_obj["file_count"]),
                rx.text(collection_obj["folder_count"]),
                rx.text(collection_obj["editor_count"]),
            ),
            color="GRAY",
            align="center"
        ),
        rx.hstack(
            rx_chakra.tooltip(
                rx.link(
                    rx.button(
                        rx.icon(
                            "eye"
                        ),
                        color="#ffb100",
                        bg = "#302400",
                        _hover = {"bg":"#413511","color":"#ffc200"},
                        radius="large",
                        variant="soft"
                    ),
                    href=f"{app_link}/collection/?id={collection_obj['id']}",
                ),
                label="View Collection"
            ),
            rx.spacer(),
            rx_chakra.tooltip(
                rx.button(
                    rx.icon(
                        "copy"
                    ),
                    color_scheme="green",
                    radius="large",
                    variant="soft",
                    on_click=copy_function
                ),
                label="Copy link"
            ),
            conditional_render(
                button3_condition,
                rx.hstack(
                    rx.spacer(),
                    button3
                )
            ),
            align="center",
            width="90%"
        ),
        align="center",
        padding="20px",
        bg="#1c1c1c",
        width="250px",
        border_radius="5px"
    )