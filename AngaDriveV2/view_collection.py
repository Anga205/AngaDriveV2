import reflex as rx
from AngaDriveV2.shared_components import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *


class ViewCollectionState(State):

    collection_id:str = ""
    collection_name:str=""
    collection_editors:list[str]=[]
    collection_sounds:list[list[str]] = []
    collection_images:list[list[str]] = []
    collection_videos:list[list[str]] = []
    collection_documents:list[list[str]] = []
    collection_files:list[list[str]] = []
    is_collection_owner:bool = False
    def load_collection_viewer(self):
        self.load_any_page()
        self.collection_id = self.router.page.params.get("id",None)
        if self.collection_id==None:
            return rx.redirect("/my_collections")
        collection_data = get_collection_info_for_viewer(self.collection_id)
        if collection_data==None:
            return rx.redirect("/my_collections")
        self.collection_name = collection_data["name"]
        self.collection_editors = collection_data["editors"]
        self.is_collection_owner = self.token in collection_data["editors"]
        collection_files = collection_data["data"]["Files"]
        self.collection_sounds = [get_file_info_for_card(x) for x in collection_files if x[0].split(".")[-1] in ["mp3","wav","ogg"]]
        self.collection_videos = [get_file_info_for_card(x) for x in collection_files if x[0].split(".")[-1] in ["mp4","webm","mkv","mov"]]
        self.collection_images = [get_file_info_for_card(x) for x in collection_files if x[0].split(".")[-1] in ["jpg","jpeg","png","gif","bmp","svg"]]
        self.collection_files = [get_file_info_for_card(x) for x in collection_files]
        self.collection_documents = [get_file_info_for_card(x) for x in self.collection_files if x not in [*self.collection_sounds, *self.collection_videos, *self.collection_images]]

class AddFileDialogState(ViewCollectionState):
    dialog_open_bool:bool = False

    user_files_bool:bool = False
    def open_dialog(self):
        self.dialog_open_bool = True
        if self.user_files==[]:
            self.user_files = get_all_user_files_for_display(self.token)
        self.user_files_bool = does_user_have_files(self.token)
    
    def close_dialog(self, arg=None):
        self.dialog_open_bool = False
        rx.clear_selected_files("view_collection_upload")
    
    selected_files:list[str] = []

def file_hovercard(file_obj):
    return rx.chakra.vstack(
        file_name_header(
            file_obj,
            border_radius="1vh 1vh 0vh 0vh"
        ),
        file_details(
            file_obj,
            border_radius="0vh 0vh 1vh 1vh"
        ),
        spacing="0px",
        width="290px"
    )

def file_selection_checkbox(file_obj):
    return rx.hstack(
        rx.checkbox(),
        rx.hover_card.root(
            rx.hover_card.trigger(
                rx.text(file_obj[0])
            ),
            rx.hover_card.content(
                file_hovercard(file_obj),
                bg="#000000"
            )
        )
    )

def add_file_to_collection_dialog(trigger, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add file(s) to collection",
                color="WHITE"
            ),
            rx.dialog.description(
                rx.vstack(
                    rx.upload(
                        rx.cond(
                            rx.selected_files("view_collection_upload"),
                            rx.chakra.vstack(
                                rx.chakra.box(
                                    height="5vh"
                                ),
                                rx.foreach(
                                    rx.selected_files("view_collection_upload"),
                                    rx.chakra.text
                                ),
                                rx.chakra.box(
                                    height="5vh"
                                )
                            ),
                            rx.chakra.vstack(
                                rx.spacer(),
                                rx.chakra.text("Drag and drop files here or click to select files"),
                                rx.spacer(),
                                height="15vh"
                            ),
                        ),
                        display='flex',
                        width="100%",
                        color="WHITE",
                        justify_content= 'center',
                        align_items= 'center',
                        border="1px dotted #0000ff",
                        id="view_collection_upload"
                    ),
                    rx.chakra.hstack(
                        rx.chakra.divider(),
                        rx.chakra.text("OR", color="GRAY"),
                        rx.chakra.divider(),
                        width="100%",
                        border_color="GRAY"
                    ),
                    rx.accordion.root(
                        rx.accordion.item(
                            header="Add existing files",
                            content=rx.scroll_area(
                                rx.vstack(
                                    rx.foreach(
                                        State.user_files,
                                        file_selection_checkbox
                                    ),
                                    style={"height":200}
                                ),
                                bg="#111111",
                                padding="10px",
                                border_radius="5px"
                            ),
                        ),
                        collapsible=True,
                        color_scheme="indigo",
                        width="100%",
                    )
                )
            ),
            on_interact_outside=AddFileDialogState.close_dialog,
            on_escape_key_down=AddFileDialogState.close_dialog,
            on_pointer_down_outside=AddFileDialogState.close_dialog,
            bg="#0f0f0f"
        ),
        open=AddFileDialogState.dialog_open_bool
    )

def index():
    return rx.chakra.vstack(
        shared_navbar(),
        rx.chakra.hstack(
            rx.chakra.tooltip(
                rx.checkbox(),
                label="Album View"
            ),
            rx.chakra.spacer(),
            rx.chakra.heading(
                ViewCollectionState.collection_name,
                color="WHITE"
            ),
            rx.cond(
                ViewCollectionState.is_collection_owner,
                rx.chakra.icon(
                    tag="edit",
                    color="WHITE",
                ),
                rx.chakra.box(height="0px", width="0px")
            ),
            rx.chakra.spacer(),
            rx.cond(
                ViewCollectionState.is_collection_owner,
                add_file_to_collection_dialog(
                    rx.chakra.button(
                        rx.chakra.icon(
                            tag="plus_square",
                            color="WHITE"
                        ),
                        rx.chakra.box(
                            width="3px"
                        ),
                        "Add Files",
                        color="WHITE",
                        size="sm",
                        bg="GREEN",
                        _hover = {"bg":"rgb(0,255,0)","color":"rgb(100,100,100)"},
                        on_click=AddFileDialogState.open_dialog
                    )
                ),
                rx.chakra.box(
                    width="0px",
                    height="0px"
                )
            ),
            width="95%"
        ),
        rx.chakra.hstack(
            rx.chakra.box(
                width = "20px"
            ),
            rx.chakra.wrap(
                rx.foreach(
                    ViewCollectionState.collection_files,
                    file_card
                ),
            ),
            rx.chakra.box(
                width = "20px"
            ),
            spacing="0px",
            width="100%",
        ),
        rx.chakra.box(
            height="20px"
        ),
        spacing="5px",
        bg = "#0f0f0f",
        height="100vh",
        width="100%"
    )