import os

# Target process names (substring match, make sure these are lowercase)
# Since this uses substring matching, "chrome" will match both "chrome" (Linux) and "chrome.exe" (Windows).
# So you generally don't need to add ".exe" to these names.
STUDY_APPS = ["chrome", "code", "antigravity-ide"]

# Path to the data file (absolute path relative to this script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "study_data.json")

# How often the script checks your running apps (in seconds)
CHECK_INTERVAL = 5