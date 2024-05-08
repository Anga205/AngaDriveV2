import reflex as rx
from AngaDriveV2.presets import *
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *
from AngaDriveV2.login_dialog import *


def static_data_box(**kwargs) -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.heading(
            "DriveV2 - Site Data",
            color="WHITE",
            font_size="3.5vh"
            ),
        rx.chakra.divider(
            border_color="GRAY"
            ),
        rx.chakra.hstack(
            site_data_card(
                "Files hosted", 
                State.files_hosted,
                height="100%",
                width="140%"
                ),
            rx.chakra.tooltip(
                site_data_card(
                    "Users", 
                    State.user_count,
                    height="100%",
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
                    type_ = "linear"
                ),
                rx.recharts.x_axis(data_key="date"),
                rx.recharts.y_axis(),
                rx.recharts.cartesian_grid(stroke_dasharray="1 1"),
                rx.recharts.graphing_tooltip(),
                data=State.site_activity,
                color="BLACK",
                height="100%"
            ),
            width = "100%",
            height="250%"
        ),
        rx.chakra.flex(
            site_data_card("Space Used", State.space_used, width="50%", height="100%"),
            rx.chakra.box(width="1vh"),
            site_data_card("Pulses",State.pulses, width = "50%", height="100%"),
            width="100%",
            height="100%",
        ),
        bg="#0f0f1f",
        border_width="1vh",
        border_radius = "1vh",
        border_color="#0f0f1f",
        spacing="0.75vh",
        **kwargs
    )

def login_button_group() -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.hstack(
            login_dialog(
                rx.chakra.button(
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
                rx.chakra.button(
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
        print(self.token)
    
    def logout(self):
        self.token = gen_token()
        self.is_logged_in = ""
        self.username:str = "{username}"
        self.email:str = "{email_id}"
        self.update_account_data_components()

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
                rx.chakra.vstack(
                    rx.chakra.password(
                        placeholder="Enter password",
                        width="100%",
                        color="WHITE"
                    ),
                    rx.chakra.hstack(
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
                        rx.chakra.spacer(),
                        rx.chakra.button(
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
                    custom_attrs={"draggable":"false"},
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
    else:
        edit_button = lambda: rx.chakra.button(
            rx.chakra.icon(
                tag="edit", 
                height="100%", 
                width="auto"
                ), 
            height="1.65vh", 
            bg="BLACK", 
            width="33%", 
            _hover = {"bg":"#111111"}
            )
        def account_aspect_line(aspect, data, action):
            return rx.chakra.hstack(
                rx.chakra.text(
                    aspect,
                    font_weight="bold",
                    width="100%",
                    text_align="center"
                ),
                rx.chakra.text(
                    data,
                    width = "100%",
                    text_align = "center"
                ),
                rx.chakra.button(
                    rx.chakra.icon(
                        tag="edit",
                        height="100%",
                        width="auto"
                    ),
                    height="1.65vh",
                    bg="BLACK",
                    _hover = {"bg":"#111111"},
                    on_click=action,
                    width="33%"
                ),
                font_size="1.65vh",
                spacing="0vh",
                width="100%"
            )
        
        return rx.chakra.vstack(
            rx.chakra.divider(
                border_color="GRAY"
                ),
            account_aspect_line(
                "Name", 
                State.username, 
                AccountEditorState.temp_edit_aspect
                ),
            rx.chakra.divider(
                border_color="GRAY"
                ),
            account_aspect_line(
                "E - mail",
                State.email,
                AccountEditorState.temp_edit_aspect
                ),
            rx.chakra.divider(
                border_color="GRAY"
                ),
            account_aspect_line(
                "Password",
                "*********",
                AccountEditorState.temp_edit_aspect
                ),
            rx.chakra.divider(
                border_color="GRAY"
                ),
            rx.chakra.hstack(
                rx.chakra.button(
                    rx.chakra.hstack(
                        rx.chakra.image(
                            src="/logout.png",
                            height="2.5vh",
                            width="auto",
                            custom_attrs={"draggable":"false"},
                        ),
                        rx.chakra.text(
                            "Log out",
                            font_size="1.65vh"
                        ),
                        spacing="1vh"
                    ),
                    on_click = AccountEditorState.logout,
                    bg="#2f0000",
                    _hover={"bg":"#330202"},
                    height="5vh",
                    border_radius="1vh",
                ),
                rx.chakra.spacer(),
                confirm_account_delete_dialog(
                    rx.chakra.button(
                        rx.chakra.hstack(
                            rx.chakra.icon(
                                tag="delete",
                                height="2.5vh",
                                width="auto",
                                color="WHITE"
                            ),
                            rx.chakra.text(
                                "Delete",
                                font_size="1.65vh"
                            ),
                            spacing="0.75vh"
                        ),
                        bg="#2f0000",
                        _hover={"bg":"#330202"},
                        height="5vh",
                        border_radius="0.75vh",
                        on_click=AccountEditorState.open_account_deletion_dialog
                    )
                ),
                width="100%",
                spacing="0vh",
            ),
            bg = "BLACK",
            spacing = "1.2vh",
            height = "100%",
            width = "100%",
            color="WHITE",
            border_color = "BLACK",
            font_size="1.65vh",
            border_radius = "1vh",
            border_width = "0.75vh"
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
                    width="22vh",
                    height="100%"
                ),
                height="100%",
                spacing="0.75vh"
            ),
            rx.cond(
                State.is_logged_in,
                account_manager(logged_in=True),
                account_manager(logged_in=False),
            ),
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

def feature_card(image_path, heading, description):
    return rx.chakra.vstack(
        rx.chakra.image(
            src=image_path,
            custom_attrs={"draggable":"false"},
            height="50%",
            width="auto",
        ),
        rx.chakra.heading(
            heading,
            font_size="2.2vh"
            ),
        rx.chakra.divider(
            border_color="GRAY"
        ),
        rx.chakra.text(
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
        height="100%"
    )


def whats_new_widget():
    return rx.chakra.vstack(
        rx.chakra.heading(
            "What's New with V2?",
            color="WHITE",
            font_size="3.5vh"
            ),
        rx.chakra.divider(
            border_color="GRAY"
            ),
        rx.chakra.hstack(
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
        rx.chakra.hstack(
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

def github_widget():
    return rx.chakra.button(
        rx.chakra.vstack(
            rx.chakra.image(
                src="github.png",
                height="60%",
                custom_attrs={"draggable":"false"},
                width="auto"
                ),
            rx.chakra.heading(
                "Star this project on github",
                font_size="1.65vh"
            ),
            height="100%",
            width="100%",
            spacing="1vh"
            ),
        color="WHITE",
        height="17.25vh",
        border_color="rgb(30,10,20)",
        _hover = {
            "bg":"rgb(15,5,10)", 
            "border-color":"rgb(15,5,10)",
            "color":"GRAY"
            },
        on_click=rx.redirect("https://github.com/Anga205/AngaDriveV2", external=True),
        width="100%",
        border_radius = "1vh",
        bg = "rgb(30,10,20)",
        border_width="1vh"
    )

def desktop_index():
    return site_template(
        "Home",
        rx.chakra.hstack(
            rx.chakra.box(
                width="0vh",
                height="0vh"
            ),
            rx.chakra.vstack(
                static_account_info(),
                static_data_box(
                    height="250%",
                    width="100%",
                ),
                height="100%",
                spacing="0.75vh",
                width="50%"
                ),
            rx.chakra.vstack(
                whats_new_widget(),
                github_widget(),
                height="100%",
                width="50%",
                spacing="0.75vh"
                ),
            rx.chakra.box(
                height="0vh",
                width="0vh"
                ),
            spacing="0.75vh",
            width="100%",
            height="93.25vh"
            ),
        )


class TabletIndexState(SystemHealthState):
    show_system_health_for_tablet:bool = False

    def open_system_health_for_tablet(self):
        self.show_system_health_for_tablet = True
        self.load_system_health_checker = True
    
    def close_system_health_no_params_for_tablet(self):
        self.show_system_health_for_tablet = False
        self.load_system_health_checker = False
    
    def close_system_health_for_tablet(self, discard_var=None):
        self.close_system_health_no_params_for_tablet()


def tablet_index():
    return rx.vstack(
        rx.hstack(
            empty_component(),
            rx.icon(
                tag="menu",
                color="#ffffff",
                _active={"color":"#777777"},
            ),
            rx.spacer(),
            rx.popover.root(
                rx.popover.trigger(
                    rx.chakra.image(
                        src="/health.png",
                        custom_attrs={"draggable":"false"},
                        color="WHITE", 
                        height="2vh",
                        on_click = TabletIndexState.open_system_health_for_tablet
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
                                    "Server Uptime: ",
                                    color="rgb(0, 100, 100)"
                                ),
                                rx.chakra.span(
                                    State.uptime,
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
                    on_escape_key_down=TabletIndexState.close_system_health_for_tablet,
                    on_pointer_down_outside=TabletIndexState.close_system_health_for_tablet,
                    on_focus_outside=TabletIndexState.close_system_health_for_tablet,
                    on_interact_outside=TabletIndexState.close_system_health_for_tablet
                ),
                open = TabletIndexState.show_system_health_for_tablet
            ),
            empty_component(
                width="10px"
            ),
            spacing="2",
            align="center",
            bg="BLACK",
            height="50px",
            width="100%"
        ),
        rx.vstack(
            rx.spacer(),
            rx.cond(
                State.is_logged_in,
                rx.text(State.username),
                rx.text("Anonymous")
            ),
            rx.spacer(),
            spacing="2",
            bg="rgb(16, 16, 16)",
            width="100%",
            height="80vh",
            align="center",
            color="WHITE",
        ),
        spacing="0",
        width="100%"
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index()
        ),
        rx.tablet_only(
            tablet_index()
        ),
        rx.mobile_only(
            view_under_construction()
        ),
        width="100%",
    )