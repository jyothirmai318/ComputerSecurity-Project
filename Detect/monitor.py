import psutil
import csv
import time
import os

# Function to check if a process is encrypting files
def is_encrypting(process, root_dir):
    try:
        for file in process.open_files():
            try:
                file_path = file.path
                if os.path.exists(file_path) and os.path.commonprefix([file_path, root_dir]) == root_dir:
                    with open(file_path, 'rb+') as f:
                        # Check if the process is writing to the file
                        if f.mode == 'rb+':
                            f.write(b'test')  # Simulate file modification
                            return True
            except (PermissionError, OSError):
                pass
    except psutil.AccessDenied:
        pass
    return False

# Function to log the monitored data to a CSV file
def log_data(data):
    with open('monitor_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Get the root directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Main monitoring loop
while True:
    # Get the list of running processes
    processes = psutil.process_iter(['pid', 'name'])
    for process in processes:
        if is_encrypting(process, script_dir):
            print(f"File encryption detected: {process.pid} - {process.name()}")
            log_data([time.strftime('%Y-%m-%d %H:%M:%S'), process.pid, process.name()])

    # 1s interval to the next iteration
    time.sleep(1)