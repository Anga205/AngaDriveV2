import reflex as rx
import random, time
from AngaDriveV2.library import *
from AngaDriveV2.DBMS import *


start_time = time.time()

class State(rx.State):
    token:str = rx.Cookie(name="token")
    files_hosted = 10000
    registered_accounts = 10000
    total_accounts = 10000
    local_start_time = float(start_time)
    uptime = format_time(round(time.time() - local_start_time))

    user_file_count=0
    user_storage_amount="0 KB"

    username= "Anonymous"
    email = "anony@mous.com"

    @rx.var
    def site_activity(self) -> list[dict]:
        return [{"date":x, "times_opened": fetch_activity_from_last_week()[x]} for x in fetch_activity_from_last_week()]

    def increment_time(self, date):
        self.uptime = format_time(round(time.time() - self.local_start_time))

    @rx.var
    def is_logged_in(self) -> bool: # returns true only if the browser has a token AND the token has an email and username attached to it
        if self.token=="":
            return False
        else:
            data = account_info(self.token)
            if None in data:
                return False
        self.username = data["display_name"]
        self.email = data["email"]
        return True

    def load_index_page(self):
        add_timestamp_to_activity()

    @rx.var
    def space_used(self) -> str:
        return get_formatted_directory_size()
    
    @rx.var
    def files_hosted(self) -> int:
        return count_files()