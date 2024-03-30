import reflex as rx
import time, asyncio
from AngaDriveV2.common import *
from AngaDriveV2.DBMS import *


start_time = time.time()

class State(rx.State):
    local_start_time = float(start_time)
    uptime = format_time(round(time.time() - local_start_time))
    temperature:str = "0°C"
    ram_usage:int
    cpu_usage:int

    def tick_health(self, date):
        self.uptime = format_time(round(time.time() - self.local_start_time))
        system_info = get_system_info()
        self.temperature = system_info["temperature"]
        self.ram_usage = system_info["ram_usage_percentage"]
        self.cpu_usage = system_info["cpu_usage"]

    token:str = rx.LocalStorage(name="token")
    is_logged_in = rx.LocalStorage(name="logged_in")
    username:str = "Sample Username"
    email:str = "anonymous@email.com"
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
    user_count = 0
    collection_count = 0
    registered_user_count = "Registered Users: 0"
    def update_site_data_components(self):
        self.collection_count = get_collection_count()
        self.files_hosted : int = count_files()
        self.space_used : str = get_all_files_size()
        self.user_count = get_user_count()
        self.registered_user_count = f"Registered Users: {get_registered_users()}"
        self.site_activity : list[dict] = [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]

    user_file_count=0
    user_storage_amount="0 KB"
    def update_account_data_components(self):
        data = get_all_user_files_for_display(self.token)
        self.user_file_count = len(data)
        self.user_storage_amount = get_sum_of_user_file_sizes(self.token)

    state_initialized:bool = False
    def load_any_page(self):
        if not self.state_initialized:
            self.add_token_if_not_present()
            add_timestamp_to_activity()
            self.state_initialized = True

    def load_index_page(self):
        self.load_any_page()
        self.update_site_data_components()
        self.update_account_data_components()
        self.update_account_info()

    user_files: list[list[str]] = []
    def load_files_page(self):
        self.load_any_page()
        self.user_files: list[list] = get_all_user_files_for_display(self.token)


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
            self.image_relative_path = filename
            add_file_to_database(
                account_token=self.token,
                file_directory=filename,
                file_size=get_file_size(outfile),
                original_file_name=file.filename
            )
        self.user_files: list[list[str]] = get_all_user_files_for_display(self.token)
        yield rx.redirect("/my_drive")
    
    def upload_progressbar(self, prog):
        self.upload_progress = prog["progress"]*100
        if prog["progress"] == 1:
            self.upload_progress=0
    
    def delete_file(self, file_obj):
        filename = file_obj[1]
        try:
            os.remove(os.path.join(file_directory,filename))
            try:
                remove_file_from_database(filename)
            except Exception as e:
                print(f"Error occured in execuring AngaDriveV2.State.delete_file.remove_file_from_database: {file_obj}")
        except Exception as e:
            print(f"Error occured in execuring AngaDriveV2.State.delete_file.os_remove: {file_obj}\nError was: {e}")
        self.user_files = get_all_user_files_for_display(self.token)

    
    async def handle_file_page_upload(self, files: list[rx.UploadFile]):
        file_link_list = []
        for file in files:
            upload_data = await file.read()
            filename = gen_filename(file.filename)
            outfile = os.path.join(file_directory,filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            self.image_relative_path = filename
            file_link_list.append(file_link+os.path.join(filename.split(".")[0],file.filename))
            add_file_to_database(
                account_token=self.token,
                file_directory=filename,
                file_size=get_file_size(outfile),
                original_file_name=file.filename
            )
        self.user_files = get_all_user_files_for_display(self.token)
        yield rx.clear_selected_files("file_page_upload")
        yield rx.set_clipboard(", \n".join(file_link_list))
    
    def copy_file_link(self, file_obj):
        if "." in file_obj[0]:
            file_path = os.path.join(file_obj[1].split(".")[0], file_obj[0])
        else:
            file_path = os.path.join(file_obj[1], file_obj[0])
        return rx.set_clipboard(file_link+file_path)
    
    def copy_file_path(self, file_obj):
        return rx.set_clipboard(file_link+file_obj[1])

    def copy_download_link(self, file_obj):
        return rx.set_clipboard(download_link+file_obj[1])
    
    def download_file(self, file_obj):
        add_timestamp_to_activity()
        return rx.download("/"+os.path.join("..",file_directory,file_obj[1]), filename=file_obj[0])