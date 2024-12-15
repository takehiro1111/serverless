l = [-2, -1, 0]
# fu = map(abs,l)
# print(fu)
# print(map(abs, l))

# print(type(map(abs, l)))

for i in map(abs,l):
  if i > -1:
    print(i)

l_s = ['apple', 'orange', 'strawberry']
print(list(map(len, l_s)))


l_1 = [1, 2, 3]
l_2 = [10, 20, 30]
print(list(map(lambda x, y: x * y, l_1, l_2)))
