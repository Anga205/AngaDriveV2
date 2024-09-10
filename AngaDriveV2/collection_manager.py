import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *
from AngaDriveV2.DBMS import *
from AngaDriveV2.common import *
import uuid

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
        new_collection_id = create_new_collection(user_token=self.token ,collection_name=self.new_collection_name)
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
    display_my_collections: list[dict[str,str]]=[]
    def update_collections(self):
        self.collection_ids = get_collection_ids_by_account_token(self.token)
        self.display_my_collections = [collection_info_for_display(collection_id) for collection_id in self.collection_ids]

    def load_collections_page(self):
        self.load_any_page()
        self.update_collections()
    
    def delete_collection(self, collection_id):
        delete_collection_from_db(collection_id)
        self.collection_ids.remove(collection_id)
        self.display_my_collections = [x for x in self.display_my_collections if x['id'] != collection_id]

    def copy_collection(self, collection_obj):
        yield rx.set_clipboard(f"{app_link}/collection?id={collection_obj['id']}")
        yield rx.toast.success(f"Collection link to {collection_obj['name']} copied to clipboard")

class ImportRepoState(CollectionState):
    repo_url:str
    input_box_color:str = "blue"
    show_import_button:bool = False

    def set_repo_url(self, string: str):
        self.repo_url=string
        if is_valid_http_url(string, is_github_repo=True):
            self.input_box_color="blue"
            self.show_import_button = True
        elif (string==""):
            self.input_box_color="blue"
            self.show_import_button = False
        else:
            self.input_box_color="red"
            self.show_import_button = False
    
    def close_dialog(self, junk_value=False):
        self.repo_url=""
        self.show_import_button = False
        self.input_box_color="blue"
        return super().close_dialog()
    
    def verify_repo_url(self):
        is_valid_repo = is_valid_github_repo(self.repo_url)
        if is_valid_repo:
            print("Repo is valid, cloning")
            clone_folder = uuid.uuid4().hex
            if git_clone(self.repo_url, clone_folder):
                print("Repo cloned successfully")
                files: dict[str, dict[str, str]] = move_files_to_upload_dir(clone_folder)
                print("Files moved to upload dir")
                folder_map:dict[str, str] = {"":create_new_collection(self.token, self.repo_url.split("/")[-1])}
                for file in files:
                    if files[file]["file_directory"] not in folder_map:
                        folder_map[files[file]["file_directory"]] = create_new_collection(self.token, files[file]["file_directory"].split("/")[-1], hidden=True)
                        parent_directory = "/".join(files[file]["file_directory"].split("/")[:-1])
                        try:
                            add_folder_to_collection(
                                folder_map[files[file]["file_directory"]], 
                                folder_map[parent_directory]
                            )
                            print(end=f"Added folder {files[file]['file_directory']} to collection {parent_directory}\n")
                        except Exception as e:
                            print(f"Failed to add folder {files[file]['file_directory']} to collection {parent_directory}. Error: {str(e)}")
                    add_file_to_database(
                        account_token=self.token,
                        file_directory=file,
                        file_size=files[file]["file_size"],
                        original_file_name=files[file]["original_file_name"]
                    )
                    print(end=f"Added file {files[file]['original_file_name']} to database\n")
                    add_file_to_collection(
                        collection_id=folder_map[files[file]["file_directory"]],
                        file_path=file
                    )
                    print(end=f"Added file {files[file]['original_file_name']} to collection {files[file]['file_directory']}\n")
                    # TODO: add ability to recursively delete all collections
                yield self.close_dialog()
                yield rx.toast.success("Repo cloned successfully")
            else:
                yield self.close_dialog()
                yield rx.toast.error("Failed to clone repo")
        else:
            yield self.close_dialog()
            yield rx.toast.error("GitHub repo not found")

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
                    conditional_render(
                        ~ImportRepoState.repo_url,
                        rx.chakra.input(
                            placeholder="Enter collection name...",
                            max_length="128",
                            color="WHITE",
                            on_change=CollectionState.set_new_collection_name,
                            is_invalid=CollectionState.is_invalid_collection_name,
                            focus_border_color=CollectionState.new_collection_input_border_color,
                            width="85%"
                        )
                    ),
                    conditional_render(
                        ~CollectionState.new_collection_name,
                        rx.vstack(
                            conditional_render(
                                ~ImportRepoState.repo_url,
                                rx.hstack(
                                    rx.divider(),
                                    rx.text("OR"),
                                    rx.divider(),
                                    width="100%",
                                    align="center"
                                )
                            ),
                            rx.input(
                                placeholder="Paste a GitHub repo url...",
                                width="85%",
                                value=ImportRepoState.repo_url,
                                on_change= ImportRepoState.set_repo_url,
                                color_scheme=ImportRepoState.input_box_color
                            ),
                            conditional_render(
                                ImportRepoState.show_import_button,
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(
                                        "Import",
                                        color_scheme="blue",
                                        variant="outline",
                                        on_click=ImportRepoState.verify_repo_url
                                    ),
                                    width="100%"
                                )
                            ),
                            align="center",
                            width="100%"
                        )
                    ),
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
            on_pointer_down_outside = ImportRepoState.close_dialog,
            on_escape_key_down = ImportRepoState.close_dialog
        ),
        open = CollectionState.open_new_collection_dialog
    )

class ConfirmDeleteDialogState(CollectionState):
    open_dialog_bool:bool = False

    collection_id_to_be_deleted:str
    collection_name_to_be_deleted:str
    def open_dialog(self, collection_id, collection_name):
        self.open_dialog_bool = True
        self.collection_id_to_be_deleted = collection_id
        self.collection_name_to_be_deleted = collection_name
    def close_dialog(self, discard):
        self.open_dialog_bool = False
    def delete_collection(self):
        collection_id = self.collection_id_to_be_deleted
        delete_collection_from_db(collection_id)
        self.collection_ids.remove(collection_id)
        self.display_my_collections = [x for x in self.display_my_collections if x['id'] != collection_id]
        self.close_dialog(False)

def confirm_delete_collection_dialog(button):
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
                        rx.chakra.span(ConfirmDeleteDialogState.collection_name_to_be_deleted, font_weight="bold"),
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
                                on_click = ConfirmDeleteDialogState.delete_collection
                            ),
                        ),
                        width="100%"
                    ),
                    width="100%",
                    align_items="start"
                ),
            ),
            bg="#0f0f0f",
            on_escape_key_down= ConfirmDeleteDialogState.close_dialog,
            on_pointer_down_outside= ConfirmDeleteDialogState.close_dialog
        ),
        open=ConfirmDeleteDialogState.open_dialog_bool
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
                                confirm_delete_collection_dialog(
                                    rx.chakra.wrap(
                                        rx.foreach(
                                            CollectionState.display_my_collections,
                                            lambda collection_obj: conditional_render(
                                                ~collection_obj['hidden'],
                                                desktop_collection_card(
                                                    collection_obj,
                                                    copy_function=CollectionState.copy_collection(collection_obj),
                                                    button3=rx.chakra.tooltip(
                                                            rx.button(
                                                            rx.chakra.icon(
                                                                tag="delete",
                                                                font_size="20px"
                                                            ),
                                                            radius="large",
                                                            variant="soft",
                                                            bg="rgb(75, 0, 0)",
                                                            color="rgb(200, 0, 0)",
                                                            _hover={"bg":"rgb(100, 0, 0)", "color": "rgb(255, 0, 0)"},
                                                            on_click= lambda: ConfirmDeleteDialogState.open_dialog(collection_obj['id'], collection_obj['name'])
                                                        ),
                                                        label="Delete Collection"
                                                    )
                                                )
                                            )
                                        ),
                                        width="100%"
                                    )
                                ),
                                spacing="0vh"
                            ),
                            rx.chakra.tab_panel(
                                rx.chakra.text("Coming Soon!")
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

def tablet_collection_display_accordian(collection_obj):  # collection_obj consists of {"id":, "name":, "file_count": , "size": , "editor_count":, "folder_count":}
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
                    on_click= lambda: CollectionState.copy_collection(collection_obj),
                    color_scheme="lime",
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
                    on_click= lambda: CollectionState.delete_collection(collection_obj['id']),
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
        color="WHITE",
        value=collection_obj["id"]
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