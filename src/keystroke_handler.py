import curses
import os

# package imports
from src.directory import get_files_in_directory

def handle_key_press(key, current_dir, files, selected):
    if key == curses.KEY_UP:
        selected = (selected - 1) % len(files)
    elif key == curses.KEY_DOWN:
        selected = (selected + 1) % len(files)
    elif key == curses.KEY_LEFT:
        if current_dir != "/":
            current_dir = os.path.dirname(current_dir)
            files = get_files_in_directory(current_dir)
            selected = 0
    elif key == curses.KEY_RIGHT:
        selected_path = os.path.join(current_dir, files[selected])
        if os.path.isdir(selected_path):
            current_dir = selected_path
            files = get_files_in_directory(current_dir)
            selected = 0
    elif key == 10:
        selected_path = os.path.join(current_dir, files[selected])
        if os.path.isdir(selected_path):
            current_dir = selected_path
            files = get_files_in_directory(current_dir)
            selected = 0
        else:
            return selected_path, current_dir, files, selected
    elif key in [ord('q'), 27, 24]:
        return None, current_dir, files, selected
    return None, current_dir, files, selected
