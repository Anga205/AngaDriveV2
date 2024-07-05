import reflex as rx
from AngaDriveV2.shared_components import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
import copy


class ViewCollectionState(State):

    collection_id:str = ""
    collection_name:str=""
    collection_editors:list[str]=[]
    collection_files:list[dict[str,str]] = []
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
        self.collection_files = [get_file_info_for_card(file) for file in collection_files]

    def remove_file_from_collection(self, file_dict):
        remove_file_from_collection_db(collection_id=self.collection_id, file_path=file_dict["file_path"])
        self.collection_files.remove(file_dict)

    def delete_file_from_collection(self, file_dict):
        filename = file_dict["file_path"]
        try:
            os.remove(os.path.join(file_directory,filename))
            try:
                remove_file_from_database(filename)
            except Exception as e:
                print(f"Error occured in execuring AngaDriveV2.view_collection.ViewCollectionState.delete_file_from_collection.remove_file_from_database: {file_dict}")
        except Exception as e:
            print(f"Error occured in execuring AngaDriveV2.view_collection.ViewCollectionState.delete_file_from_collection.os_remove: {file_dict}\nError was: {e}")
        self.collection_files.remove(file_dict)

    def print_selected_files(self):
        print("hello!")


def view_collection_file_editor_menu(file_obj, **kwargs):
    return rx.chakra.hstack(
        conditional_render(
            condition=ViewCollectionState.is_collection_owner,
            true_component=rx.chakra.spacer()
        ),
        conditional_render(
            condition=ViewCollectionState.is_collection_owner,
            true_component=rx.chakra.tooltip(
                rx.chakra.button(
                    rx.chakra.icon(
                        tag="small_close"
                    ),
                    color="#ee0000",
                    bg = "#260000",
                    _hover = {"bg":"#420000","color":"#ff0000"},
                    border_radius="2vh",
                    height="30px",
                    width="15%",
                    on_click=ViewCollectionState.remove_file_from_collection(file_obj)
                ),
                label = "Remove from collection"
            )
        ),
        rx.chakra.spacer(),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.icon(
                    tag="copy"
                ),
                color="#00a799",
                bg = "#002321",
                _hover = {"bg":"#003432","color":"#11b8aa"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click = lambda: State.copy_file_link(file_obj),
            ),
            label="Copy Link"
        ),
        rx.chakra.spacer(),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.chakra.icon(
                    tag="download"
                ),
                color="#12a1fb",
                bg = "#11222f",
                _hover = {"bg":"#223340","color":"#22c9bb"},
                border_radius="2vh",
                height="30px",
                width="15%",
                on_click = State.download_file(file_obj),
            ),
            label="Download File"
        ),
        rx.chakra.spacer(),
        rx.chakra.tooltip(
            rx.chakra.button(
                rx.icon(
                    "eye",
                    width="100%",
                    height="auto",
                ),
                color="#ffb100",
                bg = "#302400",
                _hover = {"bg":"#413511","color":"#ffc200"},
                border_radius="2vh",
                height="30px",
                width="17%",
                on_click=rx.redirect(file_obj["file_link"], external=True)
            ),
            label="View file"
        ),
        rx.chakra.spacer(),
        justify_content="center",
        align_items="center",
        height="42px",
        width="100%",
        spacing="0px",
        border_color="#1c1c1c",
        **kwargs,
    ),

file_card_context_menu_wrapper = (
        lambda component, file_obj:
        rx.context_menu.root(
            rx.context_menu.trigger(
                component
            ),
            rx.cond(
                file_obj["owner_token"]==State.token,
                rx.context_menu.content(
                    rx.context_menu.item("Copy shortened path", on_click=lambda: State.copy_file_path(file_obj)),
                    rx.context_menu.item("Copy download link", on_click=lambda: State.copy_download_link(file_obj)),
                    rx.context_menu.separator(),
                    rx.context_menu.item("Delete file", on_click=ViewCollectionState.delete_file_from_collection(file_obj), color="red"),
                ),
                rx.context_menu.content(
                    rx.context_menu.item("Copy shortened path", on_click=lambda: State.copy_file_path(file_obj)),
                    rx.context_menu.item("Copy download link", on_click=lambda: State.copy_download_link(file_obj)),
                )
            )
        )
    )

def view_collection_file_card(file_dict):
    return file_card_context_menu_wrapper(
        rx.chakra.vstack(
            file_name_header(
                file_dict,
                border_radius="1vh 1vh 0vh 0vh"
            ),
            file_details(
                file_dict,
                border_radius="0vh 0vh 0vh 0vh"
            ),
            view_collection_file_editor_menu(
                file_dict,
                border_width="0vh 0.2vh 0.2vh 0.2vh",
                border_radius= "0vh 0vh 1vh 1vh"
            ),
        width="290px",
        spacing="0px"
    ),
    file_dict
)

class AddFileDialogState(ViewCollectionState):
    dialog_open_bool:bool = False
    user_files_in_collection: dict[str, bool] = []

    user_has_files_bool:bool = False
    def open_dialog(self):
        self.dialog_open_bool = True
        self.user_files = get_all_user_files_for_display(self.token)
        self.user_has_files_bool = does_user_have_files(self.token)
        self.user_files_in_collection = {x["file_path"]:(x in self.collection_files) for x in self.user_files}
        self.new_user_files_in_collection = copy.deepcopy(self.user_files_in_collection)
    
    def close_dialog(self):
        self.dialog_open_bool = False
        self.display_add_files_button:bool = False
        return rx.clear_selected_files("view_collection_upload")

    new_user_files_in_collection: dict[str, bool] = {}
    def change_file_status(self, file_path:str, status:bool):
        self.new_user_files_in_collection[file_path] = status
        self.update_add_files_button()

    display_add_files_button:bool = False
    def update_add_files_button(self):
        if self.new_user_files_in_collection != self.user_files_in_collection:
            self.display_add_files_button = True
        else:
            self.display_add_files_button = False
    
    async def upload_file_to_collection(self, files: list[rx.UploadFile]):
        filenames = []
        for file in files:
            upload_data = await file.read()
            filename = gen_filename(file.filename)
            filenames.append(filename)
            outfile = os.path.join(file_directory,filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            add_file_to_database(
                account_token=self.token,
                file_directory=filename,
                file_size=get_file_size(outfile),
                original_file_name=file.filename
            )
            add_file_to_collection(collection_id=self.collection_id, file_path=filename)
        self.close_dialog()
        self.load_collection_viewer()

    def save_changes(self):
        new_user_files_in_collection = self.new_user_files_in_collection
        old_user_files_in_collection = self.user_files_in_collection
        for i in new_user_files_in_collection:
            if new_user_files_in_collection[i] and not old_user_files_in_collection[i]:
                add_file_to_collection(collection_id=self.collection_id, file_path=i)
                self.collection_files.append(get_file_info_for_card(i))
            elif not new_user_files_in_collection[i] and old_user_files_in_collection[i]:
                remove_file_from_collection_db(collection_id=self.collection_id, file_path=i)
                self.collection_files.remove(get_file_info_for_card(i))
        self.close_dialog()

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
        rx.checkbox(
            checked=AddFileDialogState.new_user_files_in_collection[file_obj["file_path"]],
            on_change=lambda update: AddFileDialogState.change_file_status(file_obj["file_path"],update),
        ),
        rx.hover_card.root(
            rx.hover_card.trigger(
                rx.text(file_obj["original_name"])
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
                        id="view_collection_upload",
                    ),
                    rx.cond(
                        rx.selected_files("view_collection_upload"),
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                "Upload",
                                color_scheme="green",
                                variant="soft",
                                on_click=AddFileDialogState.upload_file_to_collection(rx.upload_files(upload_id="view_collection_upload"))
                            ),
                            width="100%"
                        ),
                        rx.box(
                            width="0px",
                            height="0px"
                        )
                    ),
                    rx.cond(
                        AddFileDialogState.user_has_files_bool,
                        add_files_accordion(),
                        rx.box(
                            width="0px",
                            height="0px" 
                        )
                    )
                )
            ),
            on_interact_outside=lambda x: AddFileDialogState.close_dialog(),
            on_escape_key_down=lambda x: AddFileDialogState.close_dialog(),
            on_pointer_down_outside=lambda x: AddFileDialogState.close_dialog(),
            bg="#0f0f0f"
        ),
        open=AddFileDialogState.dialog_open_bool
    )

def add_files_accordion():
    return rx.vstack(
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
                value="item1"
            ),
            collapsible=True,
            color_scheme="indigo",
            width="100%",
        ),
        rx.cond(
            AddFileDialogState.display_add_files_button,
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Save Changes",
                    color_scheme="blue",
                    variant="soft",
                    on_click = AddFileDialogState.save_changes
                ),
                width="100%"
            ),
            rx.chakra.box(
                width="0px",
                height="0px"
            )
        ),
        width="100%"
    )


def desktop_index():
    return rx.chakra.vstack(
        shared_navbar(),
        rx.chakra.hstack(
            rx.cond(
                ViewCollectionState.collection_name,
                rx.chakra.tooltip(
                    rx.checkbox(),
                    label="Album View"
                ),
                rx.box(
                    width="0px",
                    height="0px"
                )
            ),
            rx.chakra.spacer(),
            rx.cond(
                ViewCollectionState.is_collection_owner,
                rx.chakra.editable(
                    rx.chakra.editable_preview(),
                    rx.chakra.editable_input(),
                    placeholder=ViewCollectionState.collection_name,
                    color="WHITE",
                    font_size="3vh",
                    style={"font-weight":"bold"},
                ),
                rx.chakra.text(
                    ViewCollectionState.collection_name,
                    color="WHITE",
                    font_size="3vh",
                    as_ = "b"
                ),
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
                    view_collection_file_card
                ),
            ),
            rx.chakra.box(
                width = "20px"
            ),
            spacing="0px",
        ),
        rx.chakra.box(
            height="20px"
        ),
        spacing="5px",
        bg = "#0f0f0f",
        style={"min-height":"100vh"},
        width="100%"
    )


def mobile_view():
    return rx.vstack(
        tablet_navbar("collection-viewer"),
        rx.heading(
            ViewCollectionState.collection_name,
            color="WHITE",
            style={"font-weight":"bold"}
        ),
        rx.button(
            "Add Files",
            color_scheme="green",
            variant="solid",
            on_click=AddFileDialogState.open_dialog
        ),
        bg="#0f0f0f",
        style={"min-height":"100vh"},
        align="center"
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index(),
        ),
        rx.mobile_and_tablet(
            mobile_view()
        ),
        width="100%",
        bg="#0f0f0f"
    )