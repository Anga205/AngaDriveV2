import sqlite3, os, time
from AngaDriveV2.library import *

database_directory = "rx.db"

def create_database():
    # Check if rx.db file exists in the current directory
    db_file_path = database_directory

    if not os.path.exists(db_file_path):
        print("Database not found.... creating one now")
        # If not, create a new database file and the table
        with sqlite3.connect(db_file_path) as con:
            cur = con.cursor()

            cur.execute('''
                CREATE TABLE accounts (
                    token TEXT PRIMARY KEY,
                    display_name TEXT,
                    email TEXT,
                    hashed_password TEXT,
                    avatar TEXT,
                )
                        ''')
            
            cur.execute('''
                CREATE TABLE file_data(
                        original_file_name TEXT,
                        file_directory TEXT PRIMARY KEY,
                        account_token TEXT,
                        file_size INTEGER,
                        timestamp INTEGER
                )
                        ''')
            
            cur.execute(
                '''
                CREATE TABLE notifications (
                    NOTIFICATION_ID TEXT PRIMARY KEY,
                    TIMESTAMP INTEGER,
                    NOTIFICATION_CONDITION TEXT,
                    NOTIFICATION_DATA TEXT
                )
                '''
            )

            cur.execute('''
                CREATE TABLE activity(
                    timestamps INTEGER
                )
            ''')
            con.commit()

            print("Database and table created successfully.")

    else:
        print("Database Found")
create_database()


def account_info(token):
    con = sqlite3.connect(database_directory)
    cur=con.cursor()
    cur.execute(f"SELECT (token, display_name, email) FROM accounts WHERE token={dbify(token)}")
    data = cur.fetchone()
    data = dict(zip(["token", "display_name","email"],data))
    con.close()
    return data

def add_timestamp_to_activity():
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"INSERT INTO activity (timestamps) VALUES ({round(time.time())});")
    con.commit()
    con.close()


def fetch_activity_from_last_week():
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"SELECT timestamps FROM activity")
    output = [x[0] for x in list(cur)]
    con.close()
    return calls_per_day(output)