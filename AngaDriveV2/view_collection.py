import reflex as rx
from AngaDriveV2.shared_components import *
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *
import copy
import reflex_chakra as rx_chakra


class ViewCollectionState(State):

    collection_id:str = ""
    collection_name:str=""
    collection_editors:list[str]=[]
    collection_files:list[dict[str,str]] = []
    collection_folders:list[dict[str,str]] = []
    is_collection_owner:bool = False
    has_both_folders_and_files:bool

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
        collection_files = collection_data["Files"]
        collection_folders = collection_data["Folders"]
        self.collection_files = [get_file_info_for_card(file) for file in collection_files]
        self.collection_folders = [collection_info_for_display(folder) for folder in collection_folders]
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)

    def remove_file_from_collection(self, file_dict):
        remove_file_from_collection_db(collection_id=self.collection_id, file_path=file_dict["file_path"])
        self.collection_files.remove(file_dict)
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)

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
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)
    
    def copy_collection_link(self, collection_dict):
        yield rx.set_clipboard(f"{app_link}/collection/?id={collection_dict['id']}")
        yield rx.toast.success(f"Copied link to {collection_dict['full_name']}")


def view_collection_file_editor_menu(file_obj, **kwargs):
    return rx_chakra.hstack(
        conditional_render(
            condition=ViewCollectionState.is_collection_owner,
            true_component=rx_chakra.spacer()
        ),
        conditional_render(
            condition=ViewCollectionState.is_collection_owner,
            true_component=rx_chakra.tooltip(
                rx_chakra.button(
                    rx_chakra.icon(
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
        rx_chakra.spacer(),
        rx_chakra.tooltip(
            rx_chakra.button(
                rx_chakra.icon(
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
        rx_chakra.spacer(),
        rx_chakra.tooltip(
            rx_chakra.button(
                rx_chakra.icon(
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
        rx_chakra.spacer(),
        rx_chakra.tooltip(
            rx_chakra.button(
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
        rx_chakra.spacer(),
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
        rx.vstack(
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
        spacing="0"
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
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)
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
        yield self.close_dialog()
        yield self.load_collection_viewer()

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
    return rx_chakra.vstack(
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
                            rx_chakra.vstack(
                                rx_chakra.box(
                                    height="5vh"
                                ),
                                rx.foreach(
                                    rx.selected_files("view_collection_upload"),
                                    rx_chakra.text
                                ),
                                rx_chakra.box(
                                    height="5vh"
                                )
                            ),
                            rx_chakra.vstack(
                                rx.spacer(),
                                rx_chakra.text("Drag and drop files here or click to select files"),
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
        rx_chakra.hstack(
            rx_chakra.divider(),
            rx_chakra.text("OR", color="GRAY"),
            rx_chakra.divider(),
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
            rx_chakra.box(
                width="0px",
                height="0px"
            )
        ),
        width="100%"
    )

class AddFolderDialogState(ViewCollectionState):
    dialog_open_bool:bool = False
    new_collection_name:str = ""
    new_collection_name_is_valid:bool = False
    user_folders:list[dict[str,str]] = []
    user_folders_in_collection: dict[str, bool] = []
    user_updated_folders_in_collection: dict[str, bool] = {}

    def open_dialog(self):
        collection_ids = get_collection_ids_by_account_token(self.token)
        collection_ids.remove(self.collection_id)           # remove the id of the collection that user is currently viewing
        self.user_folders=[collection_info_for_display(folder) for folder in collection_ids]
        list_of_collection_folder_ids = [folder["id"] for folder in self.collection_folders]
        self.user_folders_in_collection={collection_id:bool(collection_id in list_of_collection_folder_ids) for collection_id in collection_ids}
        self.user_updated_folders_in_collection = copy.deepcopy(self.user_folders_in_collection)
        self.dialog_open_bool = True
    
    def close_dialog(self):
        self.input_border_color = "BLUE"
        self.new_collection_name = ""
        self.new_collection_name_is_valid = False
        self.dialog_open_bool = False
        self.enable_save_folder_changes_button = False
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)

    input_border_color="BLUE"
    def assess_input(self, new_input: str):
        self.new_collection_name = new_input.strip()
        if (self.new_collection_name=="") or (len(new_input)>2):
            self.input_border_color = "BLUE"
            self.new_collection_name_is_valid = bool(self.new_collection_name) # If the input is empty, the name is invalid
            return
        self.input_border_color = "RED"


    def create_folder(self):
        if self.new_collection_name_is_valid:
            new_collection_id = create_new_collection(user_token=self.token, collection_name=self.new_collection_name)
            add_folder_to_collection(folder_id=new_collection_id, collection_id=self.collection_id)
            self.collection_folders.append(collection_info_for_display(new_collection_id))
            self.close_dialog()

    enable_save_folder_changes_button:bool = False
    def update_checkbox(self, folder_id):
        self.user_updated_folders_in_collection[folder_id] = not self.user_updated_folders_in_collection[folder_id]
        if self.user_folders_in_collection != self.user_updated_folders_in_collection:
            self.enable_save_folder_changes_button = True
        else:
            self.enable_save_folder_changes_button = False
    
    def folder_accordion_save_changes(self):
        new_folders = self.user_updated_folders_in_collection
        old_folders = self.user_folders_in_collection
        for i in new_folders:
            if new_folders[i] and not old_folders[i]:
                add_folder_to_collection(folder_id=i, collection_id=self.collection_id)
                self.collection_folders.append(collection_info_for_display(i))
            elif (not new_folders[i]) and old_folders[i]:
                remove_folder_from_collection(folder_id=i, collection_id=self.collection_id)
                self.collection_folders.remove(collection_info_for_display(i))
        self.close_dialog()
    
    def remove_folder_from_collection(self, folder_obj):
        remove_folder_from_collection(folder_id=folder_obj['id'], collection_id=self.collection_id)
        self.collection_folders.remove(folder_obj)
        self.has_both_folders_and_files = bool(self.collection_folders) and bool(self.collection_files)
        return rx.toast.error(f"Removed folder from collection")

def add_folders_accordion():
    return rx.vstack(
        rx_chakra.hstack(
            rx_chakra.divider(),
            rx_chakra.text("OR"),
            rx_chakra.divider(),
            color="GRAY",
            border_color="GRAY",
            width="100%"
        ),
        rx.accordion.root(
            rx.accordion.item(
                header="Add existing folders",
                content=rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            AddFolderDialogState.user_folders,
                            lambda folder: rx.hstack(
                                rx.checkbox(
                                    checked=AddFolderDialogState.user_updated_folders_in_collection[folder["id"]],
                                    on_change=lambda update: AddFolderDialogState.update_checkbox(folder["id"]),
                                ),
                                rx.text(
                                    folder["full_name"],
                                    color="WHITE",
                                    on_click=lambda: AddFolderDialogState.update_checkbox(folder["id"])
                                )
                            )
                        ),
                        style={"max-height":'100px'}
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
        conditional_render(
            AddFolderDialogState.enable_save_folder_changes_button,
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Save Changes",
                    color_scheme="blue",
                    variant="soft",
                    on_click=AddFolderDialogState.folder_accordion_save_changes
                ),
                width="100%"
            )
        ),
        width='100%'
    )


def add_folder_dialog(trigger, **kwargs):
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Create new collection",
                color="WHITE"
            ),
            rx.dialog.description(
                rx.vstack(
                    rx_chakra.input(
                        bg="#0f0f0f",
                        color="GRAY",
                        placeholder="Collection name",
                        border_color=AddFolderDialogState.input_border_color,
                        focus_border_color=AddFolderDialogState.input_border_color,
                        on_change=AddFolderDialogState.assess_input,
                        border_width="1px",
                        value=AddFolderDialogState.new_collection_name,
                    ),
                    conditional_render(
                        AddFolderDialogState.new_collection_name_is_valid,
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                "Create folder",
                                variant="soft",
                                color_scheme="blue",
                                on_click=AddFolderDialogState.create_folder
                            ),
                            width="100%"
                        )
                    ),
                    conditional_render(
                        AddFolderDialogState.user_folders,
                        add_folders_accordion()
                    ),
                ),
            ),
            on_interact_outside=lambda x: AddFolderDialogState.close_dialog(),
            on_escape_key_down=lambda x: AddFolderDialogState.close_dialog(),
            on_pointer_down_outside=lambda x: AddFolderDialogState.close_dialog(),
            bg="#0f0f0f"
        ),
        open=AddFolderDialogState.dialog_open_bool
    )


def desktop_index():
    return rx_chakra.vstack(
        shared_navbar(),
        rx_chakra.hstack(
            rx_chakra.spacer(),
            rx.cond(
                ViewCollectionState.is_collection_owner,
                rx_chakra.editable(
                    rx_chakra.editable_preview(),
                    rx_chakra.editable_input(),
                    placeholder=ViewCollectionState.collection_name,
                    color="WHITE",
                    font_size="3vh",
                    style={"font-weight":"bold"},
                ),
                rx_chakra.text(
                    ViewCollectionState.collection_name,
                    color="WHITE",
                    font_size="3vh",
                    as_ = "b"
                ),
            ),
            rx_chakra.spacer(),
            conditional_render(
                ViewCollectionState.is_collection_owner,
                rx.hstack(
                    add_folder_dialog(
                        rx.button(
                            rx.icon("folder-plus"),
                            "Add folder",
                            color_scheme="indigo",
                            on_click=AddFolderDialogState.open_dialog
                        )
                    ),
                    add_file_to_collection_dialog(
                        rx.button(
                            rx.icon(
                                tag="file-plus-2",
                                height="60%"
                            ),
                            "Add Files",
                            on_click=AddFileDialogState.open_dialog,
                            color="WHITE",
                            bg="GREEN",
                            _hover = {"bg":"rgb(0,255,0)","color":"rgb(100,100,100)"},
                        )
                    )
                )
            ),
            width="95%"
        ),
        conditional_render(
            ViewCollectionState.has_both_folders_and_files,
            rx.hstack(
                rx_chakra.divider(),
                rx.text(
                    "Folders",
                ),
                rx_chakra.divider(),
                border_color="gray",
                align="center",
                width="100%",
                padding="20px",
                color="gray",
            )
        ),
        rx.flex(
            rx.foreach(
                ViewCollectionState.collection_folders,
                lambda collection_obj: desktop_collection_card(
                    collection_obj, 
                    copy_function=ViewCollectionState.copy_collection_link(collection_obj),
                    button3=rx_chakra.tooltip(
                        rx.button(
                            rx.icon(
                                "circle-x"
                            ),
                            color_scheme="tomato",
                            variant="soft",
                            radius="large",
                            on_click=AddFolderDialogState.remove_folder_from_collection(collection_obj)
                        ),
                        label="Remove folder from collection"
                    ),
                    button3_condition=ViewCollectionState.is_collection_owner
                )
            ),
            spacing="2",
            justify="center",
            width="100%",
            wrap="wrap"
        ),
        conditional_render(
            ViewCollectionState.has_both_folders_and_files,
            rx.hstack(
                rx_chakra.divider(),
                rx.text(
                    "Files",
                ),
                rx_chakra.divider(),
                border_color="gray",
                align="center",
                color="gray",
                width="100%",
                padding="20px"
            ),
        ),
        rx.hstack(
            rx.flex(
                rx.foreach(
                    ViewCollectionState.collection_files,
                    view_collection_file_card
                ),
                wrap="wrap",
                spacing='3',
                justify="center",
            ),
            padding="20px",
            spacing="0",
        ),
        rx_chakra.box(
            height="20px"
        ),
        spacing="5px",
        bg = "#0f0f0f",
        style={"min-height":"100vh"},
        width="100%"
    )


def tablet_collection_display_accordian(collection_obj):  # collection_obj consists of {"id","name","full_name","file_count","size","editor_count","folder_count"}
    return rx.accordion.item(
        header = collection_obj["name"],
        content= rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("File Count: "),
                    rx.text("Total Size: "),
                    rx.text("Editors: "),
                    align="start"
                ),
                rx.vstack(
                    rx.text(collection_obj["file_count"]),
                    rx.text(collection_obj["size"]),
                    rx.text(collection_obj["editor_count"]),
                    align="start"
                ),
            ),
            rx.hstack(
                rx.spacer(),
                rx.link(
                    rx.button(
                        rx.icon("eye"),
                        bg = "#302400",
                        color="#ffb100",
                        _hover = {"bg":"#413511","color":"#ffc200"},
                        variant="soft",
                        radius="large"
                    ),
                    href=f"{app_link}/collection?id={collection_obj['id']}",
                    target="_blank"
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("copy"),
                    on_click= ViewCollectionState.copy_collection_link(collection_obj),
                    color_scheme="lime",
                    variant="soft",
                    radius="large"
                ),
                conditional_render(
                    ViewCollectionState.is_collection_owner,
                    rx.spacer()
                ),
                conditional_render(
                    ViewCollectionState.is_collection_owner,
                    rx.button(
                        rx.icon("circle-x"),
                        color_scheme="tomato",
                        on_click=AddFolderDialogState.remove_folder_from_collection(collection_obj),
                        variant="soft",
                        radius="large"
                    )
                )
            ),
            align="center",
            width="100%",
            bg="BLACK",
            padding="10px",
        ),
        bg="#120f1e",
        color="WHITE",
        value=collection_obj["id"]
    )





def mobile_view():
    return rx.vstack(
        tablet_navbar("collection-viewer"),
        rx.heading(
            ViewCollectionState.collection_name,
            color="WHITE",
            style={"font-weight":"bold"}
        ),
        conditional_render(
            ViewCollectionState.is_collection_owner,
            rx.hstack(
                rx.button(
                    rx.icon(
                        "folder-plus",
                        height="60%",
                    ),
                    "Add Folder",
                    color_scheme="indigo",
                    radius="large",
                    on_click=AddFolderDialogState.open_dialog
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="file-plus-2",
                        height="60%"
                    ),
                    "Add Files",
                    bg="GREEN",
                    color="WHITE",
                    variant="solid",
                    radius="large",
                    _hover = {"bg":"rgb(0,255,0)","color":"rgb(100,100,100)"},
                    on_click=AddFileDialogState.open_dialog
                ),
                width="95%"
            )
        ),
        conditional_render(
            ViewCollectionState.has_both_folders_and_files,
            rx.hstack(
                rx.divider(),
                rx.text("Folders"),
                rx.divider(),
                width="100%",
                align="center",
                justify="center",
            )
        ),
        conditional_render(
            ViewCollectionState.collection_folders,
            rx.accordion.root(
                rx.foreach(
                    ViewCollectionState.collection_folders,
                    tablet_collection_display_accordian
                ),
                width="95%",
                collapsible=True,
                color_scheme="gray",
                border_color="gray",
                border_width="1px",
                radius='small',
            )
        ),
        conditional_render(
            ViewCollectionState.has_both_folders_and_files,
            rx.hstack(
                rx.divider(),
                rx.text("Files"),
                rx.divider(),
                width="100%",
                align="center",
                justify="center",
            )
        ),
        rx.flex(
            rx.foreach(
                ViewCollectionState.collection_files,
                view_collection_file_card
            ),
            style={"max-width":"95%"},
            wrap='wrap',
            justify="center",
            spacing='2'
        ),
        bg="#0f0f0f",
        style={"min-height":"100vh"},
        align="center",
        spacing='3'
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