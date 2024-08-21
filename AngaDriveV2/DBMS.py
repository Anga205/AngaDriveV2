import sqlite3, os, time, bcrypt
from functools import lru_cache
from contextlib import asynccontextmanager
from AngaDriveV2.common import *

accounts={}
file_data={}
activity=[]
collections={}

def load_database():
    global con, cur
    global accounts, file_data, collections
    cur.execute("SELECT token, display_name, email, hashed_password FROM accounts")
    for row in cur:
        accounts[row[0]] = {
            "token":            row[0],
            "display_name":     row[1],
            "email":            row[2]
        }
        if row[3]!=None:
            accounts[row[0]]["hashed_password"]=row[3]
    cur.execute("SELECT original_file_name, file_directory, account_token, file_size, timestamp FROM file_data")
    for row in cur:
        file_data[row[1]] = {
            "original_file_name":    row[0],
            "file_directory":        row[1],
            "account_token":         row[2],
            "file_size":             row[3],
            "timestamp":             row[4]
        }
    cur.execute("SELECT id, name, editors, size, collections, files FROM collections")
    for row in cur:
        collections[row[0]] = {
            "id":           row[0],
            "name":         row[1],
            "editors":      row[2],
            "size":         row[3],
            "collections":  [] if row[4]=="" else row[4].split(","),
            "files":        [] if row[5]=="" else row[5].split(", ")
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
                    timestamp INTEGER
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
                    files TEXT
            )
                    ''')
        con.commit()

        print("Database and table created successfully.")
        return con, cur
    else:
        print("Database found.... connecting to it now")
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
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
    global cur, con
    cur.execute("SELECT COUNT(timestamps) FROM activity")
    count = cur.fetchone()[0]
    return count

pulse_count = get_total_activity_pulses()

def add_timestamp_to_activity():
    global cur, con, pulse_count
    cur.execute(f"INSERT INTO activity (timestamps) VALUES ({round(time.time())});")
    con.commit()
    pulse_count += 1

def get_user_count():
    global cur, con
    cur.execute(f"SELECT COUNT(DISTINCT account_token) FROM file_data")
    try:
       count = int(cur.fetchone()[0])
    except Exception as e:
        print(f'Error occured when calculating get_user_count: {e}')
        count = 0
    return count

def get_registered_users():
    global cur, con
    cur.execute("SELECT COUNT(token) FROM accounts")
    try:
       count = int(cur.fetchone()[0])
    except Exception as e:
        print(f'Error occured when calculating get_registered_users: {e}')
        count = 0
    return count

def fetch_activity_from_last_week():
    global cur, con
    cur.execute(f"SELECT timestamps FROM activity")
    output = [x[0] for x in list(cur)]
    return calls_per_day(output)

def does_filename_already_exist(filename_to_check: str) -> bool:
    
    global cur, con

    # Execute a SELECT query to check if the string is present in any row of the table
    cur.execute(f"SELECT original_file_name FROM file_data WHERE file_directory = {dbify(filename_to_check)}")
    
    row = cur.fetchone()

    # If row is not None, the string is present in the table, so true means the file name is infact there in the database
    return row is not None

def gen_filename(filename):
    generated_name = ""
    allowed_values = "qwertyuiopasdfghjklzxcvbnm1234567890"
    generated_name = "".join(random.choices(allowed_values, k=12))

    if len(filename.split("."))>1:
        generated_name = generated_name + "." + filename.split(".")[-1]
    
    if does_filename_already_exist(generated_name):
        return gen_filename(filename)   #if generated filename already exists in database, then go generate a new one
    
    return generated_name #if generated filename doesnt already exist, then return the generated one

def add_file_to_database(original_file_name, file_directory, account_token, file_size):
    
    global cur, con

    cur.execute(f"INSERT INTO file_data (original_file_name, file_directory, account_token, file_size, timestamp) VALUES (?, ?, ?, ?, ?)", (original_file_name, file_directory, account_token, file_size, round(time.time())))
    con.commit()

def get_all_user_files_for_display(account_token) -> list[dict[str, str]]:

    global cur, con

    cur.execute(f"SELECT original_file_name, file_directory, file_size, timestamp FROM file_data WHERE account_token = ?", (account_token,))

    rows = [{
        "original_name" : x[0],                                 # like original_name.png
        "file_path"     : x[1],                                 # like vb78duvhs6s.png
        "size"          : format_bytes(x[2]),                   # like 75.1 KB
        "timestamp"     : time.ctime(x[3]),                     # like wed 23 june 2023
        "truncated_name": truncate_string(x[0], length=20),     # like origina....
        "file_link"     : file_link+x[1],                       # like https://file.anga.pro/i/vb78duvhs6s.png
        "previewable"   : can_be_previewed(x[1]),               # like True
        "owner_token"   : account_token
    } for x in cur]

    return list(reversed(rows))       # reversed to put the most recently uploaded files at the top

def remove_file_from_all_collections(file_path):
    try:
        global cur, con
        cur.execute(f"SELECT file_size FROM file_data WHERE file_directory = ?", (file_path,))
        file_size = cur.fetchone()[0]
        cur.execute(f"SELECT id, size, files FROM collections WHERE files LIKE ?", (f'%{file_path}%',))
        rows = cur.fetchall()
        for row in rows:
            files:list = row[2].split(", ")
            files.remove(file_path)
            files = ", ".join(files)
            new_size = row[1] - file_size
            cur.execute(f"UPDATE collections SET files = ? WHERE id = ?", (files, row[0]))
            cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (new_size, row[0]))
        con.commit()
    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.remove_file_from_all_collections\nVar Dump:\nfile_path: {file_path}\nError: {e}")

def remove_file_from_database(file_directory):
    remove_file_from_all_collections(file_directory)
    try:
        global cur, con
        cur.execute(f"DELETE FROM file_data WHERE file_directory = {dbify(file_directory)}")
        con.commit()

    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.remove_file_from_database\nVar Dump:\nfile_directory: {file_directory}\nError: {e}")

def get_sum_of_user_file_sizes(token):

    global cur, con
    cur.execute(f"SELECT SUM(file_size) FROM file_data WHERE account_token={dbify(token)}")
    sum_of_file_sizes = cur.fetchone()[0]

    try:
        return format_bytes(sum_of_file_sizes)
    except Exception as e:
        print(f"Error occured when calculating AngaDriveV2.DBMS.get_sum_of_user_file_sizes\nVar Dump:\nsum_of_file_sizes: {sum_of_file_sizes}\nError: {e}")
        return format_bytes(0)
    
def get_collection_count():

    global cur, con

    cur.execute(f"SELECT COUNT(id) FROM collections")
    count = cur.fetchone()[0]

    return count

def delete_collection_from_db(collection_id):
    global cur, con
    cur.execute(f"select id from collections where collections like ?", (f'%{collection_id}%',))
    collection_ids_to_edit = [x[0] for x in cur]
    for collection_to_edit in collection_ids_to_edit:
        remove_folder_from_collection(collection_id, collection_to_edit)        # first remove the folder from all collections

    cur.execute(f"DELETE FROM collections WHERE id = ?", (collection_id,)) # then remove the folder entirely
    con.commit()


def get_all_collection_ids():
    
    global cur, con

    cur.execute("SELECT id FROM collections")
       
    ids = [x[0] for x in cur]

    return ids

def get_collection_ids_by_account_token(account_token):
    global cur, con
    cur.execute(f"SELECT id FROM collections WHERE editors LIKE ?", (f'%{account_token}%',))
    ids = [x[0] for x in cur]
    return ids

def collection_info_for_display(collection_id):
    global cur, con
    
    cur.execute(f"SELECT name, size, collections, files, editors FROM collections WHERE id = ?", (collection_id,))
    collection_info = cur.fetchone()
    collection_name = collection_info[0]
    collection_file_count = 0 if collection_info[3]=="" else len(collection_info[3].split(","))
    collection_size = format_bytes(collection_info[1])
    collection_editors_count = len(collection_info[4].split(","))
    collection_folder_count = 0 if collection_info[2]=="" else len(collection_info[2].split(","))
    return {
        "id":           collection_id, 
        "name":         truncate_string(collection_name), 
        "full_name":    collection_name,
        "file_count":   collection_file_count, 
        "size":         collection_size, 
        "editor_count": collection_editors_count,
        "folder_count": collection_folder_count
        }

def gen_collection_id():
    
    generated_id = "".join([random.choice(list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")) for x in range(15)])
    all_collection_ids = get_all_collection_ids()
    if generated_id in all_collection_ids:
        return gen_collection_id()
    else:
        return generated_id

def create_new_collection(user_token, collection_name):
    global cur, con
    collection_id = gen_collection_id()

    cur.execute(f"INSERT INTO collections (id, name, editors, size, collections, files) VALUES (?, ?, ?, ?, ?, ?)", (collection_id, collection_name, user_token, 0, "", ""))
    con.commit()

    return collection_id

def is_valid_token(token: str) -> bool:
    try:
        # Connect to the SQLite database
        global cur, con
        cursor=cur

        # Execute a query to check if the token exists in the 'accounts' table
        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE token = ?)", (token,))

        # Fetch the result
        result = cursor.fetchone()[0]
        # Close the cursor and connection

        # Return True if the token exists, else check filedata table
        if bool(result):
            return True
        else:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM file_data WHERE account_token = ?)", (token,))
            result = cursor.fetchone()[0]

            # Return True if the account exists in file data, else check collections
            if bool(result):
                return True
            
            else:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM collections WHERE editors LIKE ?)", ('%' + token + '%',))
                result = cursor.fetchone()[0]
                return bool(result)

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

def does_user_have_files(token):
    try:
        global cur, con
        # Execute a SELECT query to check if the search string exists in any row of the "token" column
        cur.execute("SELECT EXISTS(SELECT 1 FROM file_data WHERE account_token = ?)", (token,))
        result = cur.fetchone()[0]  # Fetch the result of the query
        return bool(result)
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    
def user_signup(token, display_name, email, password:str):

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    global cur, con

    cur.execute("INSERT INTO accounts(token, display_name, email, hashed_password) VALUES (?, ?, ?, ?)", (token ,display_name,email,hashed_password))

    con.commit()

def migrate_files(old_token, new_token):

    global cur, con

    cur.execute("UPDATE file_data SET account_token = ? WHERE account_token = ?", (new_token, old_token))

    con.commit()
    remove_account_from_accounts_table(old_token)

def remove_account_from_accounts_table(token):

    global cur, con

    cur.execute("DELETE FROM accounts WHERE token = ?", (token,))

    con.commit()

def email_already_exists(email):

    global cur, con

    cur.execute("SELECT COUNT(*) FROM accounts WHERE email = ?", (email,))

    result = cur.fetchone()
    try:
        return result>0
    except:
        return result[0]>0

def user_login(email: str, password:str):

    global cur, con

    cur.execute("SELECT token, hashed_password FROM accounts WHERE email = ?", (email,))
    
    result:list[str] = cur.fetchone()

    if result == [None, None]:
        return {False: "Account not found"}
    if not bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        return {False: "Authentication Failed"}
    return {True: result[0]}

def flowinity_user_signup(flowinity_data):
    global cur, con
    
    cur.execute("INSERT INTO accounts(token, display_name, email) VALUES (?, ?, ?)", (flowinity_data["token"], flowinity_data["username"], flowinity_data["email"]))
    
    con.commit()

def token_exists(token):
    return is_valid_token(token)

def count_files():

    global cur, con

    cur.execute("SELECT COUNT(*) FROM file_data")
    file_count = cur.fetchone()[0]

    return file_count

def get_all_files_size():

    global con, cur

    cur.execute(f"SELECT SUM(file_size) FROM file_data")
    result = format_bytes(cur.fetchone()[0])

    
    

    return result

@lru_cache(maxsize=100)
def get_file_name(file_path):
    try:
        global con, cur

        cur.execute(f"SELECT original_file_name FROM file_data WHERE file_directory = ?", (file_path, ))
        filename = cur.fetchone()[0]
        
        
        
        return filename
    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.get_file_name\nVar Dump:\nfile_path: {file_path}\nError: {e}")
        return "Error"

def get_collection_info_for_viewer(collection_id):
    global con, cur

    cur.execute(f"SELECT name, editors, size, files, collections FROM collections WHERE id = ?", (collection_id,))
    data:list[str] = cur.fetchone()
    
    if data==None:
        return None
    name = data[0]
    editors = data[1].split(",")
    return {
        "id"        : collection_id,
        "name"      : name,
        "editors"   : editors,
        "Size"      : format_bytes(data[2]),
        "Files"     : [] if data[3]=="" else data[3].split(", "),
        "Folders": [] if data[4]=="" else data[4].split(",")
    }

def get_file_info_for_card(file_path:str) -> dict[str,str]:
    try:
        global con, cur

        cur.execute("SELECT original_file_name, file_size, timestamp, account_token FROM file_data WHERE file_directory = ?",(file_path,))

        file_data = cur.fetchone()
        
        

        # ["unchangedfilename.png", "pgfubcid.png", "72.1KB", time.time(), "unchanged...", "http://localhost:8000/i/pgfubcid.png", True]

        return {
            "original_name" : file_data[0],                               # like original_name.png
            "file_path"     : file_path,                                  # like vb78duvhs6s.png
            "size"          : format_bytes(file_data[1]),                 # like 75.1 KB
            "timestamp"     : time.ctime(file_data[2]),                   # like wed 23 jun 2023
            "truncated_name": truncate_string(file_data[0], length=20),   # like origina....
            "file_link"     : file_link+file_path,                        # like https://file.anga.pro/i/vb78duvhs6s.png
            "previewable"   : can_be_previewed(file_path),                 # like True
            "owner_token"   : file_data[3]
        }
    except Exception as e:
        print(f"Error occured when running AngaDriveV2.DBMS.get_file_info_for_card\nVar Dump:\nfile_path: {file_path}\nfile_path_type: {type(file_path)}\nError: {e}")
        return {
            "original_name" : "Error",
            "file_path"     : "Error",
            "size"          : "Error",
            "timestamp"     : "Error",
            "truncated_name": "Error",
            "file_link"     : "Error",
            "previewable"   : False,
            "owner_token"   : "Error"
        }

def add_file_to_collection(collection_id, file_path):
    global con, cur

    cur.execute(f"SELECT size, files FROM collections WHERE id = ?", (collection_id,))
    size, files = cur.fetchone()
    size += get_file_size(os.path.join(file_directory,file_path))
    files = [] if files=="" else files.split(", ")
    files.append(file_path)
    files = ", ".join(files)
    cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (size, collection_id))
    cur.execute(f"UPDATE collections SET files = ? WHERE id = ?", (files, collection_id))
    con.commit()
    

def remove_file_from_collection_db(collection_id, file_path):
    global con, cur

    cur.execute(f"SELECT size, files FROM collections WHERE id = ?", (collection_id,))
    size, files = cur.fetchone()
    size -= get_file_size(os.path.join(file_directory, file_path))
    files = files.split(", ")
    files.remove(file_path)
    files = ", ".join(files)
    cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (size, collection_id))
    cur.execute(f"UPDATE collections SET files = ? WHERE id = ?", (files, collection_id))
    con.commit()
    

def user_has_collections(user_token: str) -> bool:
    global con, cur

    cur.execute(f"SELECT COUNT(*) FROM collections WHERE editors LIKE ?", (f'%{user_token}%',))
    count = cur.fetchone()[0]

    
    return count>0

def folder_is_in_collection(folder_id: str, collection_id: str) -> bool:
    global con, cur

    cur.execute(f"SELECT collections FROM collections WHERE id = ?", (collection_id,))
    collections = cur.fetchone()
    if collections==None:
        collections = []
    else:
        collections = collections[0].split(",")
    
    return folder_id in collections

def add_folder_to_collection(folder_id: str, collection_id: str):
    if folder_is_in_collection(folder_id=folder_id, collection_id=collection_id):
        return
    global con, cur
    cur.execute(f"SELECT size, collections FROM collections WHERE id = ?", (collection_id,))
    size, collections = cur.fetchone()
    cur.execute(f"SELECT size FROM collections WHERE id = ?", (folder_id,))
    folder_size = cur.fetchone()[0]
    if folder_is_in_collection(folder_id=collection_id, collection_id=folder_id):
        folder_size-=size
    size+=folder_size
    collections = [] if collections=="" else collections.split(",")
    collections.append(folder_id)
    collections = ",".join(collections)
    cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (size, collection_id))
    cur.execute(f"UPDATE collections SET collections = ? WHERE id = ?", (collections, collection_id))
    con.commit()
    

def remove_folder_from_collection(folder_id: str, collection_id: str):
    if not folder_is_in_collection(folder_id=folder_id, collection_id=collection_id):
        return
    global con, cur
    cur.execute(f"SELECT size, collections FROM collections WHERE id = ?", (collection_id,))
    size, collections = cur.fetchone()
    cur.execute(f"SELECT size FROM collections WHERE id = ?", (folder_id,))
    folder_size = cur.fetchone()[0]
    if folder_is_in_collection(folder_id=collection_id, collection_id=folder_id):
        folder_size-=size
    size-=folder_size
    collections: list[str] = collections.split(",")
    collections.remove(folder_id)
    collections = ",".join(collections)
    cur.execute(f"UPDATE collections SET size = ? WHERE id = ?", (size, collection_id))
    cur.execute(f"UPDATE collections SET collections = ? WHERE id = ?", (collections, collection_id))
    con.commit()
    

def token_exists_in_accounts_table(token):
    global con, cur
    cur.execute("SELECT COUNT(*) FROM accounts WHERE token = ?", (token,))
    result = cur.fetchone()[0]
    
    return result>0

@asynccontextmanager
async def lifespan(discard=None):
    global con
    print("Database connection opened")
    load_database()
    yield
    con.commit()
    con.close()
    print("Database connection closed")
