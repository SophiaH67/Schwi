# Function to format a number of seconds into a human readable string
# e.g. 62 -> 1m2s
def format_seconds(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m{seconds % 60}s"
    elif seconds < 86400:
        return f"{seconds // 3600}h{(seconds // 60) % 60}m"
    else:
        return f"{seconds // 86400}d{(seconds // 3600) % 24}h"
