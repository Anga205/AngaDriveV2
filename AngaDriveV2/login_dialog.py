import reflex as rx
from AngaDriveV2.common import *
from AngaDriveV2.State import State

class LoginState(State):
    signup_mode:bool = False

    def set_to_signup_mode(self):
        self.signup_mode=True
    
    def set_to_login_mode(self):
        self.signup_mode=False

    login_email_id:str
    login_password:str
    is_invalid_login_email_id:bool = False
    is_invalid_login_password:bool = False
    disable_login_button:bool = True

    def update_login_button(self):
        if "" in [self.login_email_id, self.login_password]:
            self.disable_login_button = True
        elif (not self.is_invalid_login_email_id) and (not self.is_invalid_login_password):
            self.disable_login_button = False

    def reset_dialog(self, is_opened):
        self.login_email_id = ""
        self.login_password = ""
        self.is_invalid_login_email_id:bool = False
        self.is_invalid_login_password:bool = False
        self.update_login_button()

    def set_login_email_id(self, new_text):
        new_text = new_text.replace(" ","")
        self.login_email_id = new_text
        if (new_text == "") or (is_valid_email(new_text)):
            self.is_invalid_login_email_id = False
        else:
            self.is_invalid_login_email_id = True
        self.update_login_button()
    
    def set_login_password(self, new_text):
        self.login_password = new_text
        if (self.login_password=="") or (not (len(self.login_password)<3 or len(self.login_password)>64)):
            self.is_invalid_login_password = False
        else:
            self.is_invalid_login_password = True
        self.update_login_button()

    def print_token(self):
        print(self.token)

def signup_form():
    return rx.text("d1")

def login_form():
    return rx.chakra.vstack(
        rx.chakra.box(
            height="2vh"
        ),
        rx.chakra.input(
            placeholder="E-mail ID",
            width="85%",
            color="WHITE",
            value=LoginState.login_email_id,
            on_change=LoginState.set_login_email_id,
            error_border_color="#880000",
            is_invalid=LoginState.is_invalid_login_email_id
        ),
        rx.chakra.password(
            placeholder="Password",
            width="85%",
            color="WHITE",
            error_border_color="#880000",
            value=LoginState.login_password,
            on_change=LoginState.set_login_password,
            is_invalid=LoginState.is_invalid_login_password
        ),
        rx.chakra.hstack(
            rx.chakra.spacer(),
            rx.cond(
                LoginState.disable_login_button,
                rx.dialog.close(
                    rx.chakra.button(
                        "Login",
                        color_scheme="facebook",
                        is_disabled=True,
                    )
                ),
                rx.chakra.button(
                    "Login",
                    color_scheme="facebook",
                    is_disabled=False,
                    on_click=LoginState.print_token
                ),
            ),
            width="85%"
        ),
        spacing="1vh"
    )

def login_dialog(trigger):
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger
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
            bg="#0f0f0f"
        ),
        on_open_change=LoginState.reset_dialog
    )