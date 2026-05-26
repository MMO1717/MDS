# conditions.py
# 演示 Python 中的条件判断（if / elif / else）

def demo_basic_if():
    age = 20
    if age >= 18:
        print('your age is', age)
        print('adult')
    else:
        print('your age is', age)
        print('teenager')

def demo_elif_chain():
    age = 3
    if age >= 18:
        print('adult')
    elif age >= 6:
        print('teenager')
    else:
        print('kid')

def demo_order_matters():
    age = 20
    if age >= 6:
        print('teenager (because this condition is checked first)')
    elif age >= 18:
        print('adult')
    else:
        print('kid')

def demo_truthiness():
    x = [1, 2, 3]
    if x:
        print('x is truthy because it is non-empty')
    else:
        print('x is falsy')

def demo_input_issue():
    # input() 返回字符串，不能直接与数字比较
    # birth = input('birth: ')
    # if birth < 2000:  # 会报错：TypeError
    #     ...

    s = input('birth year: ')
    try:
        birth = int(s)
        if birth < 2000:
            print('00前')
        else:
            print('00后')
    except ValueError:
        print('输入不是合法数字，无法判断出生年份')

def demo_bmi():
    # BMI 计算练习
    height = 1.75  # 米
    weight = 80.5  # 公斤
    bmi = weight / (height ** 2)
    print(f'BMI 指数为: {bmi:.1f}')
    if bmi < 18.5:
        print('过轻')
    elif bmi < 25:
        print('正常')
    elif bmi < 28:
        print('过重')
    elif bmi < 32:
        print('肥胖')
    else:
        print('严重肥胖')

def main():
    print('--- 基本 if 示例 ---')
    demo_basic_if()
    print('\n--- if-elif-else 示例 ---')
    demo_elif_chain()
    print('\n--- 判断顺序的重要性 ---')
    demo_order_matters()
    print('\n--- 值的 Truthiness 测试 ---')
    demo_truthiness()
    print('\n--- 输入与类型转换问题示范 ---')
    demo_input_issue()
    print('\n--- BMI 计算练习 ---')
    demo_bmi()

if __name__ == '__main__':
    main()