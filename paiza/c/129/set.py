sushi_types, sushi_count = list(map(int, input().split()))
# 3 5

## i 番目に並べるべき寿司の番号を表す整数 A_iの受け取り
sort_order = [int(input()) for _ in range(1, sushi_count + 1)]
print(sort_order)
# [1,2,1,2,3]

## パックを作成するために j 番目に流れてきた寿司の番号を表す整数 B_jの受け取り
random_order = [int(input()) for _ in range(1, sushi_count + 1)]
print(random_order)
# [2, 1, 3, 2, 1]


if set(sort_order) == set(random_order) and len(sort_order) == len(random_order):
    print("Yes" if sorted(sort_order) == sorted(random_order) else "No")
else:
    print("No")
