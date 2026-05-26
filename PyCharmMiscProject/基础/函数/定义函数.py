import math

def my_abs(x):
   if not isinstance(x,(int , float)):
       raise TypeError('bad operand type')
   elif x < 0:
       return -x
   elif x == 0:
       return 0
   else:return x

print(my_abs(-10))
print(my_abs(255))

def move(x,y,step,angle=0):
    nx=x+step*math.cos(angle)
    ny=y+step*math.sin(angle)
    return nx,ny
x, y = move(100, 100, 60, math.pi / 6)
print(x, y)

def quadratic(a, b, c):
    delta = b*b - 4*a*c
    if delta < 0:
        return None  # 没有实数解
    elif delta == 0:
        return -b / (2*a)
    else:
        root1 = (-b + math.sqrt(delta)) / (2*a)
        root2 = (-b - math.sqrt(delta)) / (2*a)
        return root1, root2

print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')
