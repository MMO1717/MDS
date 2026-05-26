d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

for value in d.values():
    print(value)

for k,v in d.items():
    print(k, v)

for x in 'Kevin':
    print(x)

def findMinAndMax(L):
    if not L:  # L是None 或者 空列表时，返回 (None, None)
        return (None, None)
    min_val = L[0]
    max_val = L[0]
    for x in L:
        if x < min_val:
            min_val = x
        elif x > max_val:
            max_val = x
    return (min_val, max_val)

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
