import pickle

# --- 1. 准备一个要序列化的对象 ---
# 它可以是任何 Python 对象，这里我们用一个字典作为例子
d = dict(name='Bob', age=20, score=88)

# --- 2. 使用 pickle.dump() 将对象序列化到文件 ---
# 'wb' 表示以二进制（binary）写入（write）模式打开文件
# pickle 产生的是二进制数据，所以必须用 'wb'
try:
    with open('dump.txt', 'wb') as f:
        # pickle.dump() 接受两个主要参数：
        # 1. 要序列化的对象 (d)
        # 2. 写入的目标文件对象 (f)
        print("正在将对象序列化到文件 dump.txt ...")
        pickle.dump(d, f)
        print("序列化完成。")
except IOError as e:
    print(f"文件操作失败: {e}")

# --- 3. 使用 pickle.load() 从文件反序列化对象 ---
# 'rb' 表示以二进制（binary）读取（read）模式打开文件
try:
    with open('dump.txt', 'rb') as f:
        # pickle.load() 从文件中读取数据并重建 Python 对象
        print("\n正在从文件 dump.txt 反序列化对象...")
        d_reconstructed = pickle.load(f)
        print("反序列化完成。")

        # --- 4. 验证结果 ---
        print("\n原始对象:", d)
        print("重建后的对象:", d_reconstructed)
        print("两个对象是否相同:", d == d_reconstructed)

except FileNotFoundError:
    print("错误：找不到 dump.txt 文件，请先运行序列化部分。")
except IOError as e:
    print(f"文件操作失败: {e}")
