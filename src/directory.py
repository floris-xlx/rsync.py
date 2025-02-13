import os


def get_files_in_directory(current_dir):
    return [".."] + sorted(os.listdir(current_dir))
