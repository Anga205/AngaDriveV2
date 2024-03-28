import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *
from AngaDriveV2.DBMS import *

class CollectionState(State):
    new_collection_name:str = ""
    is_invalid_collection_name:bool = False
    new_collection_input_border_color:str="#3182ce"
    show_create_button:bool = False

    def check_if_show_button(self):
        if ("" != self.new_collection_name) or (not self.is_invalid_collection_name):
            self.show_create_button = True
        if self.is_invalid_collection_name or (""==self.new_collection_name):
            self.show_create_button = False

    def set_new_collection_name(self, new_name:str):
        new_name = new_name.strip()
        self.new_collection_name = new_name
        if (new_name == "") or len(new_name)>2:
            self.is_invalid_collection_name = False
            self.new_collection_input_border_color ="#3182ce"
        elif len(new_name)<=2:
            self.is_invalid_collection_name = True
            self.new_collection_input_border_color = "#880000"
        self.check_if_show_button()
        
    def create_new_collection_button_click(self):
        create_new_collection(token=self.token ,collection_name=self.new_collection_name)
        self.close_dialog()
        
    
    open_new_collection_dialog:bool = False

    def open_dialog(self):
        self.open_new_collection_dialog = True
    
    def close_dialog(self, junk_value=False):
        self.new_collection_name=""
        self.show_create_button = False
        self.open_new_collection_dialog = False

    def close_dialog_no_inputs(self):
        self.close_dialog()


def create_new_collection_dialog(button):
    return rx.dialog.root(
        rx.dialog.trigger(
            button
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Create new Collection",
                color="WHITE"
                ),
            rx.dialog.description(
                rx.chakra.vstack(
                    rx.chakra.input(
                        placeholder="Enter collection name...",
                        max_length="128",
                        color="WHITE",
                        on_change=CollectionState.set_new_collection_name,
                        is_invalid=CollectionState.is_invalid_collection_name,
                        focus_border_color=CollectionState.new_collection_input_border_color,
                        width="85%"
                    ),
                    rx.box(height="10px"),
                    rx.cond(
                        CollectionState.show_create_button,
                        rx.chakra.hstack(
                            rx.chakra.spacer(),
                            rx.chakra.button(
                                "Create",
                                color_scheme="facebook",
                                border_radius="10px",
                                variant="outline",
                                on_click = CollectionState.create_new_collection_button_click
                            ),
                            width="100%"
                        ),
                        rx.box(
                            width="0px", 
                            height="0px"
                        )
                    ),
                    width="100%"
                )
            ),
            bg="#0f0f0f",
            on_pointer_down_outside = CollectionState.close_dialog,
            on_escape_key_down = CollectionState.close_dialog
        ),
        open = CollectionState.open_new_collection_dialog
    )


def confirm_delete_collection_dialog(button):
    return rx.dialog.root(
        rx.dialog.trigger(
            button
        ),
        rx.dialog.content(
            rx.dialog.title("Confirm delete"),
            rx.dialog.description(
                rx.chakra.vstack(
                    rx.chakra.text(
                        rx.chakra.span("Are you SURE you want to delete "),
                        rx.chakra.span("'", font_weight="bold"),
                        rx.chakra.span("Collection1 name", font_weight="bold"),
                        rx.chakra.span("' ", font_weight="bold"),
                        rx.chakra.span("permanently?"),
                        align_items="start"
                    ),
                    rx.chakra.text(
                        "Warning: this action cannot be undone.",
                        align_items="start",
                        color="RED",
                    ),
                    width="100%",
                    align_items="start"
                )
            )
        )
    )


def collection_accordian():
    card_color="#1c1c1c"
    return rx.chakra.box(
        rx.chakra.accordion(
            rx.chakra.accordion_item(
                rx.chakra.accordion_button(
                    rx.chakra.vstack(
                        rx.chakra.hstack(
                            rx.chakra.text(
                                "Collection1 name",
                                font_size="30px"
                            ),
                            rx.chakra.accordion_icon(),
                        ),
                        rx.chakra.divider(
                            border_color="GRAY"
                        ),
                        rx.chakra.box(
                            height="10px"
                        ),
                        rx.chakra.hstack(
                            rx.chakra.vstack(
                                rx.chakra.text("File Count: "),
                                rx.chakra.text("Total Size: "),
                                rx.chakra.text("Editors: "),
                                spacing="5px",
                                align_items="start"
                            ),
                            rx.chakra.vstack(
                                rx.chakra.text("72"),
                                rx.chakra.text("1.2 GB"),
                                rx.chakra.text("12"),
                                spacing="5px",
                                align_items="start",
                            ),
                            font_size="15px",
                            color="#bbbbbb",
                            spacing="10px"
                        ),
                        spacing="0vh"
                    )
                ),
                rx.chakra.accordion_panel(
                    rx.chakra.hstack(
                        rx.chakra.tooltip(
                            rx.chakra.button(
                                rx.chakra.icon(
                                    tag="edit",
                                    font_size="20px"
                                ),
                                height="30px",
                                width="40px",
                                border_radius="15px",
                                bg="rgb(0, 75, 75)",
                                color="rgb(0, 200, 200)",
                                _hover={"bg":"rgb(0, 100, 100)", "color": "rgb(0, 255, 255)"}
                            ),
                            label="Edit Files"
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.tooltip(
                            confirm_delete_collection_dialog(
                                rx.chakra.button(
                                    rx.chakra.icon(
                                        tag="delete",
                                        font_size="20px"
                                    ),
                                    height="30px",
                                    width="40px",
                                    border_radius="15px",
                                    bg="rgb(75, 0, 0)",
                                    color="rgb(200, 0, 0)",
                                    _hover={"bg":"rgb(100, 0, 0)", "color": "rgb(255, 0, 0)"}
                                )
                            ),
                            label="Delete Collection"
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.tooltip(
                            rx.chakra.button(
                                rx.chakra.icon(
                                    tag="copy",
                                    font_size="20px"
                                ),
                                height="30px",
                                width="40px",
                                border_radius="15px",
                                bg="rgb(75, 0, 75)",
                                color="rgb(200, 0, 200)",
                                _hover={"bg":"rgb(100, 100, 0)", "color": "rgb(255, 255, 0)"}
                            ),
                            label="Share Collection"
                        ),
                        width="100%"
                    )
                )
            ),
            allow_toggle=True,
            border_color=card_color
        ),
        bg=card_color,
        border_color=card_color,
        border_radius="5px",
        border_width="5px"
    )

def context_menu_wrapper(*components):
    return create_new_collection_dialog(
        rx.context_menu.root(
            rx.context_menu.trigger(
                *components
            ),
            rx.context_menu.content(
                rx.context_menu.item(
                    "New Collection",
                    on_click=CollectionState.open_dialog
                )
            )
        )
    )

def index():
    return site_template(
        "Collections",
        context_menu_wrapper(
            rx.chakra.vstack(
                rx.chakra.hstack(
                    rx.chakra.tabs(
                        rx.chakra.tab_list(
                            rx.chakra.tab("My Collections"),
                            rx.chakra.tab("Shared with me"),
                        ),
                        rx.chakra.tab_panels(
                            rx.chakra.tab_panel(
                                rx.chakra.box(
                                    height="2vh"
                                    ),
                                rx.chakra.wrap(
                                    collection_accordian(),
                                    width="100%"
                                ),
                                spacing="0vh"
                            ),
                            rx.chakra.tab_panel(
                                rx.chakra.text("test2")
                            ),
                        ),
                        color="WHITE",
                        width="100%",
                        variant="line",
                        color_scheme="cyan",
                        height="100%",
                        is_fitted=True
                    ),
                    width="100%",
                    height="100%",
                ),
                width="100%",
                height="100%"
            )
        )
    )