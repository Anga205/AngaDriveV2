import reflex
from AngaDriveV2.State import State

rx = reflex.chakra

def index():
    return rx.vstack(
        rx.spacer(),
        rx.heading("404 | Page not found"),
        rx.text("Oops! looks like you have wandered too far!"),
        rx.text("Dont worry though, you will be redirected back to homepage soon.."),
        rx.text("Large parts of the website may not be functional yet, because it is still in development"),
        rx.spacer(),
        height="100vh",
        width="100%",
        on_mount=State.page_not_found_redirect_back_to_home_page
    )