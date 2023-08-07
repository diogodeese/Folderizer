import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

# Read the configuration from the config.json file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

FOLDER_MAPPING = config["folder_mapping"]
DOWNLOAD_DIR = config["DOWNLOAD_DIR"]
DESTINATION_DIR = config["DESTINATION_DIR"]
DELAY_SECONDS = config["DELAY_SECONDS"]

class FileOrganizer(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        _, ext = os.path.splitext(file_path)
        ext = ext[1:].lower()  # Remove the dot and convert to lowercase

        if ext:
            time.sleep(DELAY_SECONDS)  # Adding a delay before moving the file
            if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                target_folder = "other"  # Default folder for unknown extensions

                for folder, extensions in FOLDER_MAPPING.items():
                    if ext in extensions:
                        target_folder = folder
                        break

                target_folder_path = os.path.join(DESTINATION_DIR, target_folder)
                if not os.path.exists(target_folder_path):
                    try:
                        os.makedirs(target_folder_path)
                    except OSError as e:
                        print(f"Error creating folder: {e}")
                        return

                try:
                    shutil.move(file_path, os.path.join(target_folder_path, os.path.basename(file_path)))
                    print(f"File moved: {file_path} -> {target_folder_path}")
                except Exception as e:
                    print(f"Error moving file: {e}")
            else:
                print(f"Incomplete or non-existent file: {file_path}")

if __name__ == "__main__":
    event_handler = FileOrganizer()
    observer = Observer()
    observer.schedule(event_handler, path=DOWNLOAD_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()