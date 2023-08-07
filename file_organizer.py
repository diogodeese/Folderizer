import os
import time
import shutil
from config_reader import read_config
from watchdog.events import FileSystemEventHandler

config = read_config()

DELAY_SECONDS = config["DELAY_SECONDS"]
FOLDER_MAPPING = config["folder_mapping"]
DESTINATION_DIR = config["DESTINATION_DIR"]

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