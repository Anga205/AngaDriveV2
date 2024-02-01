import reflex as rx

def card(heading, content, **kwargs):
    return rx.vstack(
        rx.heading(heading, color="BLUE", font_size="3vh"),
        content,
        border_color="black",
        border_width="1.5vh",
        border_radius="0.5vh",
        padding="1vh",
        align="center",
        color="WHITE",
        bg="BLACK",
        **kwargs
    )

def data_card(heading = "Sample heading", content="Sample content"):
    return card(
        heading, 
        rx.text(content, font_size="2.5vh", _as="b")
    )