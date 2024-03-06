import reflex as rx

class LoginState(rx.State):
    signup_mode:bool = False

    def set_to_signup_mode(self):
        self.signup_mode=True
    
    def set_to_login_mode(self):
        self.signup_mode=False
    

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
                )
            )
        )
    )