import reflex as rx

class LoginState(rx.State):
    signup_mode:bool = False

    def set_to_signup_mode(self):
        self.signup_mode=True
    
    def set_to_login_mode(self):
        self.signup_mode=False


def signup_form():
    return rx.text("d1")

def login_form():
    return rx.chakra.vstack(
        rx.chakra.box(
            height="3vh"
        ),
        rx.chakra.input(
            placeholder="E-mail ID",
            width="85%",
            color="WHITE",
            is_invalid=True,
            error_border_color="#880000"
        ),
        rx.chakra.box(
            height="1vh"
        ),
        rx.chakra.password(
            placeholder="Password",
            width="85%",
            color="WHITE"
        ),
        spacing="0px"
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
        )
    )