sushi_types, sushi_count = map(int, input().split())
sort_order = [int(input()) for _ in range(sushi_count)]
# [1,2,1,2,3]
random_order = [int(input()) for _ in range(sushi_count)]
# [2, 1, 3, 2, 1]

# 各寿司の出現回数を数える
count_sort = [0] * (sushi_types + 1)
count_random = [0] * (sushi_types + 1)

for s, r in zip(sort_order, random_order):
    count_sort[s] += 1
    print(f"count_sort{count_sort}")
    count_random[r] += 1
    print(f"count_random{count_random}")

print("Yes" if count_sort == count_random else "No")


# count_sort[0, 1, 0, 0]
# count_random[0, 0, 1, 0]
# count_sort[0, 1, 1, 0]
# count_random[0, 1, 1, 0]
# count_sort[0, 2, 1, 0]
# count_random[0, 1, 1, 1]
# count_sort[0, 2, 2, 0]
# count_random[0, 1, 2, 1]
# count_sort[0, 2, 2, 1]
# count_random[0, 2, 2, 1]
# Yes

# 　上記出力のように足していけば同じ要素になるため、間接的に並び替え可能ということ。
