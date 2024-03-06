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
                rx.chakra.vstack(
                    rx.chakra.text("all of these on its own doesnt really mean anything, but rest assured i do try to use best practices to keep your data safe, if you are a programmer trying to understand this website, most of the encryption related stuff is in common.py, all the best!"),
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

def signup_form():
    return rx.chakra.vstack(
        rx.chakra.box(
            height="2vh"
        ),
        rx.chakra.input(
            placeholder="Display name",
            width="85%",
            color="WHITE",
        ),
        rx.chakra.input(
            placeholder = "E-mail",
            width="85%",
            color="WHITE"
        ),
        rx.chakra.password(
            placeholder="Create a password",
            width="85%",
            color="WHITE"
        ),
        rx.chakra.password(
            placeholder="Re-type password",
            width="85%",
            color="WHITE"
        ),
        rx.chakra.text(
            rx.chakra.span("Disclaimer: ", font_weight="bold", as_="b"),
            rx.chakra.span("Although AngaDrive uses "),
            security_tooltip(
                rx.chakra.span("standard security practices", as_="u")
            ),
            rx.chakra.span(" to assure security, if I were you, I wouldnt use the same password for everything, especially not for a website maintained by a teenager."),
            color="RED"
        ),
        spacing="1vh"
    )

def data_transfer_on_login_switch():
    return rx.hover_card.root(
        rx.hover_card.trigger( 
            rx.chakra.switch(
                is_checked=True,
            )
        ),
        rx.hover_card.content(
            rx.text("Transfer files after login"),
        )
    )

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
            data_transfer_on_login_switch(),
            rx.chakra.spacer(),
            rx.cond(
                LoginState.disable_login_button,
                rx.chakra.button(
                    "Login",
                    color_scheme="facebook",
                    is_disabled=True,
                ),
                rx.dialog.close(
                    rx.chakra.button(
                        "Login",
                        color_scheme="facebook",
                        is_disabled=False,
                        on_click=LoginState.print_token
                    )
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