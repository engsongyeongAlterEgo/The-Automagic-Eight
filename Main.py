import tkinter as tk
from tkinter import ttk
from forceclose import FileModifiedHandler
from pathway import src_path, dst_path, close_path
import psutil
import os
import threading
import time
import shutil
from datetime import datetime
import subprocess

import watchdog.events
import watchdog.observers

row = 0
winWidth = 400
winHeight = 300

root = tk.Tk()
root.title("Automagic Eight.EXE")  # Set the title of the window
root.geometry(f"{winWidth}x{winHeight}")  # Set the size of the window
root.configure(bg='white')  # Set the background color of the window

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)


tabControl.add(tab1, text='Target Sync')
tabControl.add(tab2, text='Task Create')
tabControl.add(tab3, text='Test Logger')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1,
          text="Target Sync",
          foreground='black').grid(column=0,
                                   row=0,
                                   padx=30,
                                   pady=30)
ttk.Label(tab2,
          text="Task Create",
          foreground='black').grid(column=0,
                                   row=0,
                                   padx=30,
                                   pady=30)

ttk.Label(tab3,
          text="Test Logger",
          foreground='black').grid(column=0,
                                   row=0,
                                   padx=30,
                                   pady=30)
          
          
# ==========================  TAB 1 ==========================

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
    
def kill_ExactGlobe():
    # Get the list of running processes
    running_processes = psutil.process_iter(['name'])

    # Iterate over the running processes
    for process in running_processes:
        # Check if the process name contains "Exact"
        if "Exact" in process.info['name']:
            # Kill the process
            print(f'Killing process: {process.info["name"]}')
            process.kill()
    subprocess.call(['taskkill', '/F', '/IM', close_path])   
            

def stop_monitoring():
    global observer
    print("Monitoring process stopped.")
    status_label.config(text="Monitoring process stopped.")
    observer.stop()
    observer.join()

def start_monitoring():
    global monitor_thread
    print("Monitoring process started.")
    status_label.config(text="Monitoring process started.")
    monitor_thread = threading.Thread(target=monitor_folder)
    monitor_thread.start()

def save_all():
    global src_path, dst_path
    custom_src_path = src_path_entry.get()
    custom_dst_path = dst_path_entry.get()

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

tab1.rowconfigure(0, weight=1)
tab1.columnconfigure(0, weight=1)

status_label = tk.Label(tab1, text="Monitoring process not started.", fg='black')
status_label.grid(row=row, column=0, columnspan=3, sticky="WE")
row += 1

start_button = tk.Button(tab1, text="Start", command=start_monitoring, bg='green', fg='white', activebackground='darkgreen')
start_button.grid(row=row, column=0, columnspan=3, sticky="WE", padx=50, pady=1)
row += 1

stop_button = tk.Button(tab1, text="Stop", command=stop_monitoring, bg='red', fg='white', activebackground='darkred')
stop_button.grid(row=row, column=0, columnspan=3, sticky="WE", padx=50, pady=1)
row += 1

stop_button = tk.Button(tab1, text="Kill Exact", command=kill_ExactGlobe, bg='red', fg='white', activebackground='darkred')
stop_button.grid(row=row, column=0, columnspan=3, sticky="WE", padx=50, pady=1)
row += 1

separator_label = tk.Label(tab1, text="\n")
separator_label.grid(row=row, column=0,  columnspan=3)
row += 1

src_path_label = tk.Label(tab1, text="Source Path:", fg='black', width=winWidth // 25)
src_path_label.grid(row=row, column=0,  sticky="WE")
src_path_entry = tk.Entry(tab1)
src_path_entry.grid(row=row, column=1, columnspan=2, sticky="WE")
src_path_entry.insert(0, src_path)
row += 1

dst_path_label = tk.Label(tab1, text="Destination Path:", fg='black', width=winWidth // 25)
dst_path_label.grid(row=row, column=0, sticky="WE")
dst_path_entry = tk.Entry(tab1)
dst_path_entry.grid(row=row, column=1, columnspan=2, sticky="WE")
dst_path_entry.insert(0, dst_path)
row += 1

set_button = tk.Button(tab1, text="Apply", command=save_all, bg='blue', fg='white', activebackground='darkblue')
set_button.grid(row=row + 2, column=0, columnspan=3)
row += 1


# ==========================  TAB 2 ==========================

tab2.rowconfigure(0, weight=1)
tab2.columnconfigure(0, weight=1)

# ==========================  TAB 3 ==========================




root.mainloop()
