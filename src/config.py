import os

# Target process names (substring match, make sure these are lowercase)
STUDY_APPS = ["chrome", "code", "antigravity-ide"]

# Path to the data file (absolute path relative to this script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "study_data.json")

# How often the script checks your running apps (in seconds)
CHECK_INTERVAL = 5