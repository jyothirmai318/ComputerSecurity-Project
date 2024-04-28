import os

# Create the quarantine and backup directories if they don't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
QUARANTINE_DIR = os.path.join(script_dir, 'quarantine')
BACKUP_REPO = os.path.join(script_dir, 'backup')

if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

if not os.path.exists(BACKUP_REPO):
    os.makedirs(BACKUP_REPO)

import re
import ctypes
import psutil
import shutil

# Pattern to detect potentially encrypted files
ENCRYPTED_FILE_PATTERN = r'[a-zA-Z0-9+/=]+'

def is_file_encrypted(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if re.match(ENCRYPTED_FILE_PATTERN, content):
                return True
    except UnicodeDecodeError:
        return True
    return False

def show_system_warning(message):
    ctypes.windll.user32.MessageBoxW(None, message, "Policy Violation Alert", 0x40 | 0x30)

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        print(f"Terminated process with PID {pid}")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found")

def quarantine_file(file_path):
    quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    shutil.move(file_path, quarantine_path)
    print(f"File moved to quarantine: {quarantine_path}")

def restore_backup(file_path):
    backup_path = os.path.join(BACKUP_REPO, os.path.basename(file_path))
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        print(f"Backup restored for {file_path}")
    else:
        print(f"No backup found for {file_path}")

def detect_and_mitigate_policy_violations(log_file):
    log_entries = []
    with open(log_file, 'r') as f:
        next(f)  # Skip the header row
        for line in f:
            log_entries.append(line.strip().split(','))

    for timestamp, event_type, file_path, pid, process_name in log_entries:
        if event_type == 'modified':
            if is_file_encrypted(file_path):
                alert_msg = f"Policy violation detected: File {file_path} appears to be encrypted at {timestamp}"
                show_system_warning(alert_msg)
                if pid != 'N/A':
                    terminate_process(int(pid))
                quarantine_file(file_path)
                restore_backup(file_path)

    # Quarantine the log file after processing all entries
    quarantine_file(log_file)

# load monitored data log
log_file = 'monitor_log.csv'
detect_and_mitigate_policy_violations(log_file)
