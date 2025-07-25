import os
from google.genai import types

def get_files_info(working_directory, directory = None):
    if directory:
        full_path = os.path.join(working_directory,directory)
    else:
        full_path = working_directory
    parent_path = os.path.abspath(working_directory)
    child_path = os.path.abspath(full_path)
    if os.path.commonpath([parent_path]) != os.path.commonpath([parent_path, child_path]):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(child_path):
        return f'Error: "{directory}" is not a directory'
    contents = []
    try:
        for file in os.listdir(child_path):
            is_directory = "True" if os.path.isdir(os.path.join(child_path,file)) else "False"
            contents.append(f"- {file}: file_size={os.path.getsize(os.path.join(child_path,file))} bytes, is_dir={is_directory}")
    except Exception as e:
        return "Error: " + str(e) 
    contents_str = "\n".join(contents)
    return contents_str

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



