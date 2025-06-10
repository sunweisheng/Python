color_list = ['红色', '绿色', '蓝色', '黄色', '品红色', '青色','red']
print(color_list)

print(color_list[0])
print(color_list[6].title())

# 从后往前读取元素下标可以用复数
print(color_list[-1])
print(color_list[-2])

message = f"我喜欢的颜色是{color_list[-1].title()}"
print(message)

# 修改
color_list[1] = "green"
print(color_list)

# 在末尾添加
color_list.append("黑色")
print(color_list)

list = []
list.append("1")
list.append("2")
list.append("3")
print(list)

# 在表中任意位置添加元素
color_list.insert(0,"紫色")
print(color_list)

# 删除元素
del color_list[0]
print(color_list)

# 从末尾删除并返回删除的内容
color = color_list.pop()
print(color)
print(color_list)

# 删除任意位置的元素并返回其内容
color = color_list.pop(0)
print(color)
print(color_list)

# 根据元素内容删除元素(该方法只删除第一个匹配到的元素如果还要其他相同的内容需要循环多次删除才行)
color_list.remove("品红色")
print(color_list)

# 永久性排序(按字母顺序排序)
color_list.sort()
print(color_list)

# 反方向排序
color_list.sort(reverse=True)
print(color_list)

# 临时排序(按字母顺序排序)
print(sorted(color_list))
# 临时反向排序(按字母顺序排序)
print(sorted(color_list, reverse=True))

# 永久性的反向排序（按元素位置）
color_list.reverse()
print(color_list)
color_list.reverse()
print(color_list)

# 确定列表的长度
print(len(color_list))