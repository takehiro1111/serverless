def add(a, b):
    a + b  # 結果を表示するだけ

result = add(3, 5)  # ここでは値を受け取れない
print(result)  # 出力: None

l = ["Mon","tue","wed","Thu","fri","Sat","sun"]

def basic(list_args,context):
  for list_arg in list_args:
    print(context(list_arg))

basic(l,lambda list_arg: list_arg.capitalize())

l = [-3,-2,-1,0]

print(map(abs,l))
print(list((map(abs,l))))
print(type(map(abs, l)))

for i in map(abs,l):
  print(i)

l_str = ['Tokyo','Osaka']
print(list(map(len,l_str)))

print(list(map(lambda x : x ** 2,l)))

def test(x):
  return x ** 2

print(list(map(test,l)))

t_1 = (1,2,3)
t_2 = (10,20,30)

print(tuple(map(lambda x,y : x * y, t_1,t_2)))


print([x * y for x,y in zip(t_1,t_2)])

import numpy as np

a = np.array([-2, -1, 0])
print(np.abs(a))
# [2 1 0]

print(a**2)
# [4 1 0]

a_1 = np.array([1, 2, 3])
a_2 = np.array([10, 20, 30])
print(a_1 * a_2)
# [10 40 90]
