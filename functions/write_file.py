import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory,file_path)
    parent_path = os.path.abspath(working_directory)
    child_path = os.path.abspath(full_path)
    if os.path.commonpath([parent_path]) != os.path.commonpath([parent_path, child_path]):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    dir_path = os.path.dirname(child_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path,exist_ok = True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(child_path) and os.path.isdir(child_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(child_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
