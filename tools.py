import os
import json

# Implementation Functions

def read_file(file_path: str) -> str:
    """
    Reads a file and returns its contents.

    :param file_path: Path to the file to read.
    :return: The content of the file.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"
 
def write_file(file_path: str, contents: str) -> str:
    """
    Writes a file with the given contents.

    :param file_path: Path to the file to write.
    :param contents: Contents to write to the file.
    :return: A success message or error string.
    """
    try:
        with open(file_path, "w") as f:
            f.write(contents)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"
 
def list_dir(directory_path: str) -> list[str] | str:
    """
    Lists the contents of a directory.

    :param directory_path: Path to the directory to list.
    :return: A list of filenames or error string.
    """
    try:
        full_path = os.path.expanduser(directory_path)
        return os.listdir(full_path)
    except Exception as e:
        return f"Error listing directory: {e}"
 
# Dictionary for easy access if needed
file_tools_map = {
    "read_file": read_file,
    "write_file": write_file,
    "list_dir": list_dir,
}
