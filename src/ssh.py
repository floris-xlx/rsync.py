
def get_remote_user(config):
    if "remote_user" in config:
        use_last = input(f"Use last host ({config['remote_user']})? (Y/n): "
                         ).strip().lower()
        if use_last == "y" or use_last == "":
            return config["remote_user"]
    return input(
        "Enter the remote server user@host (e.g., user@example.com): ")


def get_remote_path():
    return input(
        "Enter the remote destination path (e.g., /home/user/destination/): ")


def get_ssh_port():
    return input("Enter the SSH port (default: 22): ") or "22"
