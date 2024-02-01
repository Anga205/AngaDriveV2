def format_time(number: int) -> str:
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