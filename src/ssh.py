
def get_remote_user(config):
    if "remote_user" in config:
        use_last = input(f"Use last host ({config['remote_user']})? (Y/n): ").strip().lower()
        if use_last == "y" or use_last == "":
            return config["remote_user"]
    
    while True:
        remote_user = input("Enter the remote server user@host (e.g., user@example.com): ")
        if "@" in remote_user:
            return remote_user
        else:
            print("Invalid format. Please enter in the format USER@HOST.")


def get_remote_path(config):
    if "remote_user" in config:
        user = config["remote_user"].split("@")[0]
        default_path = f"/home/{user}/files"
        use_default = input(f"Use default path ({default_path})? (Y/n): ").strip().lower()
        if use_default == "y" or use_default == "":
            config["remote_path"] = default_path
            return default_path
    
    remote_path = input("Enter the remote destination path (e.g., /home/user/destination/): ")
    config["remote_path"] = remote_path
    return remote_path


def get_ssh_port(config):
    ssh_port = input("Enter the SSH port (default: 22): ") or "22"
    config["ssh_port"] = ssh_port
    return ssh_port
