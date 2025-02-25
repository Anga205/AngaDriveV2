import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *
from AngaDriveV2.login_dialog import *
import platform
import reflex_chakra as rx_chakra

def static_data_box(**kwargs) -> rx.Component:
    return rx_chakra.vstack(
        rx.desktop_only(
            rx_chakra.hstack(
                card(
                    heading="RAM Usage",
                    content=rx.cond(
                        State.ram_percent,
                        rx_chakra.circular_progress(
                            rx_chakra.circular_progress_label(
                                rx_chakra.vstack(
                                    rx_chakra.text(
                                        State.used_ram, 
                                        color="WHITE", 
                                        font_size="1vh"
                                    ),
                                    rx.divider(
                                        color_scheme="cyan",
                                        width="50%"
                                    ),
                                    rx_chakra.text(
                                        State.total_ram, 
                                        color="WHITE", 
                                        font_size="1vh"
                                    ),
                                    spacing="0px"
                                )
                            ),
                            value=State.ram_percent, 
                            color="BLUE",
                            size="9vh",
                            height="100%",
                        ),
                        rx_chakra.circular_progress(
                            rx_chakra.circular_progress_label("Loading....", color="WHITE", font_size="1vh"),
                            color="BLUE",
                            is_indeterminate=True,
                            size="9vh",
                            height="100%",
                        )
                    ),
                    height="17vh",
                    overflow="auto",
                    width="30%"
                ),
                card(
                    heading="CPU Usage",
                    content=rx.cond(
                        State.ram_percent,
                        rx_chakra.circular_progress(
                            rx_chakra.circular_progress_label(
                                rx_chakra.text(
                                    rx_chakra.span(
                                        State.cpu_usage,
                                        font_size="2vh"
                                    ),
                                    rx_chakra.span(
                                        "%",
                                        font_size="1vh"
                                    )
                                ),
                            ),
                            value=State.cpu_usage, 
                            color="BLUE",
                            size="9vh",
                        ),
                        rx_chakra.circular_progress(
                            rx_chakra.circular_progress_label("Loading....", color="WHITE", font_size="1vh"),
                            color="BLUE",
                            is_indeterminate=True,
                            size="9vh",
                        )
                    ),
                    height="17vh",
                    overflow="auto",
                    width="30%"
                ),
                rx_chakra.vstack(
                    rx.cond(
                        State.temperature_available,
                        rx_chakra.box(
                            rx_chakra.text(
                                rx_chakra.span("Temperature: ", color="BLUE", font_size="2.5vh", as_="b"),
                                State.temperature,
                                color="WHITE",
                                font_size="2.5vh",
                                overflow="auto",
                                text_align="center"
                            ),
                            width="100%",
                            height="50%",
                            bg="BLACK",
                            border_radius="0.5vh",
                            padding="1.5vh",
                            align="center"
                        ),
                        rx_chakra.box(
                            rx_chakra.text(
                                "Temperature Unavailable",
                                color="RED",
                                as_="b",
                                font_size="2.5vh",
                                overflow="auto",
                                text_align="center"
                            ),
                            width="100%",
                            height="50%",
                            bg="BLACK",
                            border_radius="0.5vh",
                            padding="1.5vh",
                            align="center"
                        ),
                    ),
                    rx_chakra.box(
                        rx.cond(
                            State.uptime,
                            rx_chakra.text(
                                rx_chakra.span("Uptime: ", color="BLUE", font_size="2.5vh", as_="b"),
                                State.uptime,
                                color="WHITE",
                                font_size="2.5vh",
                                overflow="auto",
                                text_align="center"
                            ),
                            rx_chakra.text(
                                "Loading...",
                                color="WHITE",
                                font_size="2.5vh",
                                text_align="center"
                            )
                        ),
                        width="100%",
                        height="50%",
                        bg="BLACK",
                        border_radius="0.5vh",
                        padding="1.5vh"
                    ),
                    height="100%",
                    width="40%",
                ),
                height="17vh",
                width="100%",
                on_mount=SystemHealthState.open_system_health,
                on_unmount=SystemHealthState.close_system_health_no_params
            ),
            width="100%"
        ),
        rx_chakra.hstack(
            site_data_card(
                "Pulses",
                State.pulses,
                width = "100%",
            ),
            rx_chakra.tooltip(
                site_data_card(
                    "Users", 
                    State.user_count,
                    width="100%"
                ),
                label=State.registered_user_count
            ),
            site_data_card(
                "Collections", 
                State.collection_count,
                height="100%",
                width="130%"
            ),
            width="100%",
            spacing="0.75vh",
        ),
        rx_chakra.flex(
            rx.tooltip(
                site_data_card(
                    "Space Used", 
                    State.space_used, 
                    width="50%", 
                ),
                content=f"Your Storage: {State.user_storage_amount}",
            ),
            rx_chakra.box(width="1vh"),
            rx.tooltip(
                site_data_card(
                    "Files hosted", 
                    State.files_hosted,
                    height="100%",
                    width="50%",
                    overflow="auto"
                ),
                content=f"Your files: {State.user_file_count}",
            ),
            width="100%",
        ),
        rx.mobile_and_tablet(
            rx_chakra.hstack(
                site_data_card(
                    heading="Host",
                    content=f"{platform.node()} {platform.machine()}",
                    width="40%",
                ),
                site_data_card(
                    heading="Temp",
                    content=State.temperature,
                    width="30%",
                    overflow="auto"
                ),
                site_data_card(
                    heading="Uptime",
                    content=State.uptime,
                    width="30%",
                    overflow="auto"
                ),
                width="100%"
            ),
            width="100%"
        ),
        rx.box(
            rx.moment(
                interval=500, 
                on_change=SystemHealthState.tick_health
            ),
            display="none"
        ), 
        card(
            "Site activity over past week",
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key="times_opened",
                    stroke = "#0000ff",
                    fill = "#0000ff",
                    type_ = "linear"
                ),
                rx.recharts.x_axis(data_key="date"),
                rx.recharts.y_axis(),
                rx.recharts.cartesian_grid(stroke_dasharray="1 1"),
                rx.recharts.graphing_tooltip(),
                data=State.site_activity,
                color="BLACK",
                font_size="1.5vh",
                height="100%"
            ),
            width = "100%",
            height="100%"
        ),
        bg="rgb(0, 0, 255, 0.1)",
        padding="1vh",
        border_radius="1vh",
        spacing="0.75vh",
        **kwargs
    )

def login_button_group() -> rx.Component:
    return rx_chakra.vstack(
        rx_chakra.hstack(
            login_dialog(
                rx_chakra.button(
                    "Sign Up",
                    height="100%",
                    width="100%",
                    on_click=LoginState.set_to_signup_mode,
                    font_size="1.4vh",
                    bg="#0f1f0f",
                    color="white",
                    border_radius="1vh 0vh 0vh 0vh",
                    _hover={"bg":"#0f1f0f","color":"#11cc11"}
                ),
                height="100%",
                width="110%"
            ),
            login_dialog(
                rx_chakra.button(
                    "Login",
                    height="100%",
                    width="100%",
                    bg="#1f0f0f",
                    color="WHITE",
                    on_click=LoginState.set_to_login_mode,
                    font_size="1.4vh",
                    border_radius="0vh 1vh 0vh 0vh",
                    _hover={"bg":"#1f0f0f","color":"#cc1111"}
                ),
                height="100%",
                width="90%"
            ),
            height="100%",
            spacing="0vh",
            width="100%"
        ),
        tpu_signup_button(
            height="100%",
            width="100%",
            font_size="1.4vh",
            border_radius="0vh 0vh 1vh 1vh"
        ),
        height="100%",
        spacing="0vh",
        width="40%",
    )


class AccountEditorState(State):
    def temp_edit_aspect(self):
        print("TODO: update AccountEditorState.temp_edit_aspect")

    account_deletion_dialog:bool = False
    account_deletion_password:str = ""
    account_deletion_file_switch:bool = False
    show_account_deletion_file_switch:bool = False
    switch_tooltip_text = "Your files will be deleted"

    def open_account_deletion_dialog(self):
        self.account_deletion_dialog = True
        user_files_bool:bool = does_user_have_files(self.token)
        self.show_account_deletion_file_switch = user_files_bool
        self.account_deletion_file_switch = user_files_bool

    def close_account_deletion_dialog(self, discard_var=None):
        self.account_deletion_password:str = ""
        self.account_deletion_dialog = False
    
    def switch_account_deletion_file_switch(self, new_value):
        self.account_deletion_file_switch = new_value
        if new_value==True:
            self.switch_tooltip_text = "Your files will be deleted"
        else:
            self.switch_tooltip_text = "Your files will not be deleted"

    def delete_account(self):
        login_successful = user_login(self.token)
        if True in login_successful:
            self.close_account_deletion_dialog()
            if self.show_account_deletion_file_switch:
                if self.account_deletion_file_switch:
                    files=get_all_user_files_for_display(self.token)
                    for file in files:
                        try:
                            remove_file_from_database(file[0])
                        except Exception as e:
                            print(f"Error removing file {file[0]}: {e}")
            remove_account_from_accounts_table(self.token)
            self.logout()
        else:
            return rx.window_alert(login_successful[False])




def confirm_account_delete_dialog(button, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(
            button,
            **kwargs
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Confirm account deletion", 
                color="WHITE"
                ),
            rx.dialog.description(
                rx_chakra.vstack(
                    rx_chakra.password(
                        placeholder="Enter password",
                        width="100%",
                        color="WHITE"
                    ),
                    rx_chakra.hstack(
                        rx.cond(
                            AccountEditorState.show_account_deletion_file_switch,
                            rx.tooltip(
                                rx.switch(
                                    color_scheme="tomato",
                                    variant="classic",
                                    radius="small",
                                    checked=AccountEditorState.account_deletion_file_switch,
                                    on_change=AccountEditorState.switch_account_deletion_file_switch
                                ),
                                content=AccountEditorState.switch_tooltip_text
                            ),
                            rx.box(width="0px",height="0px")
                        ),
                        rx_chakra.spacer(),
                        rx_chakra.button(
                            "Delete",
                            color_scheme="red",
                            is_disabled=True,
                            on_click = AccountEditorState.delete_account
                        ),
                        width="100%"
                    )
                )
            ),
            bg="#0f0f0f",
            on_escape_key_down = AccountEditorState.close_account_deletion_dialog,
            on_pointer_down_outside = AccountEditorState.close_account_deletion_dialog
        ),
        open=AccountEditorState.account_deletion_dialog
    )

def feature_card(image_path, heading, description, **kwargs):
    return rx_chakra.vstack(
        rx.desktop_only(
            rx_chakra.image(
                src=image_path,
                custom_attrs={"draggable":"false"},
                height="100%",
                width="auto",
            ),
            height="50%"
        ),
        rx.mobile_and_tablet(
            rx_chakra.image(
                src=image_path,
                custom_attrs={"draggable":"false"},
                height="auto",
                width="90%",
            )
        ),
        rx_chakra.heading(
            heading,
            font_size="2.2vh"
        ),
        rx_chakra.divider(
            border_color="GRAY"
        ),
        rx_chakra.text(
            description,
            font_size="1.5vh"
        ),
        color="WHITE",
        bg="BLACK",
        spacing="0.75vh",
        border_radius="0.75vh",
        border_width="1vh",
        border_color="BLACK",
        width="33%",
        height="100%",
        **kwargs
    )


def whats_new_widget():
    return rx_chakra.vstack(
        rx_chakra.heading(
            "What's New with V2?",
            color="WHITE",
            font_size="3.5vh"
            ),
        rx_chakra.divider(
            border_color="GRAY"
            ),
        rx_chakra.hstack(
            feature_card(
                "/incognito.png",
                "Anonymous Uploads",
                "You no longer need an account to make full use of the core features provided by AngaDrive, you can just open the website and start uploading!"
            ),
            feature_card(
                "/rush.png",
                "Improved Speed",
                "Thanks to V2  making use of FastAPI as opposed to the reflex framework, along with countless minor optimizations, V2 should be upto 200% faster"
            ),
            feature_card(
                "/add-to-database.png",
                "Improved Capacity",
                "This website now runs on the raspberry pi 5, using a 1 terabyte disk, this should address a few more performance issues and file-size related bugs"
            ),
            spacing="0.75vh",
            width="100%",
            height="45%"
        ),
        rx_chakra.hstack(
            feature_card(
                "file_collection.png",
                "Galleries",
                "Now you can bundle a set of uploaded files into a single previewable gallery to share with friends!"
            ),
            feature_card(
                "/drag-and-drop.png",
                "Drop Anywhere",
                "You can now drag and drop your files anywhee on the webapp to upload it to AngaDrive cloud"
            ),
            feature_card(
                "/preview.png",
                "File Previews",
                "For select file types (like mp4, png, jpg etc.) you can preview the file from within the dashboard/gallery itself"
            ),
            spacing="0.75vh",
            width="100%",
            height="45%"
        ),
        border_color = "#1c0c1c",
        spacing="0.75vh",
        border_width="1vh",
        bg = "#1c0c1c",
        border_radius = "1vh",
        width="100%",
        height="80%"
    )

class SettingsState(State):
    
    def restore_defaults(self):
        if self.enable_caching:
            self.swap_caching()
        if self.ultra_secure:
            self.swap_security()
        if not self.enable_previews:
            self.swap_previews()
    
    show_coming_soon:bool = False
    def open_coming_soon(self):
        self.show_coming_soon = True
    
    def close_coming_soon(self, discard=False):
        self.show_coming_soon = False

def coming_soon_dialog(trigger, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.dialog.title("Coming Soon"),
            rx.dialog.description("This feature is under development and will be available soon"),
            bg="#0f0f0f",
            on_escape_key_down=SettingsState.close_coming_soon,
            on_pointer_down_outside=SettingsState.close_coming_soon
        ),
        open=SettingsState.show_coming_soon,
        **kwargs
    )


def settings_widget_desktop(**kwargs):
    def settings_button(heading, icon, tooltip, **kwargs):
        enabled = True
        if "enabled" in kwargs:
            enabled = kwargs["enabled"]
            del kwargs["enabled"]
        
        if "condition" not in kwargs:
            return rx.tooltip(
                rx.button(
                    rx.vstack(
                        rx.heading(
                            heading,
                            font_size="3vh",
                            overflow="auto"
                        ),
                        rx.icon(
                            icon,
                            height="50%",
                            width="50%"
                        ),
                        rx.text(
                            "Default: Enabled" if enabled else "Default: Disabled",
                            font_size="1.5vh"
                        ),
                        justify="center",
                        overflow="auto",
                        height="100%",
                        spacing="0vh",
                        padding="0vh",
                        width="100%",
                        align="center"
                    ),
                    height="100%",
                    width="32.5%",
                    bg="rgb(0,255,0,0.1)" if enabled else "rgb(255,0,0,0.1)",
                    color="#BBBBBB",
                    padding="0.5vh",
                    align="center",
                    _hover={"bg":"rgb(0,255,0,0.5)" if enabled else "rgb(255,0,0,0.5)", "color":"WHITE"},
                    **kwargs
                ),
                content=tooltip,
            )
        else:
            condition = kwargs["condition"]
            del kwargs["condition"]
            return rx.cond(
                condition,
                settings_button(heading, icon, tooltip[0], enabled=True, **kwargs),
                settings_button(heading, icon, tooltip[1], enabled=False, **kwargs),
            )
    return rx.vstack(
        rx.hstack(
            settings_button(
                "Caching",
                "database-zap",
                [
                    "Caching is currently Enabled, this may result in slower file deletion. (Upto 2 hours)",
                    "Caching is currently Disabled, this may result in slightly slower page-load times.",
                ],
                condition=State.enable_caching,
                on_click=SettingsState.swap_caching
            ),
            settings_button(
                "File Previews",
                "eye",
                [
                    "File Previews are currently Enabled, this may result in slower page-load times.",
                    "File Previews are currently Disabled, use this to speed up page-load times.",
                ],
                condition=State.enable_previews,
                on_click=State.swap_previews
            ),
            coming_soon_dialog(
                settings_button(
                    "Ultra-Secure",
                    "lock",
                    [
                        "Ultra-Secure is currently Enabled, all newly uploaded files are protected by password-authentication by default",
                        "Ultra-Secure is currently Disabled, all newly uploaded files are accessible to anyone with the link",
                    ],
                    condition=State.ultra_secure,
                    on_click=SettingsState.open_coming_soon
                )
            ),
            spacing="1vh",
            overflow="hidden",
            width="100%",
            height="80%"
        ),
        rx.button(
            rx.text("Restore Defaults", as_="b"),
            font_size="1.65vh",
            width="100%",
            height="20%",
            color_scheme="tomato",
            disabled=~(State.ultra_secure | ~State.enable_previews| State.enable_caching),
            on_click=SettingsState.restore_defaults,
            variant="soft",
        ),
        bg="rgb(9, 232, 84, 0.05)",
        border_radius="1vh",
        padding="1vh",
        **kwargs
    )

def import_files(**kwargs):
    return rx.vstack(
        rx_chakra.heading(
            "Import/Export files",
            color="WHITE",
            font_size="2vh",
            height="5vh"
        ),
        rx_chakra.divider(
            border_color="GRAY"
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger(
                    "GitHub", 
                    value="github",
                    height="4vh"
                ),
                rx.tabs.trigger(
                    "Flowinity", 
                    value="flowinity",
                    height="4vh"
                ),
                rx.tabs.trigger(
                    "Export", 
                    value="export",
                    height="4vh"
                ),
                height="13vh",
                font_size="1.3vh",
                spacing="0vh"
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.spacer(),
                    rx_chakra.input(
                        placeholder="Enter github repo URL",
                        width="100%",
                        font_size="1.5vh",
                        height="3.5vh",
                        border_radius="0.3vh",
                    ),
                    rx.hstack(
                        rx.spacer(),
                        rx.button(
                            "Import as collection",
                            color_scheme="iris",
                            variant="soft",
                            font_size="1.3vh",
                            disabled=True
                        ),
                        width="100%"
                    ),
                    rx.spacer(),
                    spacing="1vh",
                    height="100%",
                    padding="10px"
                ),
                value="github",
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.spacer(),
                    rx_chakra.input(
                        placeholder="Enter file link",
                        width="100%",
                        font_size="1.5vh",
                        height="3.5vh",
                        border_radius="0.3vh",
                    ),
                    rx.hstack(
                        rx.spacer(),
                        rx.button(
                            "Import files",
                            color_scheme="iris",
                            variant="soft",
                            font_size="1.3vh",
                            disabled=True
                        ),
                        width="100%"
                    ),
                    rx.spacer(),
                    spacing="1vh",
                    height="100%",
                    padding="10px"
                ),
                value="flowinity",
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.spacer(),
                    rx_chakra.password(
                        placeholder="Enter password",
                        width="100%",
                        font_size="1.5vh",
                        height="3.5vh",
                        border_radius="0.3vh",
                    ),
                    rx.hstack(
                        rx.spacer(),
                        rx.button(
                            "Export files",
                            color_scheme="iris",
                            variant="soft",
                            font_size="1.3vh",
                            disabled=True
                        ),
                        width="100%"
                    ),
                    rx.spacer(),
                    spacing="1vh",
                    style={"height":"100%"},
                    height="100%",
                    padding="10px"
                ),
                value="export",
            ),
            default_value="github",
            orientation="vertical",
            width="100%",
            bg="BLACK",
            font_size="1.2vh",
            border_radius="1vh",
            on_click=SettingsState.open_coming_soon,
            height="100%",
            spacing="1vh"
        ),
        overflow="auto",
        bg="rgb(67, 108, 49, 0.1)",
        border_radius="1vh",
        align="center",
        padding="1vh",
        spacing="1vh",
        **kwargs
    )

def bulk_actions_widget(**kwargs):
    return rx_chakra.vstack(
        rx_chakra.heading(
            "Bulk Actions",
            font_size="2.2vh",
        ),
        rx_chakra.vstack(
            rx_chakra.accordion(
                rx_chakra.accordion_item(
                    rx_chakra.accordion_button(
                        "File Actions",
                        rx_chakra.accordion_icon(),
                        font_size="2vh",
                    ),
                    rx_chakra.accordion_panel(
                        rx_chakra.vstack(
                            rx_chakra.button(
                                "Delete my files",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            rx_chakra.button(
                                "Transfer my files",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            rx_chakra.button(
                                "Change existing file settings",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            height="12vh",
                            spacing="0.5vh"
                        )
                    ),
                ),
                rx_chakra.accordion_item(
                    rx_chakra.accordion_button(
                        "Collection Actions",
                        rx_chakra.accordion_icon(),
                        font_size="2vh",
                    ),
                    rx_chakra.accordion_panel(
                        rx_chakra.vstack(
                            rx_chakra.button(
                                "Delete my Collections",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            rx_chakra.button(
                                "Transfer my Collections",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            rx_chakra.button(
                                "Change existing Collection settings",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            height="12vh",
                            spacing="0.5vh"
                        )
                    ),
                ),
                rx_chakra.accordion_item(
                    rx_chakra.accordion_button(
                        "Account Actions",
                        rx_chakra.accordion_icon(),
                        font_size="2vh",
                    ),
                    rx_chakra.accordion_panel(
                        rx_chakra.vstack(
                            rx_chakra.button(
                                "Change password",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            rx_chakra.button(
                                "Change account settings",
                                width="100%",
                                font_size="1.7vh",
                                height="33%",
                                border_radius="0.3vh"
                            ),
                            height="12vh",
                            spacing="0.5vh"
                        )
                    ),
                ),
                default_index=[0],
                spacing="0vh",
                width="100%",
                height="100%"
            ),
            height="80%",
            width="100%",
            spacing="0px"
        ),
        padding="1vh",
        border_radius="1vh",
        bg="rgb(120, 122, 151, 0.1)",
        spacing="1vh",
        on_click=SettingsState.open_coming_soon,
        overflow="auto",
        **kwargs
    )

def contact_me_widget(**kwargs):
    return rx_chakra.vstack(
        rx_chakra.heading(
            "Message the Developer", 
            font_size="2.2vh"
        ),
        rx_chakra.divider(
            border_color="GRAY"
        ),
        rx_chakra.vstack(
            rx_chakra.text_area(
                placeholder="You can send me issues, feature requests, or just say hi! but if ur expecting a response then remember to leave your email or anything else i can use to get back to you later",
                height="92%",
                font_size="1.5vh",
                width="100%",
                bg="BLACK"
            ),
            rx_chakra.hstack(
                rx_chakra.spacer(),
                rx_chakra.button(
                    "Send",
                    font_size="1.6vh",
                    height="100%",
                    width="25%"
                ),
                width="100%",
                height="8%"
            ),
            height="100%",
            width="100%",
        ),
        border_radius="1vh",
        padding="1vh",
        spacing="1vh",
        bg="rgb(184, 109, 119, 0.1)",
        overflow="auto",
        **kwargs
    )


def desktop_index():

    return site_template(
        "Home",
        rx_chakra.hstack(
            rx_chakra.box(
                width="0vh",
                height="0vh"
            ),
            rx_chakra.vstack(
                settings_widget_desktop(
                    width="100%",
                    height="20%"
                ),
                static_data_box(
                    height="80%",
                    width="100%",
                ),
                height="100%",
                spacing="0.75vh",
                width="50%"
            ),
            rx_chakra.vstack(
                rx.heading(
                    "More features coming soon!",
                ),
                align_items="center",
                justify="center",
                bg="rgb(255,0,255,0.08)",
                border_radius="1vh",
                width="50%",
                height="100%"
            ),
            rx_chakra.box(
                height="0vh",
                width="0vh"
            ),
            spacing="0.75vh",
            width="100%",
            height="93.25vh"
            ),
        )



def why_use_angadrive_tablet():
    return rx.vstack(
        rx.spacer(),
        rx.heading("Why use AngaDrive?", color="WHITE"),
        rx.box(
            rx.scroll_area(
                rx.hstack(
                    feature_card(
                        "/incognito.png",
                        "Anonymous Uploads",
                        "You no longer need an account to make full use of the core features provided by AngaDrive, you can just open the website and start uploading!"
                    ),
                    feature_card(
                        "/rush.png",
                        "Improved Speed",
                        "Thanks to V2  making use of FastAPI as opposed to the reflex framework, along with countless minor optimizations, V2 should be upto 200% faster"
                    ),
                    feature_card(
                        "/add-to-database.png",
                        "Improved Capacity",
                        "This website now runs on the raspberry pi 5, using a 1 terabyte disk, this should address a few more performance issues and file-size related bugs"
                    ),
                    feature_card(
                        "file_collection.png",
                        "Galleries",
                        "Now you can bundle a set of uploaded files into a single previewable gallery to share with friends!"
                    ),
                    feature_card(
                        "/drag-and-drop.png",
                        "Drop Anywhere",
                        "You can now drag and drop your files anywhee on the webapp to upload it to AngaDrive cloud"
                    ),
                    feature_card(
                        "/preview.png",
                        "File Previews",
                        "For select file types (like mp4, png, jpg etc.) you can preview the file from within the dashboard/gallery itself"
                    ),
                    spacing='5',
                    width=1600
                ),
                type="always",
                scrollbars="horizontal",
#                style={"height":400}
            ),
            width="80%",
        ),
        rx.box(height="1vh"),
        bg="#001015",
#        height="60vh",
        width="100%",
        align="center"
    )

def tablet_site_data():
    return rx.vstack(
        rx.spacer(),
        rx.heading("Here's some numbers:", color="WHITE"),
        static_data_box(width="98%", height="90%"),
        rx.spacer(),
        align="center",
        width="100%",   
        height="80vh",
        bg="#001510",
    )

def tablet_top_widget():
    return rx.vstack(
    rx.spacer(),
    rx.cond(
        State.is_logged_in,
        rx.vstack(
            rx.heading("Welcome back, ",State.username),
            font_size="40px",
            align="center"
        ),
        rx.vstack(
            rx.heading(
                rx.text.span("Anga", color="BLUE"),
                rx.text.span("Drive", color="PURPLE"),
                rx.text.span("V2", color="CYAN"), 
                font_size="40px"
            ),
            rx.text(
                "Because 99₹/month for google one was too expensive. (also open source btw)", 
                width="75%", 
                color="GRAY",
                text_align="center"
            ),
            align="center",
            width="100%"
        ),
    ),
    rx.spacer(),
    spacing="2",
    bg="rgb(16, 16, 16)",
    width="100%",
    height="80vh",
    align="center",
    color="WHITE",
),

def tablet_index():
    return rx.vstack(
        tablet_navbar("home"),
        tablet_top_widget(),
        why_use_angadrive_tablet(),
        tablet_site_data(),
        spacing="0",
        width="100%"
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index()
        ),
        rx.mobile_and_tablet(
            tablet_index()
        ),
        width="100%",
    )