import reflex as rx
from AngaDriveV2.common import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
import reflex_chakra as rx_chakra

class LoginState(State):
    open_login_dialog_var:bool = False
    def open_dialog(self):
        self.open_login_dialog_var = True

    signup_mode:bool = False

    def set_to_signup_mode(self):
        self.signup_mode=True
        self.open_dialog()
    
    def set_to_login_mode(self):
        self.signup_mode=False
        self.open_dialog()

    login_email_id: str
    login_password: str
    is_invalid_login_email_id: bool = False
    is_invalid_login_password: bool = False
    disable_login_button: bool = True
    login_password_focus_color: str = "#3182ce"

    def update_login_button(self):
        if "" in [self.login_email_id, self.login_password]:
            self.disable_login_button = True
        elif (not self.is_invalid_login_email_id) and (not self.is_invalid_login_password):
            self.disable_login_button = False

    def set_login_email_id(self, new_text: str):
        new_text = new_text.replace(" ","")
        self.login_email_id = new_text
        if (new_text == "") or (is_valid_email(new_text)):
            self.is_invalid_login_email_id = False
        else:
            self.is_invalid_login_email_id = True
        self.update_login_button()
    
    def set_login_password(self, new_text: str):
        self.login_password = new_text.strip()
        if (self.login_password=="") or (not (len(self.login_password)<3 or len(self.login_password)>64)):
            self.is_invalid_login_password = False
            self.login_password_focus_color = "#3182ce"
        else:
            self.is_invalid_login_password = True
            self.login_password_focus_color = "#880000"
        self.update_login_button()
    


def security_tooltip(text):
    return rx.hover_card.root(
        rx.hover_card.trigger(
            text
        ),
        rx.hover_card.content(
            rx.vstack(
                rx.text("- All passwords are encrypted before being stored"),
                rx.text("- Database isnt open to the internet"),
                rx.text("- this site might be using https, depending on if i manage to figure out cloudflare SSL"),
                rx.text("- do people even read these?"),
                rx.text("- its 1am when im typing this"),
                rx_chakra.vstack(
                    rx_chakra.text("all of these on its own doesnt really mean anything, but rest assured i do try to use best practices to keep your data safe, if you are a programmer trying to understand this website, most of the encryption related stuff is in common.py, all the best!"),
                    spacing="0px",
                    font_size="10px",
                    text_align="start",
                    width="300px"
                )
            ),
            bg="#101010",
            color="GRAY"
        )
    )

class SignUpPopupState(LoginState):
    
    signup_display_name:str = ""
    signup_email:str = ""
    signup_password:str = ""
    signup_retyped_password:str = ""

    signup_is_invalid_display_name:bool = False
    signup_is_invalid_email:bool = False
    signup_is_invalid_password:bool = False
    signup_is_invalid_retyped_password:bool = False

    signup_display_name_focus_color:str = "#3182ce"
    signup_password_focus_color:str = "#3182ce"
    signup_retyped_password_focus_color:str = "#3182ce"

    disable_signup_button: bool = True
    def enable_signup_button(self):
        if "" in [self.signup_display_name,self.signup_email,self.signup_password,self.signup_retyped_password]:
            self.disable_signup_button = True
        elif True in [self.signup_is_invalid_display_name, self.signup_is_invalid_email, self.signup_is_invalid_password, self.signup_is_invalid_retyped_password]:
            self.disable_signup_button = True
        else:
            self.disable_signup_button = False

    def set_signup_display_name(self, new_text:str):
        self.signup_display_name = new_text.strip()
        if self.signup_display_name=="":
            self.signup_is_invalid_display_name = False
            self.signup_display_name_focus_color:str = "#3182ce"
        elif len(self.signup_display_name)>30 or len(self.signup_display_name)<3:
            self.signup_is_invalid_display_name = True
            self.signup_display_name_focus_color = "#880000"
        else:
            self.signup_is_invalid_display_name = False
            self.signup_display_name_focus_color:str = "#3182ce"
        self.enable_signup_button()
    
    def set_signup_email(self, new_text:str):
        self.signup_email = new_text.replace(" ","")
        if self.signup_email == "":
            self.signup_is_invalid_email = False
        elif (not is_valid_email(self.signup_email)):
            self.signup_is_invalid_email = True
        else:
            self.signup_is_invalid_email = False
        self.enable_signup_button()

    def set_signup_password(self, new_text:str):
        self.signup_password = new_text
        if self.signup_password == "":
            self.signup_is_invalid_password = False
            self.signup_password_focus_color:str = "#3182ce"
        elif len(self.signup_password)>64 or len(self.signup_password)<3:
            self.signup_is_invalid_password = True
            self.signup_password_focus_color:str = "#880000"
        else:
            self.signup_is_invalid_password = False
            self.signup_password_focus_color:str = "#3182ce"

        if (self.signup_retyped_password != "") and (self.signup_retyped_password!=self.signup_password):
            self.signup_is_invalid_retyped_password = True
            self.signup_password_focus_color:str = "#880000"

        if self.signup_retyped_password==self.signup_password:
            self.signup_is_invalid_retyped_password = False
            self.signup_password_focus_color:str = "#3182ce"

        self.enable_signup_button()

    def set_signup_retyped_password(self, new_text:str):
        self.signup_retyped_password = new_text
        if self.signup_retyped_password == "":
            self.signup_is_invalid_retyped_password = False
            self.signup_retyped_password_focus_color:str = "#3182ce"
        elif self.signup_retyped_password!=self.signup_password:
            self.signup_is_invalid_retyped_password = True
            self.signup_retyped_password_focus_color:str = "#880000"
        else:
            self.signup_is_invalid_retyped_password = self.signup_is_invalid_password
            self.signup_retyped_password_focus_color:str = self.signup_password_focus_color
        self.enable_signup_button()
    
    def close_dialog(self):
        self.login_email_id = ""
        self.login_password = ""
        self.is_invalid_login_email_id:bool = False
        self.is_invalid_login_password:bool = False
        self.signup_display_name = ""
        self.signup_email = ""
        self.signup_password = ""
        self.signup_retyped_password = ""
        self.signup_is_invalid_display_name = False
        self.signup_is_invalid_email = False
        self.signup_is_invalid_password = False
        self.signup_is_invalid_password = False
        self.update_login_button()
        self.enable_signup_button()
        self.open_login_dialog_var = False
    

class SignUpButtonState(SignUpPopupState):
    def on_click_signup_button(self):
        if email_already_exists(self.signup_email):
            return rx.window_alert("Email ID already exists!")
        else:
            user_signup(token=self.token, display_name=self.signup_display_name,email=self.signup_email, password=self.signup_password)
            self.is_logged_in = "True"
            self.update_account_info()
            self.close_dialog(None)

def signup_form():
    return rx_chakra.vstack(
        rx_chakra.box(
            height="2vh"
        ),
        rx.tooltip(
            rx_chakra.hstack(
                rx_chakra.spacer(),
                rx_chakra.input(
                    placeholder="Display name",
                    width="85%",
                    color="WHITE",
                    value = SignUpPopupState.signup_display_name,
                    is_invalid=SignUpPopupState.signup_is_invalid_display_name,
                    on_change = SignUpPopupState.set_signup_display_name,
                    error_border_color="#880000",
                    focus_border_color=SignUpPopupState.signup_display_name_focus_color
                ),
                rx_chakra.spacer(),
                width="100%",
            ),
            content="Users will be able to see your display name in your collections"
        ),
        rx_chakra.input(
            placeholder = "E-mail",
            width="85%",
            color="WHITE",
            value = SignUpPopupState.signup_email,
            is_invalid=SignUpPopupState.signup_is_invalid_email,
            on_change = SignUpPopupState.set_signup_email,
            error_border_color="#880000",
        ),
        rx_chakra.password(
            placeholder="Create a password",
            width="85%",
            color="WHITE",
            value = SignUpPopupState.signup_password,
            is_invalid = SignUpPopupState.signup_is_invalid_password,
            on_change = SignUpPopupState.set_signup_password,
            error_border_color="#880000",
            focus_border_color=SignUpPopupState.signup_password_focus_color
        ),
        rx_chakra.password(
            placeholder="Re-type password",
            width="85%",
            color="WHITE",
            value = SignUpPopupState.signup_retyped_password,
            is_invalid = SignUpPopupState.signup_is_invalid_retyped_password,
            on_change = SignUpPopupState.set_signup_retyped_password,
            error_border_color="#880000",
            focus_border_color=SignUpButtonState.signup_retyped_password_focus_color
        ),
        rx_chakra.text(
            rx_chakra.span("Disclaimer: ", font_weight="bold", as_="b"),
            rx_chakra.span("Although AngaDrive uses "),
            security_tooltip(
                rx_chakra.span("standard security practices", as_="u")
            ),
            rx_chakra.span(" to assure security, if I were you, I wouldnt use the same password for everything, especially not for a website maintained by a teenager."),
            color="RED"
        ),
        rx_chakra.hstack(
            rx_chakra.spacer(),
            rx_chakra.button(
                "Sign Up",
                color_scheme="facebook",
                is_disabled=SignUpPopupState.disable_signup_button,
                on_click=SignUpButtonState.on_click_signup_button
            ),
            width="100%",
            spacing="0px"
        ),
        spacing="1vh"
    )

class LoginSwitchState(LoginState):
    hover_card_text:str = "Transfer files after login"
    login_switch_state:bool = False
    should_it_load_switch:bool = False

    def update_login_switch(self):
        self.should_it_load_switch = does_user_have_files(self.token)
        self.login_switch_state = self.should_it_load_switch

    def switch(self, new_switch_state: bool):
        self.login_switch_state = new_switch_state
        if new_switch_state == True:
            self.hover_card_text = "Transfer files after login"
        else:
            self.hover_card_text = "DON'T transfer files after login"

def data_transfer_on_login_switch():
    switch = rx.hover_card.root(
        rx.hover_card.trigger( 
            rx_chakra.box(
                rx_chakra.switch(
                    is_checked=LoginSwitchState.login_switch_state,
                    on_change=LoginSwitchState.switch
                )
            )
        ),
        rx.hover_card.content(
            rx.text(LoginSwitchState.hover_card_text),
        )
    )
    return rx.cond(
        LoginSwitchState.should_it_load_switch,
        switch,
        rx_chakra.box(
            height="0px",
            width="0px",
            on_mount=LoginSwitchState.update_login_switch
        )
    )

class LoginButtonState(LoginSwitchState):
    def on_login_button_press(self):
        check_login = user_login(self.login_email_id, self.login_password)
        self.update_login_switch()
        if False in check_login:
            return rx.window_alert(check_login[False])
        else:
            self.open_login_dialog_var = False
            self.login_email_id = ""
            self.login_password = ""
            old_token = self.token
            self.token = check_login[True]
            self.is_logged_in = "True"
            self.update_account_info()
            if self.login_switch_state:
                migrate_files(old_token=old_token, new_token=check_login[True])
            self.update_account_data_components()

def login_form():
    return rx_chakra.vstack(
        rx_chakra.box(
            height="2vh"
        ),
        rx_chakra.input(
            placeholder="E-mail ID",
            width="85%",
            color="WHITE",
            value=LoginState.login_email_id,
            on_change=LoginState.set_login_email_id,
            error_border_color="#880000",
            is_invalid=LoginState.is_invalid_login_email_id
        ),
        rx_chakra.password(
            placeholder="Password",
            width="85%",
            color="WHITE",
            error_border_color="#880000",
            value=LoginState.login_password,
            on_change=LoginState.set_login_password,
            is_invalid=LoginState.is_invalid_login_password,
            focus_border_color=LoginState.login_password_focus_color
        ),
        rx_chakra.hstack(
            data_transfer_on_login_switch(),
            rx_chakra.spacer(),
            rx_chakra.vstack(
                rx_chakra.button(
                    "Login",
                    color_scheme="facebook",
                    is_disabled=LoginState.disable_login_button,
                    on_click = LoginButtonState.on_login_button_press
                )
            ),
            width="85%"
        ),
        spacing="1vh"
    )

def login_dialog(trigger, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger,
            **kwargs
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    LoginState.signup_mode,
                    "Sign Up",
                    "Log in"
                ),
                color="WHITE"
            ),
            rx.dialog.description(
                rx.cond(
                    LoginState.signup_mode,
                    signup_form(),
                    login_form()
                )
            ),
            bg="#0f0f0f",
            on_pointer_down_outside = SignUpPopupState.close_dialog,
            on_escape_key_down = SignUpPopupState.close_dialog
        ),
        open=LoginState.open_login_dialog_var
    )