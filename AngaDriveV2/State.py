import reflex as rx
import random, time
from AngaDriveV2.library import *
from AngaDriveV2.DBMS import *


start_time = time.time()

class State(rx.State):
    files_hosted = 10000
    registered_accounts = 10000
    total_accounts = 10000
    space_used = "10000 GB"
    local_start_time = float(start_time)
    uptime = format_time(round(time.time() - local_start_time))

    site_activity = [
        {"date": "21 Jan", "times_opened": random.randint(1,20)},
        {"date": "22 Jan", "times_opened": random.randint(1,20)},
        {"date": "23 Jan", "times_opened": random.randint(1,20)},
        {"date": "24 Jan", "times_opened": random.randint(1,20)},
        {"date": "25 Jan", "times_opened": random.randint(1,20)},
        {"date": "26 Jan", "times_opened": random.randint(1,20)},
        {"date": "27 Jan", "times_opened": random.randint(1,20)},
    ]

    def increment_time(self, date):
        self.uptime = format_time(round(time.time() - self.local_start_time))
    

    def load_index_page(self):
        add_timestamp_to_activity()