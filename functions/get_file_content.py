import os
from config import MAX_CHARS

def get_file_content(working_directory,file_path):
    full_path = os.path.join(working_directory,file_path)
    parent_path = os.path.abspath(working_directory)
    child_path = os.path.abspath(full_path)
    if os.path.commonpath([parent_path]) != os.path.commonpath([parent_path, child_path]):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(child_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(child_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return "Error: " + str(e)
    return file_content_string
