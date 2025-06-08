print("Hello Python World!")

message = "Hello Python World!"
print(message)

message = "Hello Python Crash Course world!"
print(message)

# 字符串 “”签到‘’的用法（反之亦然）
message = 'I told my friend, "python is my favorite language"'
print(message)

# 首字母大写
name = "aba lovelace"
print(name.title())

name = "Aba Lovelace"
# 全大写
print(name.upper())

# 全小写
print(name.lower())

first_name = "aba"
last_name = "lovelace"

# 字符串中使用变量
full_name = f"{first_name} {last_name}"
print(full_name)
print (f"Hello,{full_name.title()}")

print("Python")
# 制表符
print("\tPython")

# 回车符
print("Language:\nPython\nC\nJavaScript")
print("Language:\n\tPython\n\tC\n\tJavaScript")

favorite_language = "Python "
print(favorite_language)

# 删除右端空格
favorite_language = favorite_language.rstrip()
print(favorite_language)

favorite_language = " Python "
# 删除右端空格
print(favorite_language.rstrip())
# 删除左端空格
print(favorite_language.lstrip())
# 删除两端空格
print(favorite_language.strip())

nostarch_url = "https://www.google.com"
# 用于移除字符串开头的特定前缀
nostarch_url = nostarch_url.removeprefix('https://')
print(nostarch_url)

file_name = "python_notes.txt"
# 用于移除字符串结尾的特定后缀
print(file_name.removesuffix('.txt'))