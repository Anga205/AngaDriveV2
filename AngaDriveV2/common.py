import datetime, time, os, random, re, psutil, subprocess, json, builtins, requests, shutil, threading

accounts={}
file_data={}
activity=[]
collections={}

app_data_dir = "uploaded_files"
def app_data_dir_function():
    return app_data_dir
file_directory = os.path.join(app_data_dir,"i")
database_directory = os.path.join(app_data_dir,'rx.db')

server_config_directory = os.path.join(app_data_dir, "server_config.json")
try:
    with open(server_config_directory, "r") as f:
        server_config = json.load(f)
except FileNotFoundError:
    server_config = {
        "api_url": input("Enter API url (or press enter to use http://localhost:8000): ").strip() or "http://localhost:8000",
    }
    if server_config["api_url"]=="http://localhost:8000":
        server_config['file_visible_api'] = f"{server_config['api_url']}"
        server_config["deploy_url"] = "http://localhost:3000"
    else:
        server_config['deploy_url'] = input("Enter Deploy url: (or press enter to use http://localhost:3000): ").strip() or "http://localhost:3000"
        server_config['file_visible_api'] = input(f"Enter file visible api (or press enter to use {server_config['api_url']}): ") or f"{server_config['api_url']}"
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    with open(server_config_directory, "w") as f:
        json.dump(server_config, f)
    

app_link = server_config['deploy_url']

file_link = f"{server_config['file_visible_api']}/i/"
download_link = f"{server_config['file_visible_api']}/download/"

truncate_string = lambda string, length=19: string if len(string)<=length else string[0:length]+"..."

def dbify(var):
    if var==None:
        return "NULL"
    if type(var)==type(0):
        return str(var)
    if type(var)==type(""):
        if "'" not in var:
            return "'"+var+"'"
        elif '"' not in var:
            return '"'+var+'"'
        else:
            return "'"+("".join([("''" if x=="'" else x) for x in var]))+"'"

def gen_filename(filename):
    generated_name = ""
    allowed_values = "qwertyuiopasdfghjklzxcvbnm1234567890"
    generated_name = "".join(random.choices(allowed_values, k=12))

    if len(filename.split("."))>1:
        generated_name = generated_name + "." + filename.split(".")[-1]
    
    if generated_name in file_data:
        return gen_filename(filename)   #if generated filename already exists in database, then go generate a new one
    
    return generated_name #if generated filename doesnt already exist, then return the generated one

def gen_token():
    a="qwertyuiopasdfghjklzxcvbnm"
    a=a+a.upper()
    a=a+"1234567890"
    return "".join(random.choices(a, k=10))+"."+"".join(random.choices(a, k=20))+"."+str(round(time.time()))

def time_ago(timestamp):        # calculates how long ago a given time.time()
    current_time = datetime.datetime.now()
    input_time = datetime.datetime.fromtimestamp(timestamp)
    time_difference = current_time - input_time

    seconds = time_difference.seconds
    days = time_difference.days
    years = days // 365
    months = days // 30
    weeks = days // 7

    if years > 0:
        return f"{years} {'year' if years == 1 else 'years'} ago"
    elif months > 0:
        return f"{months} {'month' if months == 1 else 'months'} ago"
    elif weeks > 0:
        return f"{weeks} {'week' if weeks == 1 else 'weeks'} ago"
    elif days > 0:
        return f"{days} {'day' if days == 1 else 'days'} ago"
    elif hours := time_difference.seconds // 3600:
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    elif minutes := seconds // 60:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    else:
        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"


def format_time(number: int) -> str:
    if number == None:
        return format_time(0)
    # Check if the input number is negative
    if number < 0:
        return "Negative numbers are not supported"

    # Round off the number to the nearest integer
    number = round(number)

    # Initialize variables to store years, months, days, hours, minutes, and seconds
    years = number // (365 * 24 * 3600)
    number %= (365 * 24 * 3600)
    months = number // (30 * 24 * 3600)
    number %= (30 * 24 * 3600)
    days = number // (24 * 3600)
    number %= (24 * 3600)
    hours = number // 3600
    number %= 3600
    minutes = number // 60
    seconds = number % 60

    # Create a list to store time components
    time_components = []

    # Add years, if present
    if years > 0:
        time_components.append(f"{years}y")

    # Add months, if present
    if months > 0:
        time_components.append(f"{months}mo")

    # Add days, if present
    if days > 0:
        time_components.append(f"{days}d")

    # Add hours, if present
    if hours > 0:
        time_components.append(f"{hours}h")

    # Add minutes, if present
    if minutes > 0:
        time_components.append(f"{minutes}m")

    # Add seconds, if present or if the input is 0
    if seconds >= 0 or len(time_components) == 0:
        time_components.append(f"{seconds}s")

    # Join the time components and return as a formatted string
    return ' '.join(time_components)

def calls_per_day(timestamps: list[int]) -> dict: #dict of length 7
    days_counts = {}
    today = datetime.datetime.now().date()
    
    for ts in timestamps:
        dt = datetime.datetime.fromtimestamp(ts)
        day = dt.date()
        
        if (today - day).days <= 6:
            formatted_day = dt.strftime('%b %d')
            if formatted_day in days_counts:
                days_counts[formatted_day] += 1
            else:
                days_counts[formatted_day] = 1
    
    last_week_dates = [(today - datetime.timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
    result = {date: days_counts.get(date, 0) for date in last_week_dates}
    
    return result

def format_bytes(bytes):
    if bytes == None:
        return 0
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def get_file_size(file_path: str) -> int:
    # Convert to an absolute path if it's a relative path
    file_path = os.path.abspath(file_path)
    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)
    return file_size

def delete_file(file_to_be_deleted):
    os.remove(file_directory, file_to_be_deleted)


def create_assets_folder():

    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
        print("Assets folder created successfully.")

create_assets_folder()


def is_valid_email(email: str) -> bool:

    email_pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(email_pattern, email))

def can_be_previewed(filename:str) -> bool:
    # Get the file extension
    file_extension = filename.split('.')[-1].lower()

    # List of file extensions that can be previewed in most modern browsers
    previewable_extensions = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'txt', 'html', "webm"]

    # Check if the file extension is in the list of previewable extensions
    return file_extension in previewable_extensions

def get_system_info():
    cpu_usage = psutil.cpu_percent(percpu=True)
    ram = psutil.virtual_memory()
    ram_usage_percentage = ram.percent
    if on_rpi:
        temp = get_cpu_temperature()
    else:
        temp = 0.0
    system_info = {
        "cpu_usage": cpu_usage,
        "ram_usage_percentage": ram_usage_percentage,
        "temperature": f"{temp}°C",
        "total_ram": format_bytes(ram.total),
        "used_ram": format_bytes(ram.used),
    }
    return system_info

last_temp_check_time=0
last_temp_seen=0
def get_cpu_temperature():
    global last_temp_check_time, last_temp_seen
    if round(last_temp_check_time/2)==round(time.time()/2):
        return last_temp_seen
    last_temp_check_time = time.time()
    try:
        output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
        temperature = float(output.split('=')[1].split("'")[0])
        last_temp_seen = round(temperature,2)
        return round(temperature,2)
    except Exception as e:
        try:
            result = subprocess.run(['sensors'], stdout=subprocess.PIPE, text=True)
            for line in result.stdout.split('\n'):      # for this part of the code, run these first:
                if 'Core 0' in line:                    # sudo apt-get install lm-sensors
                    temp_str = line.split()[2]          # sudo sensors-detect
                    last_temp_seen = temp_str[1:-2]
                    return temp_str[1:-2]
        except:
            return 0.0
    
on_rpi=bool(get_cpu_temperature())

def print(*args, end="\n"):
    debug_file=os.path.join(app_data_dir, "debug.log")
    args=list(args)
    for i in range(len(args)):
        if type(args[i])==type({}):
            args[i]="\n"+json.dumps(args[i], indent=4)
        elif type(args[i])==type([]):
            args[i]="\n"+json.dumps(args[i], indent=4)
        else:
            args[i]=str(args[i])
    args=[f"[{time.ctime(time.time())}]"]+[" ".join(args)]
    threading.Thread(target= lambda: builtins.print(*args, end=end)).start()

    if os.path.exists(debug_file):
        with open(debug_file, "a") as f:
            f.write(" ".join(args))
            f.write(end)
    else:
        with open(debug_file, "w") as f:
            f.write(" ".join(args))
            f.write(end)


def is_valid_http_url(url: str, is_github_repo: bool = False) -> bool:
    regex = re.compile(
        r'^(https?):\/\/'  # Only allow http and https
        r'(\w+(\-\w+)*\.)+[a-z]{2,}'  # Domain
        r'(:\d+)?'  # Optional port
        r'(\/[^\s]*)?'  # Resource path
        r'(\.[a-zA-Z0-9]+)?$'  # File extension
    )

    if is_github_repo:
        regex = re.compile(
            r'(^(https?):\/\/)?'  # optional http(s) prefix
            r'(github\.com\/)'  # "github.com/" prefix
            r'([\w-]+)\/'  # Username
            r'([\w-]+)$'  # Repository name
            r'(.git)?' # Optional .git suffix
        )
    
    if re.match(regex, url):
        return True
    
    return False

def url_exists(url: str) -> bool:
    try:
        rcv = requests.head(
            url=url,
            allow_redirects=True,
            timeout=(5, 10)
        )

        if rcv.status_code == 200:
            return True
    except Exception as e:
        print(f"Error resolving {url}: {e}")
        return False
    print(f"Error resolving {url}: {rcv.status_code}")
    return False

def is_valid_github_repo(url: str) -> bool:
    try:
        # Send a GET request to the GitHub API to check if the repository exists
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def git_clone(repo_url: str, dest: str) -> bool:
    try:
        # Clone the repository using the git command
        subprocess.run(['git', 'clone', repo_url, dest], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
def move_files_to_upload_dir(src_dir):
    file_info = {}
    
    for root, dirs, files in os.walk(src_dir):
        # Ignore directories that start with .
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            src_path = os.path.join(root, file)
            new_filename = gen_filename(file)
            dest_path = os.path.join(file_directory, new_filename)
            
            shutil.move(src_path, dest_path)
            
            file_info[new_filename] = {
                "original_file_name": file,
                "file_size": get_file_size(dest_path),
                "file_directory": root.removeprefix(f"{src_dir}")
            }
    
    shutil.rmtree(src_dir)  # Delete the source directory after moving the files
    
    return file_info