"""C083:売上の発表
あなたは PAIZA 社のエンジニアです。あなたはこれまでの売上のデータを横向きの棒グラフにする仕事を振られました。

与えられたデータは N 期分のデータで、第 i 期 (1 ≦ i ≦ N) の売上は a_i です。

これをそのまま棒グラフにするととても長いグラフになります。ところが、幸いすべての期の売上が R の倍数になっていることに気づきました。

そこで、売上のデータの単位を R として棒グラフを表示するプログラムを作成しましょう。

入力例 1 では、N = 3 期分のデータが与えられ、第 1 期の売上は a_1 = 5 、第 2 期の売上は a_2 = 15 、第 3 期の売上は a_3 = 10 です。売上データの単位を R = 5 として棒グラフにすると、下図のようになります。

1:*..
2:***
3:**.
このような形で、売上データが与えられた時に棒グラフを出力してください。
ただし、グラフの横幅は売り上げの最大値を R で割った数とします。上の例では 15 ÷ 5 = 3 が横幅となります。

入力例1
3 5
5
15
10

出力例1
1:*..
2:***
3:**.
"""

# 入力
# N = 期数 R = 倍数
N, R = map(int, input().split())


# 売上の受け取り
sales_lst = []
for i in range(N):
    sales = int(input())
    sales_lst.append(sales)

# 表示する際の最大の幅を算出
max_width = max(sales_lst) // R


for i in range(N):
    stars = sales_lst[i] // R

    # 出力
    ## 番号の表示
    print(f"{i + 1}:", end="")
    ## *の表示
    print(f"*" * stars, end="")
    ## .の表示
    print(f"." * (max_width - stars), end="\n")


# 売上の受け取り
# sales_lst = []
# for i in range(N):
#   sales = int(input())
#   sales_lst.append(sales)

# # グラフの最大幅を計算（最大売上 ÷ R）
# max_width = max(sales_lst) // R

# # 各期の棒グラフを出力
# for i in range(N):
#     # 現在の期の売上を R で割って "*" の数を計算
#     stars = sales_lst[i] // R

#     # i+1 を出力（1から始まる期の番号）
#     print(f"{i+1}:", end="")
#     # "*" を必要な数だけ出力
#     print("*" * stars, end="")
#     # 残りの部分を "." で埋める
#     print("." * (max_width - stars))
