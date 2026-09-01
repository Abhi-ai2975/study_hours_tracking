# Study Hours Tracking

A background tracking application designed to run as a systemd service and monitor your study time by keeping track of the specific applications you have open.

## Features
- **Background Service**: Runs smoothly in the background using systemd.
- **Process Matching**: Monitors processes (like VS Code, Chrome) securely via substring matching to track your study sessions.
- **Human-Readable Data**: Stores all your studying time history in a human-readable JSON file (`data/study_data.json`) in the format `Xh Ym Zs`.
- **Lightweight Logging**: Optimizes file I/O by only saving logs when your state changes or periodically while active.
- **Graceful Shutdown**: Hooks into system termination signals (SIGTERM/SIGINT) to ensure data is properly saved before shutting down.
- **Floating Widget**: Includes a standalone, always-on-top GUI widget (`gui.py`) to see your current study hours anywhere.

## Requirements
- Python 3
- `psutil` (can be installed via `pip install psutil` or `pip install -r requirements.txt`)
- `tkinter` (usually built-in, but on some Linux distros you may need to install `python3-tk`)

## Usage

### 1. Configuration
Open `src/config.py` and modify the `STUDY_APPS` array with the lowercase names of applications you want to track (e.g., `["chrome", "code", "antigravity-ide"]`).
*Note for Windows users:* Because the tracker uses substring matching, `"chrome"` will successfully match both `"chrome"` on Linux and `"chrome.exe"` on Windows. You generally do not need to add `.exe` to the app names.

### 2. Floating GUI Widget
To see your live study time on your screen, simply run:
```bash
python gui.py
```
*(On Windows, you can use `pythonw gui.py` to run it without a terminal window).* 
You can click and drag the widget anywhere on your screen. Click the **X** to close it.

### 3. Run Manually
You can test the tracker by running:
```bash
python main.py
```

### 3. Run in the Background (Linux - Systemd)
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
3. Check status: `systemctl --user status study-hours-tracking.service`

### 4. Run in the Background (Windows)
To run this script automatically in the background on Windows, you have two options:

**Option A: Startup Folder (Easiest)**
1. Create a new text file and paste the following:
   ```bat
   @echo off
   cd C:\path\to\study_hours_tracking
   start /B pythonw main.py
   ```
   *(Note: using `pythonw` instead of `python` runs it without a terminal window)*
2. Save this file as `tracker.bat`.
3. Press `Win + R`, type `shell:startup`, and press Enter.
4. Move your `tracker.bat` file into that Startup folder. It will now run invisibly every time you log in.

**Option B: Task Scheduler (More robust)**
1. Open Windows Task Scheduler.
2. Click "Create Basic Task..." and name it "Study Hours Tracker".
3. Trigger: "When I log on".
4. Action: "Start a program".
5. Program/script: `pythonw` (this hides the console window).
6. Add arguments: `main.py`
7. Start in: `C:\path\to\study_hours_tracking`
8. Finish the setup and ensure it is enabled.

### Viewing Saved Data
Regardless of OS, look inside `data/study_data.json` to see your tracked hours.

## Files
- `main.py`: Entry point, sets up signal handlers.
- `src/tracker.py`: Contains the main logic for process checking and periodic saving.
- `src/storage.py`: Manages reading/writing the `study_data.json` state.
- `src/config.py`: Holds configurable settings.
