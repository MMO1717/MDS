print('dic')
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d)
d['Kevin']=100
print(d)
print('Kevin的成绩是',d['Kevin'])
print('Kevin' in d)
print(d.get('Kevin'))
print(d.get('Kobe'))

print()
print('set')
s = {1, 2, 3}
print(s)
s = {1, 1, 2, 2, 3, 3}
print(s)
s.add(4)
print(s)
s.remove(4)
print(s)
s2 = {2, 3, 4}
print(s&s2)
a = ['c', 'b', 'a']
a.sort()
print(a)
