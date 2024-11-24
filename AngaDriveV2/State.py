import reflex as rx
import asyncio
from AngaDriveV2.common import *
from AngaDriveV2.DBMS import *


start_time = time.time()

class State(rx.State):
    local_start_time = float(start_time)
    uptime:str = format_time(round(time.time() - local_start_time))
    ram_percent:int
    total_ram:str
    used_ram:str
    cpu_usage:int
    temperature:str
    temperature_available:bool

    token:str = rx.LocalStorage(name="token")
    is_logged_in = rx.LocalStorage(name="logged_in")
    username:str = "{username}"
    email:str = "{email_id}"

    enable_previews_local:str = rx.LocalStorage(name="enable_previews")
    enable_caching_local:str = rx.LocalStorage(name="enable_caching")
    ultra_secure_local:str = rx.LocalStorage(name="ultra_secure")
    settings_initialized:str = rx.LocalStorage(name="settings_initialized")
    enable_previews:bool
    ultra_secure:bool
    enable_caching:bool

    def initialize_settings(self):
        if not self.settings_initialized:
            self.settings_initialized = "true"
            self.enable_previews_local = "true"
            self.enable_caching_local = ""
            self.ultra_secure_local = ""
        self.enable_previews = bool(self.enable_previews_local)
        self.enable_caching = bool(self.enable_caching_local)
        self.ultra_secure = bool(self.ultra_secure_local)

    def swap_previews(self):
        if self.enable_previews_local == "true":
            self.enable_previews_local = ""
        else:
            self.enable_previews_local = "true"
            if self.ultra_secure:
                self.swap_security()
        self.enable_previews = bool(self.enable_previews_local)

    def swap_caching(self):
        if self.enable_caching_local == "true":
            self.enable_caching_local = ""
        else:
            self.enable_caching_local = "true"
        self.enable_caching = bool(self.enable_caching_local)
    
    def swap_security(self):
        if self.ultra_secure_local == "true":
            self.ultra_secure_local = ""
        else:
            self.ultra_secure_local = "true"
            if self.enable_caching:
                self.swap_caching()
        self.ultra_secure = bool(self.ultra_secure_local)

    def add_token_if_not_present(self): # check if there is a token, if not, create one and then add it to database
        if self.token == "" or (not is_valid_token(self.token)):
            generated_token = gen_token()
            self.token:str = generated_token
            self.is_logged_in = ""

    def update_account_info(self):
        if self.is_logged_in:
            account_data = account_info(self.token)
            self.username = account_data.get("display_name")
            self.email = account_data.get("email")

    files_hosted : int = 0
    space_used : str = "0 KB"
    site_activity : list[dict] = [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]
    user_count: int = 0
    collection_count: int = 0
    registered_user_count: str = "Registered Users: 0"
    pulses:int = 0
    def update_site_data_components(self):
        self.collection_count = get_collection_count()
        self.files_hosted : int = count_files()
        self.space_used : str = get_all_files_size()
        self.user_count = get_user_count()
        self.registered_user_count: str = f"Registered Users: {get_registered_users()}"
        self.site_activity : list[dict] = [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]
        self.pulses: int = get_total_activity_pulses()

    user_file_count: int = 0
    user_storage_amount:str = "0 KB"
    def update_account_data_components(self):
        data: list[dict[str, str]] = get_all_user_files_for_display(self.token)
        self.user_file_count: int = len(data)
        self.user_storage_amount: str = get_sum_of_user_file_sizes(self.token)

    state_initialized:bool = False
    def load_any_page(self):
        if not self.state_initialized:
            self.add_token_if_not_present()
            add_timestamp_to_activity()
            self.initialize_settings()
            self.state_initialized = True
        if self.username == "{username}":
            self.update_account_info()

    def load_index_page(self):
        self.load_any_page()
        self.update_site_data_components()
        self.update_account_data_components()
        self.update_account_info()

    user_files: list[dict[str, str]] = []
    def load_files_page(self):
        self.load_any_page()
        self.user_files: list[dict[str, str]] = get_all_user_files_for_display(self.token)


    async def page_not_found_redirect_back_to_home_page(self):
        await asyncio.sleep(5)
        return rx.redirect("/")
    

    is_uploading:bool = False
    upload_progress:int=0
    async def handle_upload(self, files: list[rx.UploadFile]):
        UPLOAD_ID = "upload1"
        yield rx.clear_selected_files(UPLOAD_ID)
        for file in files:
            upload_data = await file.read()
            filename = gen_filename(file.filename)
            outfile = os.path.join(file_directory,filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            add_file_to_database(
                account_token=self.token,
                file_directory=filename,
                file_size=get_file_size(outfile),
                original_file_name=file.filename,
                cached=self.enable_caching
            )
        self.user_files: list[dict[str, str]] = get_all_user_files_for_display(self.token)
        yield rx.redirect("/my_drive")
        yield rx.toast.success("Files successfully uploaded")
    
    def upload_progressbar(self, prog):
        self.upload_progress = prog["progress"]*100
        if prog["progress"] == 1:
            self.upload_progress=0
    
    def delete_file(self, file_obj):
        try:
            if file_obj not in self.user_files:
                return rx.toast.error("File not found")
            filename = file_obj["file_path"]
            try:
                os.remove(os.path.join(file_directory,filename))
                try:
                    remove_file_from_database(filename)
                except Exception as e:
                    print(f"Error occured in execuring AngaDriveV2.State.delete_file.remove_file_from_database: {file_obj}")
            except Exception as e:
                print(f"Error occured in execuring AngaDriveV2.State.delete_file.os_remove: {file_obj}\nError was: {e}")
            self.user_files.remove(file_obj)
        except Exception as e:
            print(f"Error occured in execuring AngaDriveV2.State.delete_file: {file_obj}\nError was: {e}")
    
    def copy_file_link(self, file_obj: dict[str, str]):
        if "." in file_obj["original_name"]:
            file_path = os.path.join(file_obj["file_path"].split(".")[0], file_obj["original_name"])
        else:
            file_path = os.path.join(file_obj["file_path"], file_obj["original_name"])
        valid_file_link = cache_link if file_obj.get("cached") else file_link
        yield rx.set_clipboard(valid_file_link+file_path.replace(" ","%20"))
        yield rx.toast.success("File link copied to clipboard")
    
    def copy_file_path(self, file_obj):
        valid_file_link = cache_link if file_obj.get("cached") else file_link
        yield rx.set_clipboard(valid_file_link+file_obj["file_path"])
        yield rx.toast.success("File path copied to clipboard")

    def copy_download_link(self, file_obj):
        valid_download_link = cached_download_link if file_obj.get("cached") else download_link
        yield rx.set_clipboard(valid_download_link+file_obj["file_path"])
        yield rx.toast.success("Download link copied to clipboard")
    
    def download_file(self, file_obj):
        add_timestamp_to_activity()
        valid_download_link = cached_download_link if file_obj.get("cached") else download_link
        return rx.redirect(valid_download_link+file_obj.get("file_path"), external=True, replace=True)

    def logout(self):
        self.token = gen_token()
        self.is_logged_in = ""
        self.username:str = "{username}"
        self.email:str = "{email_id}"
        self.update_account_data_components()
    
