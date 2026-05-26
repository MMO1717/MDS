import json


# 定义一个 Student 类
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


# 创建一个实例
s = Student('Alice', 21, 95)
print("原始 Student 实例:", s)

# --- 错误尝试：直接序列化实例 ---
try:
    json.dumps(s)
except TypeError as e:
    print("\n直接序列化失败，错误信息:", e)
    print("这是因为 JSON 不知道如何处理 Student 类型的对象。")


# --- 正确方法：提供一个转换函数 ---
# 这个函数告诉 json.dumps 如何将 Student 实例转换成一个字典
def student_to_dict(std):
    # std.__dict__ 是一个包含实例所有属性的字典
    # {'name': 'Alice', 'age': 21, 'score': 95}
    return std.__dict__


# 使用 default 参数指定转换函数
json_string_ok = json.dumps(s, default=student_to_dict)
print("\n使用转换函数后，序列化成功！")
print("序列化后的 JSON 字符串:", json_string_ok)

# --- 反序列化自定义对象 ---
# json.loads() 默认只会返回一个字典
reconstructed_dict = json.loads(json_string_ok)
print("\n反序列化后得到的是一个字典:", reconstructed_dict)


# 如果想把它变回 Student 实例，需要自己写一个转换函数
def dict_to_student(d):
    return Student(d['name'], d['age'], d['score'])


# 使用 object_hook 参数在反序列化时应用转换
reconstructed_student = json.loads(json_string_ok, object_hook=dict_to_student)
print("使用 object_hook 转换后，得到 Student 实例:", reconstructed_student)
print("对象类型:", type(reconstructed_student))
print("实例的 name 属性:", reconstructed_student.name)
