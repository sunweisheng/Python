from unicodedata import digit

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

lists = []
lists.append("1")
lists.append("2")
lists.append("3")
print(lists)

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

# 遍历整个列表
for color in color_list:
    print(color)

for color in color_list:
    print(f"color is:{color}")
print("color end.")

# 数值列表
for value in range(1,5):
    print(value)

numbers = list(range(1,6))
print(numbers)

numbers = list(range(2,11,2))
print(numbers)

squares = []
for value in range(1,11):
    square = value ** 2
    squares.append(square)
print(squares)

# 对数值列表统计
digits = [1,2,3,4,5,6,7,8,9,0]
print(min(digits))
print(max(digits))
print(sum(digits))

# 列表推导式
squares = [value ** 2 for value in range(1,11)]
print(squares)

# 切片
# 显示0，1，2三个元素
print(color_list[0:3])
print(color_list[1:4])
print(color_list[:2])
print(color_list[2:])
print(color_list[-2:])
for color in color_list[:3]:
    print(color)

# 复制列表
my_colors = color_list[:]
print(my_colors)

my_colors.append("橙色")
print(my_colors)
print(color_list)