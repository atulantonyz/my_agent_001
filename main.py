import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_functions import call_function,available_functions
from config import MAX_ITERS


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
    i = 0
    while True:
        if i == MAX_ITERS:
            print("Maximum number of iterations reached")
            break
        i+=1
        res = client.models.generate_content(model="gemini-2.0-flash-001",contents= messages,\
                                             config=types.GenerateContentConfig(tools= [available_functions], system_instruction=system_prompt)) 
        if res.candidates:
            for candidate in res.candidates:
                messages.append(candidate.content)
        if verbose:
            print("User prompt:",prompt)
            print("Prompt tokens:",res.usage_metadata.prompt_token_count)
            print("Response tokens:",res.usage_metadata.candidates_token_count)
        if res.function_calls:
            for fc in res.function_calls:
                #print(f"Calling function: {fc.name}({fc.args})")
                function_call_result = call_function(fc,verbose)
                try:
                    response = function_call_result.parts[0].function_response.response
                    if verbose:
                        print(f"-> {response}")
                    messages.append(function_call_result)
                except Exception as e:
                    raise Exception(f"Error: calling function {fc.name}: {e}")
        else:
            print(res.text)
            break
if __name__ == "__main__":
    main()
