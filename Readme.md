# Study Hours Tracking

A background tracking application designed to run as a systemd service and monitor your study time by keeping track of the specific applications you have open.

## Features
- **Background Service**: Runs smoothly in the background using systemd.
- **Process Matching**: Monitors processes (like VS Code, Chrome) securely via substring matching to track your study sessions.
- **Human-Readable Data**: Stores all your studying time history in a human-readable JSON file (`data/study_data.json`) in the format `Xh Ym Zs`.
- **Lightweight Logging**: Optimizes file I/O by only saving logs when your state changes or periodically while active.
- **Graceful Shutdown**: Hooks into system termination signals (SIGTERM/SIGINT) to ensure data is properly saved before shutting down.

## Requirements
- Python 3
- `psutil` (can be installed via `pip install psutil` or `pip install -r requirements.txt`)

## Usage

### 1. Configuration
Open `src/config.py` and modify the `STUDY_APPS` array with the lowercase names of applications you want to track (e.g., `["chrome", "code", "antigravity-ide"]`).

### 2. Run Manually
You can test the tracker by running:
```bash
python main.py
```

### 3. Run as Systemd Service (Recommended)
This tool is designed to run silently as a user-level background service.

1. Create a service file `~/.config/systemd/user/study-hours-tracking.service`:
```ini
[Unit]
Description=Study Hours Background Tracker
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/study_hours_tracking
ExecStart=/usr/bin/python3 main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```
2. Reload daemon, enable, and start the service:
```bash
systemctl --user daemon-reload
systemctl --user enable study-hours-tracking.service
systemctl --user start study-hours-tracking.service
```

### Checking Status and Logs
- **Service Status:** `systemctl --user status study-hours-tracking.service`
- **View Live Logs:** `journalctl --user -u study-hours-tracking.service -f`
- **View Saved Data:** Look inside `data/study_data.json`

## Files
- `main.py`: Entry point, sets up signal handlers.
- `src/tracker.py`: Contains the main logic for process checking and periodic saving.
- `src/storage.py`: Manages reading/writing the `study_data.json` state.
- `src/config.py`: Holds configurable settings.
