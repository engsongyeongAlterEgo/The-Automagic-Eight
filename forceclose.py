import os
import threading
import time
import shutil
import pathway
from datetime import datetime
import subprocess
import watchdog.events
import watchdog.observers
import tkinter as tk
from threading import Thread

stop_flag = False
observer = None  # Declare observer as a global variable

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
    global observer  # Access the global observer
    # Create a watchdog observer
    observer = watchdog.observers.Observer()

    # Create a file modified event handler
    event_handler = FileModifiedHandler(pathway.close_path)

    # Schedule the event handler to monitor the folder
    observer.schedule(event_handler, pathway.src_path, recursive=True)

    # Start the observer
    observer.start()

    try:
        while not stop_flag:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Start monitoring the folder
def start_process():
    status_label.config(text="Monitoring process started.")
    thread = Thread(target=monitor_folder)
    thread.start()

def stop_process():
    status_label.config(text="Monitoring process stopped.")
    global stop_flag
    stop_flag = True
    global observer  # Access the global observer
    if observer is not None:
        observer.stop()
        observer.join()
        observer = None  # Reset the observer

root = tk.Tk()
root.geometry("300x100")
root.title("Automagic Eight.EXE")
status_label = tk.Label(root, text="Monitoring process not started.")
status_label.pack()
start_button = tk.Button(root, text="Start", command=start_process)
start_button.pack()
stop_button = tk.Button(root, text="Stop", command=stop_process)
stop_button.pack()
root.mainloop()