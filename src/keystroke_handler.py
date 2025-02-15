from blessed import Terminal
import os

# package imports
from src.directory import get_files_in_directory

term = Terminal()

def handle_key_press(key, current_dir, files, selected):
    if key.name == "KEY_UP":
        selected = (selected - 1) % len(files)
    elif key.name == "KEY_DOWN":
        selected = (selected + 1) % len(files)
    elif key.name == "KEY_LEFT":
        if current_dir != "/":
            current_dir = os.path.dirname(current_dir)
            files = get_files_in_directory(current_dir)
            selected = 0
    elif key.name == "KEY_RIGHT":
        selected_path = os.path.join(current_dir, files[selected])
        if os.path.isdir(selected_path):
            current_dir = selected_path
            files = get_files_in_directory(current_dir)
            selected = 0
    elif key in ["\n", "\r", term.KEY_ENTER]:  # Updated to handle enter key
        selected_path = os.path.join(current_dir, files[selected])
        if os.path.isdir(selected_path):
            current_dir = selected_path
            files = get_files_in_directory(current_dir)
            selected = 0
        else:
            return selected_path, current_dir, files, selected
    elif key in [term.KEY_ESCAPE, term.KEY_CTRL_X, 'q']:
        return None, current_dir, files, selected
    else:
        # Block the input if it's not a recognized key
        pass
    return None, current_dir, files, selected
