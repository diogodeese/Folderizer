import os
import time
import shutil
from config_reader import read_config
from watchdog.events import FileSystemEventHandler

config = read_config()

DELAY_SECONDS = config["DELAY_SECONDS"]
FOLDER_MAPPING = config["FOLDER_MAPPING"]
DESTINATION_DIR = config["DESTINATION_DIR"]

# Dictionary to track file sizes for monitoring
file_sizes = {}

class FileOrganizer(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_extension = os.path.splitext(file_path)[1][1:].lower()

            for folder, extensions in FOLDER_MAPPING.items():
                if file_extension in extensions:
                    self.wait_for_download_complete(file_path, folder)
                    break

    def wait_for_download_complete(self, file_path, folder):  # Pass 'folder' as an argument
        while True:
            try:
                size = os.path.getsize(file_path)
                if size == file_sizes.get(file_path):
                    self.move_file(file_path, folder)  # Pass 'folder' to move_file() as well
                    break
                file_sizes[file_path] = size
            except FileNotFoundError:
                pass  # File may be deleted during checking
            time.sleep(1)  # Wait for a second before checking again

    def move_file(self, file_path, folder):
        destination = os.path.join(DESTINATION_DIR, folder)
        new_file_path = os.path.join(destination, os.path.basename(file_path))
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_path} to {new_file_path}")