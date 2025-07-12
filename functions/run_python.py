import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    parent_path = os.path.abspath(working_directory)
    child_path = os.path.abspath(full_path)
    if os.path.commonpath([parent_path]) != os.path.commonpath([parent_path, child_path]):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(child_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path} is not a Python file.'
    try:
        res = subprocess.run(["python",child_path],capture_output=True,cwd= parent_path,timeout=30,text=True)
        output = []
        output.append(f"STDOUT: {res.stdout}")
        output.append(f"STDERR: {res.stderr}")
        if res.returncode !=0:
            output.append(f"Process exited with code {res.returncode}")
        return "\n".join(output) if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Use Python to run the code in the specified file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that contains the Python code to run",
            ),
        },
    ),
)
