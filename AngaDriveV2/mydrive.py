import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.shared_components import *

class UploadState(State):
    open_upload_dialog:bool = False
    
    def open_dialog(self):
        self.open_upload_dialog = True

    def close_dialog(self):
        self.open_upload_dialog = False
        return rx.clear_selected_files("file_page_upload")

    async def handle_file_page_upload(self, files: list[rx.UploadFile]):
        yield rx.clear_selected_files("file_page_upload")
        file_link_list = []
        for file in files:
            upload_data = await file.read()
            filename = gen_filename(file.filename)
            outfile = os.path.join(file_directory,filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            file_link_list.append(file_link+os.path.join(filename.split(".")[0],file.filename))
            add_file_to_database(
                account_token=self.token,
                file_directory=filename,
                file_size=get_file_size(outfile),
                original_file_name=file.filename
            )
        self.user_files: list[dict[str, str]] = get_all_user_files_for_display(self.token)
        yield self.close_dialog()
        yield rx.set_clipboard(", \n".join(file_link_list))
        yield rx.toast.success("Files uploaded and copied to clipboard")

def upload_button():
    return rx.dialog.root(
    rx.dialog.trigger(
        rx.chakra.button(
            rx.chakra.image(
                src="/upload.png",
                height="2vh",
                custom_attrs={"draggable":"false"},
                width="auto"
                ),
            "Upload",
            color="WHITE",
            font_size="1.65vh",
            height="4vh",
            bg="#000055",
            width="10vh",
            border_radius="1vh",
            _hover={"bg":"#0000aa"},
            on_click=UploadState.open_dialog
        ),
    ),
    rx.dialog.content(
        rx.dialog.title(
            "Upload Files"
        ),
        rx.dialog.description(
            rx.upload(
                rx.cond(
                    rx.selected_files("file_page_upload"),
                    rx.vstack(
                        rx.spacer(),
                        rx.foreach(
                            rx.selected_files("file_page_upload"),
                            rx.text
                        ),
                        rx.spacer(),
                        style={"min-height":"10vh"},
                        align="center"
                    ),
                    rx.vstack(
                        rx.spacer(),
                        rx.text("Drag and drop files here or click to select files"),
                        rx.spacer(),
                        style={"min-height":"15vh"}
                    ),
                ),
                display='flex',
                justify_content= 'center',
                align_items= 'center',
                padding="1vh",
                border_radius="5px",
                border="1px dotted #0000ff",
                id="file_page_upload"
            )
        ),
        rx.box(
            height="1vh"
        ),
        rx.cond(
            rx.selected_files("file_page_upload"),
            empty_component(),
            rx.vstack(
                rx.hstack(
                    rx.divider(),
                    rx.text("OR"),
                    rx.divider(),
                    justify="center",
                    align="center",
                    width="100%"
                ),
                rx.chakra.input(
                    placeholder="Enter file link",
                    width="100%"
                ),
                rx.box(
                    height="1vh"
                ),
                spacing="0",
                width="100%",
            )
        ),
        rx.chakra.hstack(
            rx.chakra.button(
                "Close",
                bg="#440000",
                color="WHITE",
                _hover={"bg":"#000033"},
                on_click=UploadState.close_dialog
            ),
            rx.spacer(),
            conditional_render(
                rx.selected_files("file_page_upload"),
                rx.chakra.box(
                    rx.chakra.button(
                        "Upload",
                        bg="#113322",
                        color="WHITE",
                        _hover={"bg":"#224433"},
                        on_click=UploadState.handle_file_page_upload(rx.upload_files(upload_id="file_page_upload", on_upload_progress=State.upload_progressbar))
                    )
                ),
            ),
            width="100%",
            spacing="10"
        ),
        bg="#111111",
        color="WHITE",
        on_escape_key_down=lambda x: UploadState.close_dialog(),
        on_pointer_down_outside=lambda x: UploadState.close_dialog()
    ),
    open=UploadState.open_upload_dialog
)

def desktop_index():
    return site_template(
        "Files",
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.vstack(
                    rx.chakra.heading(
                        "My Files",
                        color="WHITE",
                        font_size="3.5vh"
                    ),
                    rx.chakra.spacer(),
                    spacing="0vh",
                    height="100%"
                ),
                rx.chakra.spacer(),
                rx.chakra.vstack(
                    rx.chakra.spacer(),
                    upload_button(),
                    spacing="0vh",
                    height="100%"
                    ),
                width="98%",
                height="8vh"
            ),
            rx.chakra.hstack(
                rx.chakra.box(
                    width="5vh", 
                    height="0vh"
                    ),
                rx.cond(
                    State.user_files,
                    rx.chakra.wrap(
                        rx.foreach(
                            State.user_files,
                            file_card
                        ),
                    ),
                    rx.chakra.vstack(
                        rx.chakra.spacer(),
                        rx.chakra.alert(
                            rx.chakra.alert_icon(),
                            rx.chakra.alert(
                                "Drag and drop files here, of click the 'Upload' button on the top right", 
                                bg="#000033", 
                                color="WHITE"
                            ),
                            border_radius="2vh",
                            bg="#000033",
                            border_color="#0000aa",
                            border_width="0.2vh"
                        ),
                        rx.chakra.spacer(),
                        height="50vh",
                    )
                ),
                spacing="0vh",
            ),
            bg="#0f0f0f",
            width="100%"
        )
    )

def no_files():
    return rx.upload(
    rx.vstack(
        rx.spacer(),
        rx.callout(
            "uploaded files will show up here, tap anywhere to upload files",
            icon="info"
        ),
        rx.spacer(),
        height="100vh",
        align="center",
        width="100%"
    ),
    id="tablet_page_upload",
    border="0px",
    width="100%",
    height="95vh",
    padding="0px",
    on_drop=UploadState.handle_file_page_upload(rx.upload_files(upload_id="file_page_upload", on_upload_progress=State.upload_progressbar))
)

def tablet_show_files():
    return rx.vstack(
    empty_component(height="50px"),
    rx.hstack(
        rx.heading("My Files", color="WHITE"),
        rx.spacer(),
        rx.upload(
            rx.button("Upload"),
            id="tablet_page_upload",
            border="0px",
            padding="0px",
            on_drop=UploadState.handle_file_page_upload(rx.upload_files(upload_id="file_page_upload", on_upload_progress=State.upload_progressbar))
        ),
        width="90%"
    ),
    rx.vstack(
        rx.foreach(
            State.user_files,
            mobile_file_card
        ),
        width="100%",
        spacing="3",
        align="center",
        bg="#0f0f0f"
    ),
    width="100%",
    align="center"
)

def tablet_page():
    return rx.cond(
        State.user_files,
        tablet_show_files(),
        no_files()
    )

def tablet_index():
    return rx.vstack(
        tablet_navbar("files"),
        tablet_page(),
        spacing='0',
        width="100%",
        bg="#0f0f0f",
        height="100vh"
    )

def index():
    return rx.box(
        rx.desktop_only(
            desktop_index()
        ),
        rx.mobile_and_tablet(
            tablet_index()
        ),
        width="100%",
        bg="#0f0f0f"
    )