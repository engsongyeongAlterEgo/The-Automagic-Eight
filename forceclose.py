import tkinter as tk
import os
import threading
import time
import shutil
from pathway import src_path, dst_path, exe_path, close_path
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
        subprocess.run([exe_path])
        self.timer_started = False

    def on_modified(self, event):
        # if datetime.now() - self.last_modified < timedelta(seconds=1):
        #     subprocess.call(['taskkill', '/F', '/IM', self.program_to_close])
        # else:
        #     self.last_modified = datetime.now()
        if event.event_type != 'modified':
            return
        if not self.timer_started :
            self.start_timer()

        subprocess.call(['taskkill', '/F', '/IM', self.program_to_close])   
        print(f'Event type: {event.event_type}  path : {event.src_path}')
        print(event.is_directory) # This attribute is also available
        if not event.is_directory:
            # Force close the program
            print(f'event type: {event.event_type}  path : {event.src_path}')
            # Get the file name from the event source path
            file_name = os.path.basename(event.src_path)
            print(f'File name: {file_name}')
            shutil.copyfile(event.src_path, dst_path + '\\' + file_name)

def monitor_folder():
    # Create a watchdog observer
    global observer
    observer = watchdog.observers.Observer()

    # Create a file modified event handler
    event_handler = FileModifiedHandler(close_path)

    # Schedule the event handler to monitor the folder
    observer.schedule(event_handler, src_path, recursive=True)

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

winHeight = 300
winWidth = 400

root = tk.Tk()
root.title("Automagic Eight.EXE")  # Set the title of the window
root.geometry(f"{winWidth}x{winHeight}")  # Set the size of the window
root.configure(bg='black')  # Set the background color of the window

row = 0

status_label = tk.Label(root, text="Monitoring process not started.", bg='black', fg='white')
status_label.grid(row=row, column=0, columnspan=3, sticky="WE")
row += 1

start_button = tk.Button(root, text="Start", command=start_monitoring, bg='green', fg='white', activebackground='darkgreen')
start_button.grid(row=row, column=0, columnspan=2, sticky="E")
row += 1

stop_button = tk.Button(root, text="Stop", command=stop_monitoring, bg='red', fg='white', activebackground='darkred')
stop_button.grid(row=row, column=0, columnspan=2, sticky="E")
row += 1

separator_label = tk.Label(root, text="\n", bg='black')
separator_label.grid(row=row, column=0,  columnspan=2)
row += 1

src_path_label = tk.Label(root, text="Source Path:", bg='black', fg='white', width= winWidth // 25)
src_path_label.grid(row=row, column=0, sticky="WE")
src_path_entry = tk.Entry(root, width= winWidth // 18)
src_path_entry.grid(row=row, column=1, columnspan=2,  sticky="WE")
src_path_entry.insert(0, src_path)
row += 1

dst_path_label = tk.Label(root, text="Destination Path:", bg='black', fg='white', width= winWidth // 25)
dst_path_label.grid(row=row, column=0, sticky="WE")
dst_path_entry = tk.Entry(root, width= winWidth // 18)
dst_path_entry.grid(row=row, column=1, columnspan=2, sticky="WE")
dst_path_entry.insert(0, dst_path)
row += 1

def save_all():
    global src_path, dst_path
    custom_src_path = src_path_entry.get()
    custom_dst_path = src_path_entry.get()
    
    
    if dst_path != custom_dst_path or src_path != custom_src_path:
        dst_path = custom_dst_path
        src_path = custom_src_path
        f = open("pathway.py", "w")
        f.write(f"src_path = {src_path}\ndst_path = {dst_path}\nexe_path = {dst_path}\\E6Shell.exe\nclose_path = {close_path}")
        f.close()
        
        print("Pathway.py has been updated.")
            
        f = open("pathway.py", "r")
        print(f.read())
        f.close()
        
set_button = tk.Button(root, text="Apply", command=save_all, bg='blue', fg='white', activebackground='darkblue')
set_button.grid(row=row + 2, column=1, columnspan=2)
row += 1


root.mainloop()