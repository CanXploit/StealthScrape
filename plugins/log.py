from datetime import datetime

# ANSI Color Codes
COLORS = {
    "INFO": "\033[94m",   # Blue
    "SUCCESS": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",    # Red
    "RESET": "\033[0m"     # Reset color
}

# Log messages dictionary
LOG_MESSAGES = {
    "get_links": ("INFO", "Getting links for domain {}..."),
    "links_grabbed": ("SUCCESS", "Grabbed {} links."),
    "file_saved": ("SUCCESS", "Links saved to file: {}"),
    "continue_with_extensions": ("INFO", "Continuing with extension selection..."),
    "extensions_selected": ("SUCCESS", "Selected extensions: {}"),
    "filtered_links_saved": ("SUCCESS", "Filtered links saved to: {}"),
    "no_filtered_links": ("ERROR", "No matching links found."),
    "error_grabbing_links": ("ERROR", "Error grabbing links: {}"),
    "invalid_choice": ("ERROR", "Invalid input. Please choose 'y' or 'n'."),
    "check": ("INFO", "Checking host domain...."),
    "check_alive": ("SUCCESS", "The domain is alive!"),
    "check_not_alive": ("ERROR", "The domain is NOT alive!"),
    "get_subdomains": ("INFO", "Fetching subdomains..."),
    "subdomain_found": ("SUCCESS", "Found subdomain: {}"),
    "grab_files": ("INFO", "Grabbing files..."),
    "silent_grab": ("INFO", "Performing silent grab..."),
    "proxy_fog": ("INFO", "Sending proxy fog requests..."),
    "downloading": ("INFO", "Downloading file {}")
}

def log(event, *args):
    if event in LOG_MESSAGES:
        level, message = LOG_MESSAGES[event]
        if args:
            message = message.format(*args)

        timestamp = datetime.now().strftime("%H:%M:%S")
        color = COLORS.get(level, COLORS["INFO"])
        
        print(f"{color}[{level}] [{timestamp}]: {message}{COLORS['RESET']}")
