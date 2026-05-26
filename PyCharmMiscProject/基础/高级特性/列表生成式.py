# ===== 列表生成式（List Comprehensions）笔记 =====
# 特点：
# Python 内置的高级语法，能让你用一行代码快速构造 list，语法简洁、表达清晰。
# 原理：把要生成的元素表达式放在前面，后面接上 for 循环（可加筛选条件）。

print(list(range(1,11)))


#  示例 1：生成 1 到 10 的平方
squares = [x * x for x in range(1, 11)]
print(squares)
# 结果: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

#  示例 2：筛选偶数再平方
even_squares = [x * x for x in range(1, 11) if x % 2 == 0]
print(even_squares)
# 结果: [4, 16, 36, 64, 100]

#  示例 3：嵌套循环，生成两个字符串集合的全排列
pairs = [m + n for m in 'ABC' for n in 'XYZ']
print(pairs)
# 结果: ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

#  示例 4：遍历当前目录下所有文件和文件夹
import os
files = [d for d in os.listdir('.')]
print(files)
# os.listdir('.') 会返回当前目录的所有名称列表

#  示例 5：同时遍历字典的 key 和 value
d = {'x': 'A', 'y': 'B', 'z': 'C'}
kv_pairs = [k + '=' + v for k, v in d.items()]
print(kv_pairs)
# 结果类似: ['x=A', 'y=B', 'z=C']

#  示例 6：将字符串列表统一转换为小写
L = ['Hello', 'World', 'IBM', 'Apple']
lower_list = [s.lower() for s in L]
print(lower_list)
# 结果: ['hello', 'world', 'ibm', 'apple']

# === 注意语法差异：if...else ===
#  列表推导中，for 后面的 if 是过滤条件，不能写 else，否则语法错误:
# [x for x in range(1, 11) if x % 2 == 0 else 0]  # SyntaxError

#  如果想在表达式中作条件判断，必须用 “表达式 if 条件 else 表达式” 放在 for 前面：
conditional = [x if x % 2 == 0 else -x for x in range(1, 11)]
print(conditional)
# 结果: [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

# === 应对不同类型数据的数据清洗示例 ===
L1 = ['Hello', 'World', 18, 'Apple', None]
#  想对字符串进行 .lower()，避免报错，可以先判断类型：
L2 = [s.lower() for s in L1 if isinstance(s, str)]
print(L2)
#  结果: ['hello', 'world', 'apple']


d = {"x": "A", "y": "B", "z": "C"}
print([k + "=" + v for k, v in d.items()])

L = ["Hello", "World", "IBM", "Apple"]
print([s.lower() for s in L])