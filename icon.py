import os
import pystray
import threading
from PIL import Image
from pystray import MenuItem as item

# Signal the main thread to wait for the icon thread to complete
exit_event = threading.Event()

# Run when the user clicks the "Exit" menu item
def on_exit_clicked(icon, item):
    print("Exiting the program...")
    # Clean up any resources or tasks before exiting (if needed)
    icon.stop()
    exit_event.set()
    os._exit(0)

# Create the icon and menu
image = Image.open("assets/icon.jpg")
icon = pystray.Icon("Folderizer", image, "Folderizer", menu=pystray.Menu(item("Exit", on_exit_clicked)))

# Run the icon in the system tray
def run_icon():
    icon.run()

# Wait for the icon thread to complete
def wait_for_icon_thread():
    exit_event.wait()
