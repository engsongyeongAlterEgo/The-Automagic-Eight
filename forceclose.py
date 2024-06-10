import tkinter as tk
import os
import threading
import time
import shutil
import pathway
from datetime import datetime
import subprocess
import watchdog.events
import watchdog.observers

class FileModifiedHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, program_to_close):
        self.last_modified = datetime.now()
        self.program_to_close = program_to_close
        self.timer_started = False

    def start_timer(self):
        self.timer_started = True
        threading.Timer(5, self.launch_program).start()

    def launch_program(self):
        subprocess.run([pathway.exe_path])
        self.timer_started = False

    def on_modified(self, event):
        # if datetime.now() - self.last_modified < timedelta(seconds=1):
        #     subprocess.call(['taskkill', '/F', '/IM', self.program_to_close])
        # else:
        #     self.last_modified = datetime.now()
        
        if not self.timer_started :
            self.start_timer()

        subprocess.call(['taskkill', '/F', '/IM', self.program_to_close])   
        print(f'Event type: {event.event_type}  path : {event.src_path}')
        print(event.is_directory) # This attribute is also available
        if not event.is_directory:
            # Force close the program
            #subprocess.call(['taskkill', '/F', '/IM', self.program_to_close])
            print(f'event type: {event.event_type}  path : {event.src_path}')
            # Get the file name from the event source path
            file_name = os.path.basename(event.src_path)
            print(f'File name: {file_name}')
            shutil.copyfile(event.src_path, pathway.dst_path + '\\' + file_name)
            # subprocess.run([pathway.exe_path])

def monitor_folder():
    # Create a watchdog observer
    global observer
    observer = watchdog.observers.Observer()

    # Create a file modified event handler
    event_handler = FileModifiedHandler(pathway.close_path)

    # Schedule the event handler to monitor the folder
    observer.schedule(event_handler, pathway.src_path, recursive=True)

    # Start the observer
    observer.start()

def stop_monitoring():
    global observer
    status_label.config(text="Monitoring process stopped.")
    observer.stop()
    observer.join()

def start_monitoring():
    global monitor_thread
    status_label.config(text="Monitoring process started.")
    monitor_thread = threading.Thread(target=monitor_folder)
    monitor_thread.start()

root = tk.Tk()
root.title("Automagic Eight.EXE")  # Set the title of the window
root.geometry("300x100")  # Set the size of the window
root.configure(bg='black')  # Set the background color of the window

status_label = tk.Label(root, text="Monitoring process not started.", bg='black', fg='white')
status_label.pack()

start_button = tk.Button(root, text="Start", command=start_monitoring, bg='green', fg='white', activebackground='darkgreen')
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_monitoring, bg='red', fg='white', activebackground='darkred')
stop_button.pack()

root.mainloop()