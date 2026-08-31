import psutil
import time
import logging
from datetime import datetime
from src.config import STUDY_APPS, CHECK_INTERVAL
from src.storage import load_data, save_data, seconds_to_str

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

is_running = True

def stop_tracker():
    global is_running
    is_running = False
    logging.info("Initiating tracker shutdown...")

def check_if_studying() -> bool:
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and any(app in proc.info['name'].lower() for app in STUDY_APPS):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def run_tracker():
    logging.info("Study Tracker Started! Monitoring in the background...")
    
    data = load_data()
    last_save_time = time.time()
    was_studying = False
    
    while is_running:
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if current_date not in data:
            data[current_date] = 0
            
        currently_studying = check_if_studying()
        
        if currently_studying:
            data[current_date] += CHECK_INTERVAL
            if not was_studying:
                logging.info(f"Started studying! Total today so far: {seconds_to_str(data[current_date])}")
            was_studying = True
        else:
            if was_studying:
                logging.info(f"Stopped studying. Total today: {seconds_to_str(data[current_date])}")
                save_data(data) # Save immediately when stopping
            was_studying = False
            
        # Periodic save every 60 seconds if studying
        if currently_studying and time.time() - last_save_time >= 60:
            save_data(data)
            last_save_time = time.time()
            logging.info(f"Studying... Total today: {seconds_to_str(data[current_date])}")
            
        time.sleep(CHECK_INTERVAL)
        
    # Final save on exit
    save_data(data)
    logging.info("Tracker stopped and data saved.")