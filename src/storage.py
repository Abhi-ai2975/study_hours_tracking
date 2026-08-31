import json
import os
import re
from src.config import DATA_FILE

def seconds_to_str(total_seconds: int) -> str:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

def str_to_seconds(time_str: str) -> int:
    match = re.match(r"(?:(\d+)h\s*)?(?:(\d+)m\s*)?(?:(\d+)s)?", time_str)
    if match:
        h = int(match.group(1) or 0)
        m = int(match.group(2) or 0)
        s = int(match.group(3) or 0)
        return h * 3600 + m * 60 + s
    return 0

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
            # Migrate old single-day format
            if "date" in data and "seconds" in data:
                return {data["date"]: data["seconds"]} if data["date"] else {}
                
            # Convert loaded data back to integer seconds for the tracker to use
            parsed_data = {}
            for date_key, time_val in data.items():
                if isinstance(time_val, int):
                    parsed_data[date_key] = time_val
                elif isinstance(time_val, str):
                    parsed_data[date_key] = str_to_seconds(time_val)
            return parsed_data
            
    except json.JSONDecodeError:
        return {}

def save_data(data: dict) -> None:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Convert integer seconds to readable string format for JSON
    formatted_data = {date_key: seconds_to_str(seconds) for date_key, seconds in data.items()}
    
    with open(DATA_FILE, 'w') as f:
        json.dump(formatted_data, f, indent=4)