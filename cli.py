import os
import curses
import subprocess
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "rsync.json")

from src.directory import get_files_in_directory
from src.keystroke_handler import handle_key_press
from src.ssh import get_remote_user, get_remote_path, get_ssh_port


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def initialize_curses():
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)


def display_files(stdscr, current_dir, files, selected, executable_extensions):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f"Current Directory: {current_dir}")

    for i, file in enumerate(files[:height - 3]):
        file_path = os.path.join(current_dir, file)
        file_ext = os.path.splitext(file)[-1].lower()

        if os.path.isdir(file_path):
            color_pair = curses.color_pair(2)
        elif file_ext in executable_extensions:
            color_pair = curses.color_pair(4)
        else:
            color_pair = curses.color_pair(3)

        if i == selected:
            stdscr.addstr(i + 2, 0, f"> {file}",
                          curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 2, 0, f"  {file}", color_pair)

    stdscr.addstr(
        height - 1, 0,
        "Select a file to transfer (Arrow keys to navigate, Left to go up, Right to go in, Enter to select, Ctrl+X/Esc/Q to quit):"
    )


def file_explorer(stdscr):
    initialize_curses()
    executable_extensions = {".exe", ".py", ".sh", ".rs", ".ts", ".js", ".pyt"}
    current_dir = os.getcwd()
    files = get_files_in_directory(current_dir)
    selected = 0

    while True:
        display_files(stdscr, current_dir, files, selected,
                      executable_extensions)
        key = stdscr.getch()
        selected_path, current_dir, files, selected = handle_key_press(
            key, current_dir, files, selected)
        if selected_path is not None:
            return selected_path


def start_rsync_transfer(selected_file, remote_user, remote_path, ssh_port):
    print("Starting Rsync transfer...")
    subprocess.run([
        "rsync", "-avzP", "-e", f"ssh -p {ssh_port}", selected_file,
        f"{remote_user}:{remote_path}"
    ])
    print("File transfer complete.")


def main():
    config = load_config()

    selected_file = curses.wrapper(file_explorer)
    if not selected_file:
        print("No file selected. Exiting.")
        return

    remote_user = get_remote_user(config)
    remote_path = get_remote_path()
    ssh_port = get_ssh_port()

    config["remote_user"] = remote_user
    save_config(config)

    start_rsync_transfer(selected_file, remote_user, remote_path, ssh_port)


if __name__ == "__main__":
    main()