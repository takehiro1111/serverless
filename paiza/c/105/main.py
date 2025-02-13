"""C105:カードのスコア
あなたは数字の書かれた何枚かのカードを持っていて、それらのカードの総合スコアを計算しようとしています。

カードは 1 ～ 100 の数字が書かれたものが 1 枚ずつあり、あなたはそれらのうち N 枚のカードを持っています。このとき、この N 枚のカードの総合スコアは以下のように計算されます。

・10, 11, 12 のように、1 の差で連続しているカードを 1 つのグループにする。例えば、5, 10, 11, 12, 24, 25 というカードがあったら「5」というグループと「10, 11, 12」というグループと「24, 25」というグループに分かれる。
・各グループのスコアは、グループ内の最大の数であり、総合スコアは各グループのスコアの和である。例えば上記の例では、「5」というグループのスコアは 5 で、「10, 11, 12」というグループのスコアは 12 で、「24, 25」というグループのスコアは 25 なので、総合スコアは 5+12+25 = 42 である。

持っている N 枚のカードのリストが与えられるので、これらのカードの総合スコアを求めてください

入力例1
6
5 10 11 12 24 25


出力例1
42

"""

# カードの枚数を受け取る。
N = int(input())


n_list = sorted([int(i) for i in input().split()])

all_groups = []
current_group = [n_list[0]]

for i in range(1, N):
    # 前の要素と連続している場合
    if n_list[i] == n_list[i - 1] + 1:
        current_group.append(n_list[i])

    else:
        # 連続した数字ではない場合
        all_groups.append(current_group)
        current_group = [n_list[i]]

all_groups.append(current_group)

total = sum(max(group) for group in all_groups)
print(total)


# # カードの番号を受け取る。
# n_list = sorted([int(i) for i in input().split()])
# # [5, 10, 11, 12, 24, 25]


# groups = []  # 全てのグループを保持するリスト 多次元配列でグループを持つ。
# current_group = [n_list[0]]  # 現在処理中のグループ

# # カードをグループ化する。
# for i in range(1, N):
#   # 連続した数字はそれ用のリストに入れる。
#   if n_list[i] == n_list[i-1]+1: # 前の数字と連続している場合
#     current_group.append(n_list[i])
#     print(f"current_group{current_group}")
#   else:
#     groups.append(current_group)
#     print(f"groups:{groups}")

#     # 現在処理している要素に更新する。
#     current_group = [n_list[i]]
#     print(f"current_group,else{current_group}")


# groups.append(current_group)  # 最後のグループを追加

# print(groups)

# total = sum(max(group) for group in groups)
# print(total)
