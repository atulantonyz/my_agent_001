import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_to_file
from functions.run_python import schema_run_python_file


def main():
    load_dotenv()
    if len(sys.argv) ==1:
        print("No prompt provided")
        sys.exit(1)
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    messages = [
            types.Content(role = "user", parts = [types.Part(text=prompt)]),
    ]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
""" 
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_to_file,
        schema_run_python_file,
    ]
    )
    res = client.models.generate_content(model="gemini-2.0-flash-001",contents= messages,\
                                         config=types.GenerateContentConfig(tools= [available_functions], system_instruction=system_prompt)) 
    if verbose:
        print("User prompt:",prompt)
        print("Prompt tokens:",res.usage_metadata.prompt_token_count)
        print("Response tokens:",res.usage_metadata.candidates_token_count)
    if res.function_calls:
        for fc in res.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
    print(res.text)
if __name__ == "__main__":
    main()
