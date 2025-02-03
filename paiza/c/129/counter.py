from collections import Counter

# 入力
## 寿司の種類の数と寿司の情報の受け取り
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

# 各寿司の出現回数を比較
if Counter(sort_order) == Counter(random_order):
    print(Counter(sort_order))
    print(Counter(random_order))
    print("Yes")
else:
    print("No")
