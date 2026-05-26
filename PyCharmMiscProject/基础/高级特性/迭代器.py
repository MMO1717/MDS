from collections.abc import Iterable

"判断是否能迭代"
print(isinstance([1,2,3], Iterable))  # True
print(isinstance(123, Iterable))      # False