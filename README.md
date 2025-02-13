# rsync_cli

## Overview

`rsync_cli` is a command-line interface (CLI) tool designed to facilitate file transfers using the `rsync` protocol on Unix-based systems. This tool provides a user-friendly interface for selecting files and directories to transfer, making it easier to manage and execute file synchronization tasks.

## Features

- **Interactive File Explorer**: Navigate through directories and select files using a curses-based interface. For example, use the arrow keys to move through files and directories, and press Enter to select a file for transfer.
- **File Metadata Display**: View file size and type information before initiating a transfer. For instance, when you select a file, its size and MIME type are displayed at the bottom of the interface.
- **Configuration Management**: Save and reuse remote server configurations for convenience. For example, the tool remembers the last used remote server details, allowing you to quickly reconnect without re-entering information.
- **Secure Transfers**: Utilize SSH for secure file transfers with customizable port settings. You can specify a different SSH port if your server does not use the default port 22.
- **Support for Executable Files**: Highlight and easily identify executable files within directories. Executable files are displayed in a distinct color, making them stand out in the file explorer.

## Installation

To install `rsync_cli`, clone the repository and ensure you have Python and `rsync` installed on your system. For example, run the following commands:
