from functions.get_files_info import get_files_info

res1 = get_files_info("calculator", ".")
print("Result for current directory:")
print(res1)

res2 = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
print(res2)

res3 = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(res3)

res4 = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(res4)
