import signal
import sys
from src.tracker import run_tracker, stop_tracker

def handle_shutdown(signum, frame):
    stop_tracker()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        run_tracker()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)