import os
from blessed import Terminal
import subprocess
import json
import mimetypes

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "rsync.json")

from src.directory import get_files_in_directory
from src.keystroke_handler import handle_key_press
from src.ssh import get_remote_user, get_remote_path, get_ssh_port


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def initialize_terminal(term):
    print(term.enter_fullscreen)
    print(term.clear)


def format_size(size_bytes):
    if size_bytes >= 1024**3:
        size = size_bytes / 1024**3
        unit = "GB"
    elif size_bytes >= 1024**2:
        size = size_bytes / 1024**2
        unit = "MB"
    elif size_bytes >= 1024:
        size = size_bytes / 1024
        unit = "KB"
    else:
        size = size_bytes
        unit = "B"
    return f"{size:.2f} {unit}"


def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def display_files(term, current_dir, files, selected, executable_extensions):
    print(term.clear)
    width = term.width
    print(term.move(0, 0) + f"Current Directory: {current_dir}")

    # Calculate the start index for the visible window of files
    start_index = max(0, min(len(files) - (term.height - 5), selected - (term.height - 6) // 2))
    end_index = start_index + term.height - 5

    for i, file in enumerate(files[start_index:end_index]):
        file_path = os.path.join(current_dir, file)
        file_ext = os.path.splitext(file)[-1].lower()

        if os.path.isdir(file_path):
            color = term.yellow
        elif file_ext in executable_extensions:
            color = term.red
        else:
            color = term.blue

        if i + start_index == selected:
            print(term.move(i + 2, 0) + term.bold + term.magenta(f"> {file}"))
            # Display file metadata
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                print(term.move(term.height - 3, 0) + f"File: {file} | Size: {format_size(file_size)} | Type: {mime_type or 'Unknown'}")
        else:
            print(term.move(i + 2, 0) + color(f"  {file}"))

    print(term.move(term.height - 2, 0) + "Select a file to transfer (Arrow keys to navigate, Left to go up, Right to go in, Enter to select, Ctrl+X/Esc/Q to quit):")


def file_explorer(term):
    initialize_terminal(term)
    executable_extensions = {".exe", ".py", ".sh", ".rs", ".ts", ".js", ".pyt"}
    current_dir = os.getcwd()
    files = get_files_in_directory(current_dir)
    
    # Sort files by size
    files = sorted(files, key=lambda f: os.path.getsize(os.path.join(current_dir, f)) if os.path.isfile(os.path.join(current_dir, f)) else 0)
    
    selected = 0

    while True:
        display_files(term, current_dir, files, selected, executable_extensions)
        key = term.inkey()
        selected_path, current_dir, files, selected = handle_key_press(
            key, current_dir, files, selected)
        if selected_path is not None:
            return selected_path

def start_rsync_transfer(selected_file, remote_user, remote_path, ssh_port):
    import enlighten

    print("Starting Rsync transfer...")
    manager = enlighten.Manager()
    progress_bar = manager.counter(total=100, desc='Rsync Progress', unit='%', leave=False)

    # Run rsync and capture the output
    process = subprocess.Popen(
        [
            "rsync", "-avzP", "--compress-level=9", "--partial", "--inplace", "-e", f"ssh -p {ssh_port}", selected_file,
            f"{remote_user}:{remote_path}"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        if '%' in line:
            # Extract the percentage from the rsync output
            try:
                percent = int(line.split('%')[0].split()[-1])
                progress_bar.update(percent - progress_bar.count)
            except (ValueError, IndexError):
                pass

    process.wait()
    progress_bar.close()
    print("File transfer complete.")


def main():
    term = Terminal()
    try:
        print(term.blue("Loading configuration..."))
        config = load_config()
        print(term.green("Configuration loaded successfully."))

        print(term.blue("Starting file explorer..."))
        try:
            with term.fullscreen(), term.cbreak():
                selected_file = file_explorer(term)
            if not selected_file:
                print("No file selected. Exiting.")
                return
        except Exception as e:
            print(term.red(f"An error occurred during file selection: {e}"))
            return
        print(f"File selected: {selected_file}")

        print("Retrieving remote user information...")
        remote_user = get_remote_user(config)
        print(f"Remote user: {remote_user}")

        print("Retrieving remote path...")
        remote_path = get_remote_path(config)
        print(f"Remote path: {remote_path}")

        print("Retrieving SSH port...")
        ssh_port = get_ssh_port(config)
        print(f"SSH port: {ssh_port}")

        print("Updating configuration with remote user...")
        config["remote_user"] = remote_user
        save_config(config)
        print("Configuration updated and saved.")
        print(term.blue("Initiating file transfer..."))
        start_rsync_transfer(selected_file, remote_user, remote_path, ssh_port)
        print(term.green("File transfer initiated successfully."))
    except Exception as e:
        print(term.red(f"An error occurred: {e}"))


if __name__ == "__main__":
    main()