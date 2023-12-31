import os
import time
import threading
from config_reader import read_config
from watchdog.observers import Observer
from file_organizer import FileOrganizer
from icon import run_icon, wait_for_icon_thread

config = read_config()

DOWNLOAD_DIR = config["DOWNLOAD_DIR"]
DELAY_SECONDS = config["DELAY_SECONDS"]
FOLDER_MAPPING = config["FOLDER_MAPPING"]
DESTINATION_DIR = config["DESTINATION_DIR"]

# Create destination folders if they don't exist
for folder in FOLDER_MAPPING:
    folder_path = os.path.join(DESTINATION_DIR, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

if __name__ == "__main__":
    # Start the system tray icon in a separate thread
    icon_thread = threading.Thread(target=run_icon)
    icon_thread.daemon = True
    icon_thread.start()

    event_handler = FileOrganizer()
    observer = Observer()
    observer.schedule(event_handler, path=DOWNLOAD_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(DELAY_SECONDS)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    # Wait for the icon thread to complete before exiting the main thread
    wait_for_icon_thread()
    print("Program has exited gracefully.")