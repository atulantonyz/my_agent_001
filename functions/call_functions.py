from google.genai import types
from functions.get_files_info import get_files_info,schema_get_files_info
from functions.get_file_content import get_file_content,schema_get_files_content
from functions.write_file import write_file,schema_write_to_file
from functions.run_python import run_python_file,schema_run_python_file
from config import WORKING_DIR



def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    name_2_fn_map = {
        'get_file_content': get_file_content,
        'get_files_info': get_files_info,
        'write_file': write_file,
        'run_python_file': run_python_file
    }
    function_name = function_call_part.name
    function_args = function_call_part.args
    if function_name not in name_2_fn_map:
        return types.Content(role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_name,
                                    response={"error": f"Unknown function: {function_name}"},
                                )
                            ],
                    )
    args = dict(function_args)
    args["working_directory"] = WORKING_DIR
    function_result = name_2_fn_map[function_name](**args)
    return types.Content(role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_name,
                                response={"result": function_result},
                            )
                        ],
                )

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_to_file,
        schema_run_python_file,
    ]
    )
