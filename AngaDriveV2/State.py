import reflex as rx
import random, time, asyncio
from AngaDriveV2.library import *
from AngaDriveV2.DBMS import *


start_time = time.time()

class State(rx.State):
    collection_count = 10000
    local_start_time = float(start_time)
    uptime = format_time(round(time.time() - local_start_time))

    user_file_count=0
    user_storage_amount="0 KB"

    def increment_time(self, date):
        self.uptime = format_time(round(time.time() - self.local_start_time))

#    @rx.var
#    def is_logged_in(self) -> bool: # returns true only if the browser has a token AND the token has an email and username attached to it
#        if self.token=="":
#            return False
#        else:
#            data = account_info(self.token)
#            if None in data:
#                return False
#        self.username = data["display_name"]
#        self.email = data["email"]
#        return True

    token:str = rx.Cookie(name="token")
    username:str = "Sample Username"
    email:str = "anonymous@email.com"
    def add_token_if_not_present(self): # check if there is a token, if not, create one and then add it to database
        if self.token == "":
            generated_token = gen_token()
            self.token:str = generated_token
            create_new_account_without_info(generated_token)

    files_hosted : int = 0
    space_used : str = "0 KB"
    site_activity : list[dict] = [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]
    user_count = 0
    def update_site_data_components(self):
        self.files_hosted : int = count_files()
        self.space_used : str = get_formatted_directory_size()
        self.user_count = get_user_count()
        self.site_activity : list[dict] = [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]


    def load_any_page(self):
        add_timestamp_to_activity()
        self.add_token_if_not_present()

    def load_index_page(self):
        self.load_any_page()
        self.update_site_data_components()

    def temp_edit_aspect(self):
        print("editing aspect")

    async def page_not_found_redirect_back_to_home_page(self):
        await asyncio.sleep(5)
        return rx.redirect("/")