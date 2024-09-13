import sqlite3, os, time, bcrypt
from functools import lru_cache
from contextlib import asynccontextmanager
from AngaDriveV2.common import *

def load_database():
    global con, cur
    global accounts, file_data, collections, activity
    cur.execute("SELECT token, display_name, email, hashed_password FROM accounts")
    for row in cur:
        accounts[row[0]] = {
            "token":            row[0],
            "display_name":     row[1],
            "email":            row[2]
        }
        if row[3]!=None:
            accounts[row[0]]["hashed_password"]=row[3]
    cur.execute("SELECT original_file_name, file_directory, account_token, file_size, timestamp, cached FROM file_data")
    for row in cur:
        file_data[row[1]] = {
            "original_file_name":    row[0],
            "file_directory":        row[1],
            "account_token":         row[2],
            "file_size":             row[3],
            "timestamp":             row[4],
            "cached":                bool(row[5])
        }
    cur.execute("SELECT id, name, editors, size, collections, files, hidden FROM collections")
    for row in cur:
        collections[row[0]] = {
            "id":           row[0],
            "name":         row[1],
            "editors":      [] if row[2]=="" else row[2].split(","),
            "size":         row[3],
            "collections":  [] if row[4]=="" else row[4].split(","),
            "files":        [] if row[5]=="" else row[5].split(", "),
            "hidden":       bool(row[6])
        }
    cur.execute("SELECT timestamps FROM activity")
    for row in cur:
        activity.append(row[0])

def create_database():
    if not os.path.exists(database_directory):
        print("Database not found.... creating one now")
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE accounts (
                token TEXT PRIMARY KEY,
                display_name TEXT,
                email TEXT,
                hashed_password TEXT
            )''')
        
        cur.execute('''
            CREATE TABLE file_data(
                    original_file_name TEXT,
                    file_directory TEXT PRIMARY KEY,
                    account_token TEXT,
                    file_size INTEGER,
                    timestamp INTEGER,
                    cached BOOLEAN DEFAULT 0
            )
                    ''')

        cur.execute('''
            CREATE TABLE activity(
                timestamps INTEGER
            )
        ''')

        cur.execute('''
            CREATE TABLE collections(
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    editors TEXT,
                    size INTEGER,
                    collections TEXT,
                    files TEXT,
                    hidden BOOLEAN DEFAULT 0
            )
                    ''')
        con.commit()

        print("Database and table created successfully.")
        return con, cur
    else:
        print("Database found.... connecting to it now")
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute("PRAGMA table_info(collections)")
        columns = [column[1] for column in cur.fetchall()]
        if "hidden" not in columns:
            print("Updating database to contain hidden column in collections table")
            cur.execute("ALTER TABLE collections ADD COLUMN hidden BOOLEAN DEFAULT 0")
            con.commit()
        cur.execute("PRAGMA table_info(file_data)")
        columns = [column[1] for column in cur.fetchall()]
        if "cached" not in columns:
            print("Updating database to contain cached column in file_data table")
            cur.execute("ALTER TABLE file_data ADD COLUMN cached BOOLEAN DEFAULT 0")
            con.commit()
        return con, cur

con, cur = create_database()

def account_info(token):
    try:
        return {
            "token"         : token,
            "display_name"  : accounts[token]["display_name"],
            "email"         : accounts[token]["email"]
        }
    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.account_info\nVar Dump:\ntoken: {token}\ndata: {accounts}\nError: {e}")
        return dict(zip(["token", "display_name","email"],["ERROR", "ERROR", "ERROR"]))

def get_total_activity_pulses():
    return len(activity)

pulse_count = get_total_activity_pulses()

def add_timestamp_to_activity():

    timestamp = round(time.time())
    global activity, pulse_count
    activity.append(timestamp)
    pulse_count += 1

    global cur, con
    cur.execute(f"INSERT INTO activity (timestamps) VALUES ({timestamp});")
    con.commit()

def get_user_count():
    
    accounts_set = set()
    for file in file_data:
        accounts_set.add(file_data[file]["account_token"])
    for collection in collections:
        for editor in collections[collection]["editors"]:
            accounts_set.add(editor)
    for account in accounts:
        accounts_set.add(account)
    return len(accounts_set)

def get_registered_users():
    return len(accounts)

def calculate_collection_size(collection_id, ignore_files=None, ignore_folders=None):
    first=False
    if ignore_files==None and ignore_folders==None:
        first=True
    if ignore_files==None:
        ignore_files = set()
    if ignore_folders==None:
        ignore_folders = set()
    size=0
    for file in collections[collection_id]["files"]:
        if file not in ignore_files:
            size += file_data[file]["file_size"]
            ignore_files.add(file)
    for folder in collections[collection_id]["collections"]:
        if folder not in ignore_folders:
            ignore_folders.add(folder)
            calculation = calculate_collection_size(folder, ignore_files, ignore_folders)
            size += calculation["size"]
            ignore_files.update(calculation["ignore_files"])
            ignore_folders.update(calculation["ignore_folders"])
    if first:
        return size
    return {"size": size, "ignore_files": ignore_files, "ignore_folders": ignore_folders}

def update_collection_size(collection_id, collections_updated=None):
    global collections
    first=False
    if collections_updated==None:
        first=True
        collections_updated = set()
    collections[collection_id]["size"] = calculate_collection_size(collection_id)

    global con, cur
    cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (collections[collection_id]["size"], collection_id))
    con.commit()

    collections_updated.add(collection_id)
    for collection in collections:
        if collection not in collections_updated:
            if collection_id in collections[collection]["collections"]:
                collections_updated.update(update_collection_size(collection, collections_updated))
    if not first:
        return collections_updated

def fetch_activity_from_last_week():
    return calls_per_day(activity)

def does_filename_already_exist(filename_to_check: str) -> bool:
    return filename_to_check in file_data

def add_file_to_database(original_file_name, file_directory, account_token, file_size, cached=False):

    timestamp = round(time.time())

    global file_data
    file_data[file_directory] = {
        "original_file_name": original_file_name,
        "file_directory": file_directory,
        "account_token": account_token,
        "file_size": file_size,
        "timestamp": timestamp,
        "cached": cached
    }
    
    global cur, con
    cur.execute(f"INSERT INTO file_data (original_file_name, file_directory, account_token, file_size, timestamp, cached) VALUES (?, ?, ?, ?, ?, ?)", (original_file_name, file_directory, account_token, file_size, timestamp, int(cached)))
    con.commit()

def get_all_user_files_for_display(account_token) -> list[dict[str, str]]:

    rows = []

    for file in file_data:
        if file_data[file]["account_token"]==account_token:
            rows.append({
                "original_name" : file_data[file]["original_file_name"],                                 # like original_name.png
                "file_path"     : file_data[file]["file_directory"],                                 # like vb78duvhs6s.png
                "size"          : format_bytes(file_data[file]["file_size"]),                   # like 75.1 KB
                "timestamp"     : time.ctime(file_data[file]["timestamp"]),                     # like wed 23 june 2023
                "truncated_name": truncate_string(file_data[file]["original_file_name"], length=20),     # like origina....
                "file_link"     : file_link+file_data[file]["file_directory"],                       # like https://file.anga.pro/i/vb78duvhs6s.png
                "previewable"   : can_be_previewed(file_data[file]["file_directory"]),               # like True
                "owner_token"   : account_token,
                "cached"        : file_data[file]["cached"]
            })
    return list(reversed(rows))       # reversed to put the most recently uploaded files at the top

def remove_file_from_all_collections(file_path):
    global collections
    for collection in collections:
        if file_path in collections[collection]["files"]:
            remove_file_from_collection_db(collection, file_path)

def remove_file_from_database(file_directory):
    remove_file_from_all_collections(file_directory)

    global file_data
    del file_data[file_directory]

    try:
        global cur, con
        cur.execute(f"DELETE FROM file_data WHERE file_directory = ?", (file_directory,))
        con.commit()

    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.remove_file_from_database\nVar Dump:\nfile_directory: {file_directory}\nError: {e}")

def get_sum_of_user_file_sizes(token):

    sum_of_sizes = 0
    for file in file_data:
        if file_data[file]["account_token"]==token:
            sum_of_sizes += file_data[file]["file_size"]
    return format_bytes(sum_of_sizes)
    
def get_collection_count():
    return len(collections)

def delete_collection_from_db(collection_id):

    global collections
    for collection in collections:
        if collection_id in collections[collection]["collections"]:
            remove_folder_from_collection(collection_id, collection)
    del collections[collection_id]

    global cur, con
    cur.execute(f"DELETE FROM collections WHERE id = ?", (collection_id,))
    con.commit()

def get_all_collection_ids() -> list[str]:
    return list(collections.keys())

def get_collection_ids_by_account_token(account_token: str) -> list[str]:
    ids = []
    for collection in collections:
        if account_token in collections[collection]["editors"]:
            ids.append(collection)
    return ids

def collection_info_for_display(collection_id):
    return {
        "id":           collection_id, 
        "name":         truncate_string(collections[collection_id]["name"]), 
        "full_name":    collections[collection_id]["name"],
        "file_count":   len(collections[collection_id]["files"]), 
        "size":         format_bytes(collections[collection_id]["size"]), 
        "editor_count": len(collections[collection_id]["editors"]),
        "folder_count": len(collections[collection_id]["collections"]),
        "hidden":       collections[collection_id]["hidden"]
        }

def gen_collection_id():
    
    generated_id = "".join([random.choice(list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")) for x in range(15)])
    all_collection_ids = get_all_collection_ids()
    if generated_id in all_collection_ids:
        return gen_collection_id()
    else:
        return generated_id

def create_new_collection(user_token, collection_name, hidden=False):

    global collections
    collection_id = gen_collection_id()
    collections[collection_id] = {
        "id":           collection_id,
        "name":         collection_name,
        "editors":      [user_token],
        "size":         0,
        "collections":  [],
        "files":        [],
        "hidden":       hidden
    }

    global cur, con
    cur.execute(f"INSERT INTO collections (id, name, editors, size, collections, files, hidden) VALUES (?, ?, ?, ?, ?, ?, ?)", (collection_id, collection_name, user_token, 0, "", "", int(hidden)))
    con.commit()

    return collection_id

def is_valid_token(token: str) -> bool:
    if token in accounts:
        return True
    for file in file_data:
        if token == file_data[file]["account_token"]:
            return True
    for collection in collections:
        if token in collections[collection]["editors"]:
            return True
    return False

def does_user_have_files(token):
    for file in file_data:
        if file_data[file]["account_token"]==token:
            return True
    return False
    
def user_signup(token, display_name, email, password:str):

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    global accounts
    accounts[token] = {
        "token"         : token,
        "display_name"  : display_name,
        "email"         : email,
        "hashed_password": hashed_password
    }

    global cur, con

    cur.execute("INSERT INTO accounts(token, display_name, email, hashed_password) VALUES (?, ?, ?, ?)", (token ,display_name,email,hashed_password))

    con.commit()

def migrate_files(old_token, new_token):

    global file_data

    for file in file_data:
        if file_data[file]["account_token"]==old_token:
            file_data[file]["account_token"] = new_token

    global cur, con

    cur.execute("UPDATE file_data SET account_token = ? WHERE account_token = ?", (new_token, old_token))

    con.commit()
    remove_account_from_accounts_table(old_token)

def remove_account_from_accounts_table(token):

    global accounts
    del accounts[token]

    global cur, con

    cur.execute("DELETE FROM accounts WHERE token = ?", (token,))

    con.commit()

def email_already_exists(email):
    for account in accounts:
        if accounts[account]["email"]==email:
            return True
    return False

def user_login(email: str, password:str):

    result: list[str] = [None, None]
    for account in accounts:
        if accounts[account]["email"]==email:
            result = [account, accounts[account]["hashed_password"]]
            break

    if result == [None, None]:
        return {False: "Account not found"}
    if not bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        return {False: "Authentication Failed"}
    return {True: result[0]}

def flowinity_user_signup(flowinity_data):
    global accounts
    accounts[flowinity_data["token"]] = {
        "token"         : flowinity_data["token"],
        "display_name"  : flowinity_data["username"],
        "email"         : flowinity_data["email"]
    }

    global cur, con
    cur.execute("INSERT INTO accounts(token, display_name, email) VALUES (?, ?, ?)", (flowinity_data["token"], flowinity_data["username"], flowinity_data["email"]))
    con.commit()

def token_exists(token):
    return is_valid_token(token)

def count_files():
    return len(file_data)

def get_all_files_size():
    sum_of_sizes = 0
    for file in file_data:
        sum_of_sizes += file_data[file]["file_size"]
    return format_bytes(sum_of_sizes)

@lru_cache(maxsize=100)
def get_file_name(file_path):
    return file_data.get(file_path, {}).get("original_file_name", "Error")

def get_collection_info_for_viewer(collection_id):
    if collection_id not in collections:
        return None
    return {
        "id"        : collection_id,
        "name"      : collections[collection_id].get("name", "Error"),
        "editors"   : collections[collection_id].get("editors", []),
        "Size"      : format_bytes(collections[collection_id]["size"]),
        "Files"     : collections[collection_id].get("files", []),
        "Folders"   : collections[collection_id].get("collections", []),
        "Hidden"    : collections[collection_id].get("hidden", False)
    }

def get_file_info_for_card(file_path:str) -> dict[str,str]:
    return {
        "original_name" : file_data.get(file_path, {}).get("original_file_name", "Error"),                              # like original_name.png
        "file_path"     : file_path,                                                                                    # like vb78duvhs6s.png
        "size"          : format_bytes(file_data.get(file_path, {}).get("file_size", 0)),                               # like 75.1 KB
        "timestamp"     : time.ctime(file_data.get(file_path, {}).get("timestamp", 0)),                                 # like wed 23 jun 2023
        "truncated_name": truncate_string(file_data.get(file_path, {}).get("original_file_name", "Error"), length=20),  # like origina....
        "file_link"     : file_link+file_path,                                                                          # like https://file.anga.pro/i/vb78duvhs6s.png
        "previewable"   : can_be_previewed(file_path),                                                                  # like True
        "owner_token"   : file_data.get(file_path, {}).get("account_token", "Error")
    }

def add_file_to_collection(collection_id, file_path):
    global collections
    collections[collection_id]["files"].append(file_path)
    update_collection_size(collection_id)

    global con, cur
    files = ", ".join(collections[collection_id]["files"])
    cur.execute(f"UPDATE collections SET files = ? WHERE id = ?", (files, collection_id))
    con.commit()

def remove_file_from_collection_db(collection_id, file_path):

    global collections
    collections[collection_id]["files"].remove(file_path)
    
    global con, cur
    files = ", ".join(collections[collection_id]["files"])
    cur.execute(
        f"UPDATE collections SET files = ? WHERE id = ?", 
        (files, collection_id)
    )
    con.commit()
    update_collection_size(collection_id)

def user_has_collections(user_token: str) -> bool:
    for collection in collections:
        if user_token in collections[collection]["editors"]:
            return True
    return False

def folder_is_in_collection(folder_id: str, collection_id: str) -> bool:
    return folder_id in collections[collection_id]["collections"]

def add_folder_to_collection(folder_id: str, collection_id: str):
    if folder_is_in_collection(folder_id=folder_id, collection_id=collection_id):
        return
    
    global collections
    collections[collection_id]["collections"].append(folder_id)
    update_collection_size(collection_id)

    global con, cur
    cur.execute(f"UPDATE collections SET collections = ? WHERE id = ?", (",".join(collections[collection_id]["collections"]), collection_id))
    con.commit()

def remove_folder_from_collection(folder_id: str, collection_id: str):
    if not folder_is_in_collection(folder_id=folder_id, collection_id=collection_id):
        return
    
    global collections
    collections[collection_id]["collections"].remove(folder_id)
    update_collection_size(collection_id)

    global con, cur
    cur.execute(f"UPDATE collections SET collections = ? WHERE id = ?", (",".join(collections[collection_id]["collections"]), collection_id))
    con.commit()

def token_exists_in_accounts_table(token):
    return token in accounts

def save_file_from_link(file_link: str, filename: str, account_token:str):
    original_file_name = file_link.split("/")[-1].replace("%20", " ")
    try:
        response = requests.get(file_link, stream=True)
        response.raise_for_status()
        with open(os.path.join(file_directory,filename), 'wb') as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)
        file_size = os.path.getsize(os.path.join(file_directory,filename))
        add_file_to_database(original_file_name, filename, account_token, file_size)
    except Exception as e:
        print(f"AngaDriveV2.DBMS.save_file_from_link Error saving file: {e}")

def switch_cache_status(file_path:str):
    global file_data
    file_data[file_path]["cached"] = not file_data[file_path]["cached"]

    global con, cur
    cur.execute(f"UPDATE file_data SET cached = ? WHERE file_directory = ?", (int(file_data[file_path]["cached"]), file_path))
    con.commit()

@asynccontextmanager
async def lifespan(discard=None):
    global con
    print("Database connection opened")
    load_database()
    yield
    con.commit()
    con.close()
    print("Database connection closed")
