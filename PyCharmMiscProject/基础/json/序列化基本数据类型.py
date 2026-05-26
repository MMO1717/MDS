import json

# --- 1. 准备一个对象 ---
# 注意：JSON 的 key 必须是字符串
d = {'name': 'Bob', 'age': 20, 'score': 88}

# --- 2. 使用 json.dumps() 将对象序列化为 JSON 字符串 ---
# .dumps() 的 's' 代表 string
json_string = json.dumps(d)
print("Python 字典:", d)
print("序列化后的 JSON 字符串:", json_string)

# --- 3. 使用 json.loads() 将 JSON 字符串反序列化为 Python 对象 ---
# .loads() 的 's' 代表 string
reconstructed_d = json.loads(json_string)
print("从 JSON 字符串反序列化后的 Python 对象:", reconstructed_d)
print("对象类型:", type(reconstructed_d))

# --- 4. 使用 json.dump() 和 json.load() 直接操作文件 ---
# 'w' 表示以文本写入模式打开，因为 JSON 是纯文本
try:
    with open('dump.json', 'w') as f:
        # json.dump() 直接将对象序列化为 JSON 格式并写入文件
        json.dump(d, f)
        print("\n已将对象序列化并存入 dump.json 文件。")
except IOError as e:
    print(f"文件操作失败: {e}")

try:
    with open('dump.json', 'r') as f:
        # json.load() 直接从文件中读取 JSON 数据并反序列化
        file_d = json.load(f)
        print("从 dump.json 文件中反序列化得到的对象:", file_d)
except FileNotFoundError:
    print("错误：找不到 dump.json 文件。")
except IOError as e:
    print(f"文件操作失败: {e}")
