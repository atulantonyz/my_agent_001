from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

res1 = get_file_content("calculator", "lorem.txt")
print(res1)
res2 = get_file_content("calculator", "main.py")
print(res2)
res3 = get_file_content("calculator", "pkg/calculator.py")
print(res3)
res4 = get_file_content("calculator", "/bin/cat") 
print(res4)



