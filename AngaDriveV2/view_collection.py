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

    def open_dialog(self):
        self.dialog_open_bool = True
    
    def close_dialog_no_inputs(self):
        self.dialog_open_bool = False
    
    def close_dialog(self, arg=None):
        self.close_dialog_no_inputs()

def add_file_to_collection_dialog(trigger, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add file(s) to collection"
            ),
            rx.dialog.description(
                rx.button("lorem ipsum dolor sit amet"),
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