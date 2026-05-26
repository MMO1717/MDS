"要创建一个generator，有很多种方法。第一种方法很简单，只要把一个列表生成式的[]改成()，就创建了一个generator："
g=(x*x for x in range(1,11))
print(next(g))
print(next(g))
"generator保存的是算法，每次调用next(g)，就计算出g的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。"

g=(x*x for x in range(1,11))
for i in g:
    print(i)

def fib_yield(max):
    a, b = 0, 1
    for _ in range(max):
        yield b        # 生成一个数列值
        a, b = b, a + b
    return 'done'

print("\nfib_yield:")
g = fib_yield(10)
for num in g:
    print(num)