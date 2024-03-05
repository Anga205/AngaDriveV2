import datetime, time, os, random

file_directory = os.path.join(os.getcwd(), "file_handler", "assets")

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


def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def format_bytes(bytes):
    if bytes == None:
        return 0
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def get_formatted_directory_size(directory = file_directory):
    size_in_bytes = get_directory_size(directory)
    return format_bytes(size_in_bytes)

def count_files(directory = file_directory):
    file_count = 0
    for dirpath, _, filenames in os.walk(directory):
        file_count += len(filenames)
    return file_count

def get_file_size(file_path: str) -> int:
    # Convert to an absolute path if it's a relative path
    file_path = os.path.abspath(file_path)
    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)
    return file_size

def delete_file(file_to_be_deleted):
    os.remove(file_directory, file_to_be_deleted)
