titles = []
while True:
    title = input("输入资料标题：").strip()
    if title == "q":
        break
    if not title:
        print("标题不能为空")
        continue
    titles.append(title)
print(f"资料列表：{titles}")
print(f"资料总数:{len(titles)}")