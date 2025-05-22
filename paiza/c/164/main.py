# # # # 長さ N の配列 A があり、パイザさんはこれを昇順に並べ替えたいと思っています。

# # # たくさんの時間を費やした結果、 Q 回の入れ替えを行うことで、並べ替えができるのではないかと考えました。
# # # 「入れ替え」とは、整数 i, j (1 ≦ i, j ≦ N) を自由に選び、 A_i と A_j を交換することを表します。

# # # 配列 A と Q 回の入れ替えの内容が与えられます。
# # # 入れ替えを行った結果、配列の内容が昇順となっている場合は "Yes" を、そうでない場合は "No" を出力してください。

# # # 例えば、入力例 1 では、以下の図のような入れ替えを行います。

# # 入力例1
# # 3
# # 7 4 3
# # 5
# # 2 3
# # 1 2
# # 1 3
# # 2 3
# # 1 2


# 出力例1
# Yes


# N = 長さ3
# A = [7, 4, 3]
# Q = 5

length = int(input())

# 配列
array_str = input().split()
array = [int(num) for num in array_str]

# 入れ替え回数
times = int(input())

# 配列の長さ
# ソート処理
for _ in range(times):
    i, j = map(int, input().split())
    array[i - 1], array[j - 1] = array[j - 1], array[i - 1]


# ソートが昇順だったらYesを表示
def main():
    for k in range(length - 1):
        if array[k] > array[k + 1]:
            return "No"

    return "Yes"


print(main())
