bool_a=True
bool_b=False
print(bool_a)
print(f"输出的内容是: {bool_a}")
print(10,"good",True,2.5)
print("Hello", end="")   # 不换行
print("World")
print("A", end="---")
print("B")
print("2025", "06", "26", sep="-")
#格式化输出
#1。 使用 % 格式符（类似 C 语言）
name = "Tom"
age = 20
print("Name: %s, Age: %d" % (name, age))
print("Name: {}, Age: {}".format("Alice", 25))
print("Name: {0}, Age: {1}".format("Bob", 30))
print("Pi: {:.2f}".format(3.14159))

name1="itcat"
name2="ieheima"
print(name1+"你好")
num=1
num2=2
print(num>num2)