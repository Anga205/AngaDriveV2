import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *
from AngaDriveV2.DBMS import *
from AngaDriveV2.common import *

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
        if self.new_collection_name == "":
            return
        new_collection_id = create_new_collection(token=self.token ,collection_name=self.new_collection_name)
        self.collection_ids.append(new_collection_id)
        self.display_my_collections.append(collection_info_for_display(new_collection_id))
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

    collection_ids: list[int] = []
    display_my_collections: list[list[str]]=[]
    def update_collections(self):
        self.collection_ids = get_collection_ids_by_account_token(self.token)
        self.display_my_collections = [collection_info_for_display(collection_id) for collection_id in self.collection_ids]

    def load_collections_page(self):
        self.load_any_page()
        self.update_collections()

    def delete_collection(self, collection_id):
        delete_collection_from_db(collection_id)
        self.collection_ids.remove(collection_id)
        self.display_my_collections = [x for x in self.display_my_collections if x[0] != collection_id]
    
    def copy_collection(self, collection_id):
        return rx.set_clipboard(f"{app_link}/collection?id={collection_id}")


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

def confirm_delete_collection_dialog(button, collection_id, collection_name):
    return rx.dialog.root(
        rx.dialog.trigger(
            button
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Confirm delete",
                color="WHITE"
                ),
            rx.dialog.description(
                rx.chakra.vstack(
                    rx.chakra.text(
                        rx.chakra.span("Are you SURE you want to delete "),
                        rx.chakra.span("'", font_weight="bold"),
                        rx.chakra.span(collection_name, font_weight="bold"),
                        rx.chakra.span("' ", font_weight="bold"),
                        rx.chakra.span("permanently?"),
                        align_items="start",
                        color="WHITE"
                    ),
                    rx.chakra.text(
                        "Warning: this action cannot be undone.",
                        align_items="start",
                        color="RED",
                    ),
                    rx.chakra.box(width="0px", height="10px"),
                    rx.chakra.hstack(
                        rx.chakra.spacer(),
                        rx.dialog.close(
                            rx.chakra.button(
                                "Delete",
                                color_scheme="red",
                                on_click = lambda: CollectionState.delete_collection(collection_id)
                            ),
                        ),
                        width="100%"
                    ),
                    width="100%",
                    align_items="start"
                ),
            ),
            bg="#0f0f0f"
        )
    )

def collection_accordian(collection_obj):   # collection_obj consists of [collection_id, collection_name, file_count, file_size, editor_count]
    card_color="#1c1c1c"
    return rx.chakra.box(
        rx.chakra.accordion(
            rx.chakra.accordion_item(
                rx.chakra.accordion_button(
                    rx.chakra.vstack(
                        rx.chakra.box(height="0px", width="170px"),
                        rx.chakra.hstack(
                            rx.chakra.text(
                                collection_obj[1], # collection name
                                font_size="30px",
                                color="WHITE"
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
                                rx.chakra.text(collection_obj[2]),
                                rx.chakra.text(collection_obj[3]),
                                rx.chakra.text(collection_obj[4]),
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
                                ),
                                collection_id=collection_obj[0],
                                collection_name=collection_obj[1]
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
                                _hover={"bg":"rgb(100, 100, 0)", "color": "rgb(255, 255, 0)"},
                                on_click= lambda: CollectionState.copy_collection(collection_obj[0])
                            ),
                            label="Share Collection"
                        ),
                        width="100%"
                    ),
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

def desktop_index():
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
                                    rx.foreach(
                                        CollectionState.display_my_collections,
                                        collection_accordian
                                    ),
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

def tablet_collection_display_accordian(collection_obj):  # collection_obj consists of [collection_id, collection_name, file_count, file_size, editor_count]
    return rx.accordion.item(
        header = collection_obj[1],
        content= rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("File Count: "),
                    rx.text("Total Size: "),
                    rx.text("Editors: "),
                    align="start"
                ),
                rx.vstack(
                    rx.text(collection_obj[2]),
                    rx.text(collection_obj[3]),
                    rx.text(collection_obj[4]),
                    align="start"
                ),
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.icon("copy"),
                    on_click= lambda: CollectionState.copy_collection(collection_obj[0]),
                    color_scheme="grass",
                    variant="soft",
                    radius="large"
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("notebook-pen"),
                    color_scheme="teal",
                    variant="soft",
                    radius="large"
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("trash-2"),
                    on_click= lambda: CollectionState.delete_collection(collection_obj[0]),
                    color_scheme="tomato",
                    variant="soft",
                    radius="large"
                ),
                rx.spacer()
            ),
            align="center",
            width="100%",
            bg="BLACK",
            padding="10px",
        ),
        bg="#120f1e",
        color="WHITE"
    )

def tablet_index():
    return rx.vstack(
        tablet_navbar("collections"),
        rx.vstack(
            rx.heading(
                "My Collections",
                color="White"
            ),
            rx.hstack(
                rx.spacer(),
                create_new_collection_dialog(
                    rx.button("Create New Collection", on_click=CollectionState.open_dialog)
                ),
                width="100%"
            ),
            rx.cond(
                CollectionState.collection_ids,
                rx.accordion.root(
                    rx.foreach(
                        CollectionState.display_my_collections,
                        tablet_collection_display_accordian
                    ),
                    width="100%",
                    collapsible=True,
                    color_scheme="gray",
                    border_color="gray",
                    border_width="1px",
                    radius='none'
                ),
                rx.vstack(
                    rx.spacer(),
                    rx.callout(
                        "You have no collections yet. Create a new collection to get started.",
                        icon="info"
                    ),
                    rx.spacer(),
                    rx.spacer(),
                    height="100vh"
                ),
            ),
            width="95%",
            align="center"
        ),
        bg="#0f0f0f",
        width="100%",
        align='center'
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index()
        ),
        rx.mobile_and_tablet(
            tablet_index(),
        ),
        width="100%",
        bg="#0f0f0f",
        style={"min-height":"100vh"}
    )