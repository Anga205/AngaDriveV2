import sqlite3, os, time, bcrypt
from AngaDriveV2.common import *

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
                    hashed_password TEXT
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

            cur.execute('''
                CREATE TABLE collections(
                        id TEXT PRIMARY KEY,
                        timestamp INTEGER,
                        name TEXT,
                        editors TEXT,
                        data TEXT
                )
                        ''')
            con.commit()

            print("Database and table created successfully.")

create_database()


def account_info(token):
    con = sqlite3.connect(database_directory)
    cur=con.cursor()
    cur.execute(f"SELECT token, display_name, email FROM accounts WHERE token={dbify(token)}")
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

def get_user_count():
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"SELECT COUNT(DISTINCT account_token) FROM file_data")
    try:
       count = int(cur.fetchone()[0])
    except Exception as e:
        print(f'Error occured when calculating get_user_count: {e}')
        count = 0
    con.close()
    return count

def fetch_activity_from_last_week():
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"SELECT timestamps FROM activity")
    output = [x[0] for x in list(cur)]
    con.close()
    return calls_per_day(output)

def create_new_account_without_info(token):
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"INSERT INTO accounts (token) VALUES ({dbify(token)});")
    con.commit()
    con.close()

def does_filename_already_exist(filename_to_check: str) -> bool:
    
    con = sqlite3.connect(database_directory)
    c = con.cursor()

    # Execute a SELECT query to check if the string is present in any row of the table
    c.execute(f"SELECT * FROM file_data WHERE file_directory = {dbify(filename_to_check)}")
    
    row = c.fetchone()

    con.close()

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
    
    original_file_name= dbify(original_file_name)
    file_directory = dbify(file_directory)
    account_token = dbify(account_token)
    file_size = dbify(file_size)

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"INSERT INTO file_data (original_file_name, file_directory, account_token, file_size, timestamp) VALUES ({original_file_name}, {file_directory}, {account_token}, {file_size}, {dbify(round(time.time()))})")
    con.commit()
    con.close()

def get_all_user_files_for_display(account_token):
    
    account_token = dbify(account_token)

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"SELECT original_file_name, file_directory, file_size, timestamp FROM file_data WHERE account_token={account_token}")

    rows = [[x[0], x[1], format_bytes(x[2]), time.ctime(x[3])] for x in cur]

    con.close()

    return rows

def remove_file_from_database(file_directory):
    
    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"DELETE FROM file_data WHERE file_directory = {dbify(file_directory)}")
    con.commit()

    con.close()

def get_sum_of_user_file_sizes(token):

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"SELECT SUM(file_size) FROM file_data WHERE account_token={dbify(token)}")
    sum_of_file_sizes = cur.fetchone()[0]

    con.close()
    try:
        return format_bytes(sum_of_file_sizes)
    except Exception as e:
        print(f"Error occured when calculating AngaDriveV2.DBMS.get_sum_of_user_file_sizes\nVar Dump:\nsum_of_file_sizes: {sum_of_file_sizes}\nError: {e}")
        return format_bytes(0)
    
def get_collection_count():

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"SELECT COUNT(id) FROM collections")
    count = cur.fetchone()[0]

    cur.close()
    con.close()

    return count

def get_all_collection_ids():
    
    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("SELECT id FROM collections")
       
    ids = [x[0] for x in cur]

    con.close()
    return ids


def gen_collection_id():
    
    generated_id = "".join([random.choice(list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")) for x in range(15)])

    if generated_id in get_all_collection_ids():
        return gen_collection_id()
    else:
        return generated_id

def create_new_collection(token, collection_name):
    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute(f"INSERT INTO collections (id, timestamp, name, editors, data) VALUES ({dbify(gen_collection_id())}, {dbify(time.time())}, {dbify(collection_name)}, {dbify(token)}, {dbify(str([]))})")
    con.commit()

def is_valid_token(token: str) -> bool:
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_directory)
        cursor = conn.cursor()

        # Execute a query to check if the token exists in the 'accounts' table
        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE token = ?)", (token,))
        
        # Fetch the result
        result = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return True if the token exists, False otherwise
        return bool(result)
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

def does_user_have_files(token):
    try:
        conn = sqlite3.connect(database_directory)
        cursor = conn.cursor()
        # Execute a SELECT query to check if the search string exists in any row of the "token" column
        cursor.execute("SELECT EXISTS(SELECT 1 FROM file_data WHERE account_token = ?)", (token,))
        result = cursor.fetchone()[0]  # Fetch the result of the query
        conn.close()
        return bool(result)
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    
def user_signup(token, display_name, email, password:str):

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("UPDATE accounts SET display_name = ?, email = ?, hashed_password = ? WHERE token = ?", (display_name, email, hashed_password, token))

    con.commit()
    con.close()

def move_files_after_login(old_token, new_token):

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("UPDATE file_data SET account_token = ? WHERE account_token = ?", (old_token, new_token))

    con.commit()
    con.close()
    remove_account_from_accounts_table(old_token)

def remove_account_from_accounts_table(token):

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("DELETE FROM accounts WHERE token = ?", (token,))

    con.commit()
    con.close()

def email_already_exists(email):

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM accounts WHERE email = ?", (email,))

    result = cur.fetchone()
    con.close()
    try:
        return result>0
    except:
        return result[0]>0

def user_login(email: str, password:str):

    con = sqlite3.connect(database_directory)
    cur = con.cursor()

    cur.execute("SELECT token, hashed_password FROM accounts WHERE email = ?", (email,))
    
    result:list[str] = cur.fetchone()
    con.close()

    if result == None:
        return {False: "Account not found"}
    if not bcrypt.checkpw(result[1].encode('utf-8'), password.encode('utf-8')):
        return {False: "Authentication Failed"}
    return {True: result[0]}