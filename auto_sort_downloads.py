import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the Downloads directory and the target folders for each file type
# DOWNLOADS_DIR points to the current user's Downloads folder
DOWNLOADS_DIR = os.path.join(os.path.expanduser('~'), 'Downloads')

# TARGET_DIRS defines the mapping of file extensions to their respective folders
# Each key represents a folder name, and the value is a list of file extensions
TARGET_DIRS = {
    'Documents': ['.pdf', '.docx', '.txt', '.xls', '.xlsx'],  # Document files
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],              # Image files
    'Videos': ['.mp4', '.mov', '.avi', '.ogg'],               # Video files
    'Music': ['.mp3', '.wav'],                                # Music files
    'Archives': ['.zip', '.rar', '.7z'],                      # Compressed archive files
    'Presentation': ['.pptx'],                                # Presentation files (e.g., PowerPoint)
    'Application': ['.exe'],                                  # Executable files
    'Code': ['.java', '.py', '.cs','.html']                           # Code files for Java, Python, C#
}

# Define a custom event handler class inheriting from FileSystemEventHandler
# This will respond to file system events such as modifications in the Downloads folder
class DownloadHandler(FileSystemEventHandler):
    # on_modified is triggered whenever the content in the Downloads directory changes
    def on_modified(self, event):
        # Iterate over all files in the Downloads directory
        for filename in os.listdir(DOWNLOADS_DIR):
            file_path = os.path.join(DOWNLOADS_DIR, filename)  # Full path of the file

            # Skip if the item is a directory or a hidden file (files starting with '.')
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue

            # Extract the file extension
            _, file_extension = os.path.splitext(filename)
            
            # Find the appropriate folder based on the file extension
            for folder, extensions in TARGET_DIRS.items():
                # If the file's extension matches any in the target list, move it
                if file_extension.lower() in extensions:
                    move_file_to_folder(file_path, folder)
                    break  # Stop checking once the correct folder is found

# Function to move a file to the designated folder
# It creates the target folder if it doesn't exist and then moves the file
def move_file_to_folder(file_path, folder_name):
    folder_path = os.path.join(DOWNLOADS_DIR, folder_name)  # Full path of the target folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the target folder if it doesn't exist
    
    try:
        # Move the file to the target folder
        shutil.move(file_path, folder_path)
        print(f"Moved: {file_path} to {folder_path}")
    except Exception as e:
        # Handle any errors during file movement
        print(f"Failed to move {file_path}: {e}")

# The main execution block starts here
if __name__ == "__main__":
    # Create an event handler instance of DownloadHandler
    event_handler = DownloadHandler()
    
    # Create an observer that will monitor the Downloads directory
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_DIR, recursive=False)  # Schedule it to monitor Downloads folder
    observer.start()  # Start the observer

    print(f"Monitoring {DOWNLOADS_DIR}...")  # Notify the user that monitoring has started

    try:
        # Keep the script running indefinitely
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the observer when the script is interrupted (e.g., by pressing Ctrl + C)
        observer.stop()

    observer.join()  # Wait for the observer to finish
