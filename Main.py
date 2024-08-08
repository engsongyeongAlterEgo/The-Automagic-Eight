import tkinter as tk
from tkinter import ttk, messagebox
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work_item_tracking import JsonPatchOperation
from azure.devops.v7_0.work_item_tracking.models import Wiql
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import webbrowser
from forceclose import FileModifiedHandler
from pathway import src_path, dst_path, close_path
import psutil
import os
import threading
import time
import shutil
from datetime import datetime
import subprocess
from FinalSolution import connection, getBug, open_work_item_in_browser
from FinalSolution import organization_url
from storage import readData, writeData
from hourEntry import automate_hour_entry
import json

# pip install tk
# pip install azure-devops
# pip install beautifulsoup4
# pip install selenium



import watchdog.events
import watchdog.observers

userState = readData()

winWidth = 400
winHeight = 350

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
tabControl.add(tab3, text='Hour Entry')
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
          text="Hour Entry",
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
    
    if(custom_dst_path != userState["dst_path"] or custom_src_path != "src_path"):
        print("Custom paths modified.")
        writeData(['', '', '', custom_src_path, custom_dst_path, ''])
    
    # MODIFIED TO TXT FILE    
    # if dst_path != custom_dst_path or src_path != custom_src_path:
    #     dst_path = custom_dst_path
    #     src_path = custom_src_path
    #     f = open("pathway.py", "w")
    #     f.write(f"src_path = \"{src_path}\"\ndst_path = \"{dst_path}\"\nexe_path = \"{dst_path}\"\\E6Shell.exe\nclose_path = \"{close_path}\"")
    #     f.close()

    #     print("Pathway.py has been updated.")

    #     f = open("pathway.py", "r")
    #     print(f.read())
    #     f.close()

row = 0
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
src_path_entry.insert(0, "")
row += 1

dst_path_label = tk.Label(tab1, text="Destination Path:", fg='black', width=winWidth // 25)
dst_path_label.grid(row=row, column=0, sticky="WE")
dst_path_entry = tk.Entry(tab1)
dst_path_entry.grid(row=row, column=1, columnspan=2, sticky="WE")
dst_path_entry.insert(0, "")
row += 1

set_button = tk.Button(tab1, text="Apply", command=save_all, bg='blue', fg='white', activebackground='darkblue')
set_button.grid(row=row + 2, column=0, columnspan=3)
row += 1


# ==========================  TAB 2 ==========================

# Azure DevOps organization URL and personal access token (PAT)
project_name = 'Exact-Globe-Plus'
work_item_type = 'Task'

title = ""
created_work_item_coding = ""
userName = ""
bug_work_item_id = ""

def create_work_item():
    if(entry_token.get() == ""):
        messagebox.showerror('Token',"Token not found.")
        return
    
    personal_access_token = entry_token.get()
    credentials = BasicAuthentication('', personal_access_token) if personal_access_token != '' else None
    connection = Connection(base_url=organization_url, creds=credentials) if credentials else None
    wit_client = connection.clients.get_work_item_tracking_client()
    writeData(['', '', entry_token.get(), '', '', ''])
    print("Organization URL: ", organization_url)
    bug_id.set(bug_work_item_id)                    
    # Define fields for the new work items
    new_work_item_coding = [
        JsonPatchOperation(
            op="add",
            path="/fields/System.Title",
            value= code_title_entry.get()
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.AssignedTo",
            value= user_name.get()
        ),
        JsonPatchOperation(
            op="add",
            path="/relations/-",
            value={
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{organization_url}/_apis/wit/workItems/{bug_item_id.get()}"
            }
        ),
        # Add more fields as needed
    ]
                        
    new_work_item_testing = [
        JsonPatchOperation(
            op="add",
            path="/fields/System.Title",
            value= test_title_entry.get()
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.AssignedTo",
            value= " "
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/Microsoft.VSTS.Common.Activity",
            value="Testing"
        ),
        JsonPatchOperation(
            op="add",
            path="/relations/-",
            value={
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{organization_url}/_apis/wit/workItems/{bug_item_id.get()}"
            }
        ),
    ]
    
    print(new_work_item_coding[2].value.get('url'))
                        
    # Uncomment when you want to create task:

    # Create the work items
    try:
        created_work_item_coding = wit_client.create_work_item(
            document=new_work_item_coding,
            project=project_name,
            type=work_item_type
        )
        print(f"Created Coding work item with ID: {created_work_item_coding.id}")
        
        created_work_item_testing = wit_client.create_work_item(
            document=new_work_item_testing,
            project=project_name,
            type=work_item_type
        )
        print(f"Created Testing work item with ID: {created_work_item_testing.id}")
        
                #def update_work_item(wit_client, work_item_id, project_name):
        update_patch_document = [
            JsonPatchOperation(
                op="replace",  # Use "replace" to update an existing field
                path="/fields/System.State",
                value="Done"
            ),
        ]
        
        try:
            updated_work_item = wit_client.update_work_item(
                document=update_patch_document,
                id=created_work_item_coding.id,
                project=project_name
            )
            print(f"Updated work item with ID: {updated_work_item.id}")
        except Exception as e:
            print(f"Failed to update work item 1: {str(e)}")
            messagebox.showerror("update_work_item", "Error on updating work item 1.")
                                
    except Exception as e:
        print(f"Failed to create work items: {str(e)}")
        messagebox.showerror("create_work_item", "Error on creating work items.")
                    
    # Create the work items
        
    open_work_item_in_browser(bug_item_id.get(), organization_url, project_name)
                        
    # Example usage
    #update_work_item(wit_client, created_work_item_coding.id, project_name)

def on_submit():
    # url = entry_br_id.get()
    br_id = entry_br_id.get()
    # if url == "":
    #     messagebox.showerror("on_submit", "URL not found.")
    #     return
    
    if(entry_token.get() == ""):
        messagebox.showerror("on_submit","Token not found.")
        return
    writeData(['', '', entry_token.get(), '', '', ''])
    
    try:
        bug_work_item = getBug(br_id)
        bug_item_id.set(str(bug_work_item[0]))
        user_name.set(str(bug_work_item[1]))
        code_title_entry.insert(0, "[CODE] " + bug_work_item[2])
        test_title_entry.insert(0, "[TEST] " + bug_work_item[2])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messagebox.showerror("on_submit", "Error on Fetching DevOps BUG ITEM.")

    # Close the WebDriver
    # driver.quit()


tab2.rowconfigure(0, weight=0)
tab2.columnconfigure(0, weight=0)

row = 0
label_token = tk.Label(tab2, text="Enter Token:", fg="black")
label_token.grid(row=row, column=0)
entry_token = tk.Entry(tab2, width=30, show="*")
entry_token.grid(row=row, column=1)
entry_token.insert(0, "")
row += 1

# # Create labels and entry fields with red color
# label_br_id = tk.Label(tab2, text="Enter URL:", fg="black")
# label_br_id.grid(row=row, column=0)
# entry_br_id = tk.Entry(tab2, width=30)
# entry_br_id.grid(row=row, column=1)
# row += 1

# Create labels and entry fields with red color
label_br_id = tk.Label(tab2, text="Enter BR ID:", fg="black")
label_br_id.grid(row=row, column=0)
entry_br_id = tk.Entry(tab2, width=30)
entry_br_id.grid(row=row, column=1)
row += 1

# Button to submit URL
btn_submit = tk.Button(tab2, text="Submit", command=on_submit, bg="black", fg="white")
btn_submit.grid(row=row, column=0, columnspan=2, pady=10)
row += 1


# Label and text variable for BR ID
# label_br_id = tk.Label(tab2, text="BR ID:", fg="black")
# label_br_id.grid(row=row, column=0, pady=5)
# br_id = tk.StringVar()
# br_id.set("")
# label_br_id_value = tk.Label(tab2, textvariable=br_id, fg="black")
# label_br_id_value.grid(row=row, column=1)
# row += 1

# Label and text variable for BR ID
label_bug_item_id = tk.Label(tab2, text="BUG ITEM ID:", fg="black")
label_bug_item_id.grid(row=row, column=0, pady=5)
bug_item_id = tk.StringVar()
bug_item_id.set("")
label_bug_item_id_value = tk.Label(tab2, textvariable=bug_item_id, fg="black")
label_bug_item_id_value.grid(row=row, column=1)
row += 1

# Label and text variable for BR ID
label_user_name = tk.Label(tab2, text="USER NAME:", fg="black")
label_user_name.grid(row=row, column=0, pady=5)
user_name = tk.StringVar()
user_name.set("")
label_user_name_value = tk.Label(tab2, textvariable=user_name, fg="black")
label_user_name_value.grid(row=row, column=1)
row += 1

code_title = tk.Label(tab2, text="Code Title:", fg="black")
code_title.grid(row=row, column=0)
code_title_entry = tk.Entry(tab2, width=30)
code_title_entry.grid(row=row, column=1)
row += 1

test_title = tk.Label(tab2, text="Test Title:", fg="black")
test_title.grid(row=row, column=0)
test_title_entry = tk.Entry(tab2, width=30)
test_title_entry.grid(row=row, column=1)
row += 1

# Label and text variable for Bug ID
label_bug_id = tk.Label(tab2, text="Bug ID:", fg="black")
label_bug_id.grid(row=row, column=0, pady=5)
bug_id = tk.StringVar()
bug_id.set("")
label_bug_id_value = tk.Label(tab2, textvariable=bug_id, fg="black")
label_bug_id_value.grid(row=row, column=1)
row += 1

# Button to open work item in browser
btn_open = tk.Button(tab2, text="Create Task", command=lambda: create_work_item(), bg="black", fg="white")
btn_open.grid(row=row, column=0, columnspan=2, pady=10)
row += 1

# # Button to open work item in browser
# btn_open = tk.Button(tab2, text="Open Work Item", command=lambda: open_work_item_in_browser(bug_id.get(), organization_url, project_name), bg="black", fg="white")
# btn_open.grid(row=row, column=0, columnspan=2, pady=10)

# ==========================  TAB 3 ==========================

tab3.rowconfigure(0, weight=0)
tab3.columnconfigure(0, weight=0)

# Create labels and entry fields for User ID and Password
# label_user_id = tk.Label(tab3, text="User ID:", fg="black")
# label_user_id.grid(row=0, column=0, sticky="WE")
# entry_user_id = tk.Entry(tab3, show="")
# entry_user_id.grid(row=0, column=1)

# label_password = tk.Label(tab3, text="Password:", fg="black")
# label_password.grid(row=1, column=0, sticky="WE")
# entry_password = tk.Entry(tab3, show="*")
# entry_password.grid(row=1, column=1)

label_user_id = tk.Label(tab3, text="User ID :", fg='black', width=winWidth // 25)
label_user_id.grid(row=row, column=0,  sticky="WE")
entry_user_id = tk.Entry(tab3)
entry_user_id.grid(row=row, column=1, columnspan=2, sticky="WE")
entry_user_id.insert(0, "")
row += 1

label_password = tk.Label(tab3, text="Password :", fg='black', width=winWidth // 25)
label_password.grid(row=row, column=0, sticky="WE")
entry_password = tk.Entry(tab3, show="*")
entry_password.grid(row=row, column=1, columnspan=2, sticky="WE")
entry_password.insert(0, "")
row += 1

label_pro_code = tk.Label(tab3, text="Project Code :", fg='black', width=winWidth // 25)
label_pro_code.grid(row=row, column=0,  sticky="WE")
entry_pro_code = tk.Entry(tab3)
entry_pro_code.grid(row=row, column=1, columnspan=2, sticky="WE")
row += 1

label_activity = tk.Label(tab3, text="Activity :", fg='black', width=winWidth // 25)
label_activity.grid(row=row, column=0,  sticky="WE")
entry_activity = tk.Entry(tab3)
entry_activity.grid(row=row, column=1, columnspan=2, sticky="WE")
row += 1

separator_label = tk.Label(tab3, text="\n")
separator_label.grid(row=row, column=0,  columnspan=3)
row += 1

def trigger_hour_entry():
    user_id = entry_user_id.get()
    password = entry_password.get()
    pro_code = entry_pro_code.get()
    activity = entry_activity.get()
    automate_hour_entry(user_id, password, pro_code, activity)

btn_trigger_hour_entry = tk.Button(tab3, text="Start", command=trigger_hour_entry, bg="green", fg="black")
btn_trigger_hour_entry.grid(row=row, column=0, columnspan=3, padx=10, sticky="WE")

def init():
    userState = readData()
    entry_user_id.insert(0, userState['userName'])
    entry_password.insert(0, userState['userPassword'])
    entry_token.insert(0, userState['userToken'])
    src_path_entry.insert(0, userState['src_path'])
    dst_path_entry.insert(0, userState['dst_path'])
    
init()

root.mainloop()



