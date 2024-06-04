import os
import time
import subprocess

def monitor_folder(folder_path, program_to_close):
    # Get the initial modification time of the folder
    initial_mod_time = os.path.getmtime(folder_path)

    while True:
        # Check if the folder has been modified
        current_mod_time = os.path.getmtime(folder_path)
        if current_mod_time > initial_mod_time:
            # Force close the program
            subprocess.call(['taskkill', '/F', '/IM', program_to_close])

            # Update the initial modification time
            initial_mod_time = current_mod_time

        # Wait for a certain interval before checking again
        time.sleep(1)

# Specify the folder path to monitor
folder_path = 'C:\\Users\\ENGS437957\\source\\repos\\Globe.NetApp\\binGlobe.Net'

# Specify the program name to force close
program_to_close = 'E6Shell.exe'

# Start monitoring the folder
monitor_folder(folder_path, program_to_close)