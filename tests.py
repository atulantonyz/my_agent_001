from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

res1 = run_python_file("calculator", "main.py")
print(res1)
res2 = run_python_file("calculator", "tests.py")
print(res2)
res3 = run_python_file("calculator", "../main.py")
print(res3)
res4 = run_python_file("calculator", "nonexistent.py")
print(res4)



