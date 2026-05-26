# pattern_match.py
# 演示 Python 的 match…case 模式匹配用法

def simple_match(score):
    """匹配简单值"""
    match score:
        case 'A':
            print('score is A.')
        case 'B':
            print('score is B.')
        case 'C':
            print('score is C.')
        case _:
            print('score is ???.')

def age_match(age):
    """多种匹配条件示例：值绑定、多个值匹配、默认情况"""
    match age:
        case x if x < 10:
            print(f'< 10 years old: {x}')
        case 10:
            print('10 years old.')
        case 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
            print('11~18 years old.')
        case 19:
            print('19 years old.')
        case _:
            print('not sure.')

def args_match(args):
    """按列表结构匹配命令参数"""
    match args:
        case ['gcc']:
            print('gcc: missing source file(s).')
        case ['gcc', file1, *files]:
            print('gcc compile:', file1, ', '.join(files))
        case ['clean']:
            print('clean')
        case _:
            print('invalid command.')

def main():
    print('--- simple_match examples ---')
    simple_match('A')
    simple_match('D')

    print('\n--- age_match examples ---')
    for a in [5, 10, 13, 19, 21]:
        print('age =', a, '->', end=' ')
        age_match(a)

    print('\n--- args_match examples ---')
    examples = [
        ['gcc'],
        ['gcc', 'hello.c'],
        ['gcc', 'hello.c', 'world.c'],
        ['clean'],
        ['other']
    ]
    for cmd in examples:
        print('args =', cmd, '->', end=' ')
        args_match(cmd)

if __name__ == '__main__':
    main()