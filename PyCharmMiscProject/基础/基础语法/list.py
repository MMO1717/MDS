# 列表（list）基础操作示例
# 创建一个包含整数元素的列表
people = [1, 3, 4, 5]
print(people)  # 输出整个列表

# 获取列表长度
print(len(people))  # 输出列表的元素个数

# 访问列表的第一个元素（索引从0开始）
print(people[0])

# 访问列表的最后一个元素（负索引从-1开始）
print(people[-1])

# 在索引1的位置插入元素2，原位置及之后的元素依次后移
people.insert(1, 2)
print(people)

# 在列表末尾追加元素6
people.append(6)
print(people)

# 弹出并移除列表的最后一个元素
people.pop()
print(people)

# 修改指定位置的元素值
people[4] = 100
print(people)

# 嵌套列表：列表中包含另一个列表
all_list = [1, people]
print(all_list)

# ========== 额外功能演示 ==========
# 1. 使用 remove() 删除指定元素（只删除第一个匹配项）
people.remove(3)  # 删除值为3的元素
print("After remove(3):", people)

# 2. 使用 sort() 对列表进行升序排序
people.sort()
print("After sort():", people)

# 3. 使用 reverse() 反转列表顺序
people.reverse()
print("After reverse():", people)

# 4. 使用 count() 和 index() 查找元素
print("Count of 2:", people.count(2))   # 统计值为2的元素出现次数
if 2 in people:
    print("Index of 2:", people.index(2))  # 查找值为2的第一个索引位置
else:
    print("2 not found in people")

# ========== tuple 示例 ==========
# tuple 是不可变序列，一旦创建后元素不能被修改

# 创建空元组
empty_tuple = ()
print(empty_tuple, type(empty_tuple))

# 只有一个元素时，必须加逗号，否则不是tuple
not_a_tuple = (1)
print(not_a_tuple, type(not_a_tuple))  # 实际为int类型

# 正确的一元tuple写法
single_tuple = (3,)
print(single_tuple, type(single_tuple))

# 多元素tuple
multi_tuple = (4, 5, 6)
print(multi_tuple, type(multi_tuple))

# 嵌套tuple的访问示例
nested_tuple = (1, (10, 20, 30), 3)
print("nested_tuple[1][2]:", nested_tuple[1][2])  # 访问嵌套tuple中的元素

# 练习：二维列表的索引提取
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Bob']
]
print(L[0][0])  # Apple
print(L[1][1])  # Python
print(L[2][2])  # Bob

# tuple 与可变元素的特殊情况
# tuple本身不可变，但如果包含可变对象（如list），可变对象的内容可以变
t = ('a', 'b', ['A', 'B'])
print("Before:", t)
t[2][0] = 'X'  # 修改了tuple中list的内容
t[2][1] = 'Y'
print("After :", t)
# 注意：tuple的结构（元素数量和引用）不能变，但可变元素的内容可变