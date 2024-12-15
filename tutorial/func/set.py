# dict = {
#   "sports" : "soccer",
#   "game" : "monsto",
#   "anime" : "naruto",
#   "game" : "pazudora"
# }


# print(set(dict.items()))

# alpha = ["a","b","c"]

# set = { i.upper() for i in alpha}
# print(set)

# num = {1,2,3}
# add_set = num.add(4)
# print(add_set)
# print(num)

# rem = {1,2,3}
# rem.remove(2)
# # rem.remove(4)
# print(rem)

# num = {1,2,3}
# num.discard(1)
# num.discard(4)
# print(num)

# num = {1,2,3}
# num.pop()
# print(num)

# num = {1,2,3}
# num.clear()
# print(num)


# s1 = {0, 1}
# s2 = {1, 2}
# s3 = {3, 4}

# union = s1 | s2 | s3
# print(union)

# s1 = {0, 1}
# s2 = {1, 2}
# s3 = {3, 4}

# s1 |= s2

# print(s1)

# a = [1]
# b = {2}
# c = (3,4)

# b.update(a,c)
# print(b)

# s1 = {0, 1}
# l1 = [1, 2]
# t1 = (3, 4)

# s1.update(l1, t1)
# print(s1)


# ### 差集合
# s1 = {0, 1}
# s2 = {1, 2}
# s3 = {2, 3}

# dif = s1 - s2 - s3
# print(dif)

# s1 = {0, 1}
# l1 = [1, 2]
# t1 = (2, 3)

# dif = s1.difference(l1, t1)
# print(dif)

# s1 = {0, 1}
# s2 = {1, 2}
# s3 = {2, 3}

# s1 -= s2
# s1 -= s3

# print(s1)

# s1 = {0, 1}
# l1 = [1, 2]
# t1 = (2, 3)

# s1.difference_update(l1, t1)
# print(s1) # {0}

# set1 = {1,2}
# set2 = {2,4}

# total = set1 & set2
# print(total)

# set1 = {1,2}
# set2 = [2,3]

# total = set1.intersection(set2)
# print(total)

# set1 = {1,2}
# set2 = {2,4}

# set1 &= set2
# print(set1)

s1 = {0, 1, 2}
s2 = {1, 2, 3}
s3 = {2, 3, 4}

s1 &= s2
print(s1)

s1 &= s3
print(s1)

s1 = {1, 2, 3, 4, 5, 6}
l1 = [1, 2, 3]

print(s1.issuperset(l1))
