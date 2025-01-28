"""C150:ご挨拶
PAIZA さんは以前から住みたかった町に引っ越して来ました。

その町には碁盤の目状に道が張り巡らされており、合計で N 軒の家が建っています。
しかし、家同士には距離があるため、PAIZAさんは距離 D までのご近所さんにご挨拶に伺うことにしました。

PAIZA さんの家の座標とその他の家の座標が与えられます。
PAIZA さんが挨拶に向かう件数を出力してください。

図1

家同士の距離は | x_1 - x_2 | + | y_1 - y_2 | で定義されます。

たとえば、入力例 1 では、PAIZA さんの家は (0, 0) にあり、

家 1 との距離は | 0 - 2 | + | 0 - 3 | = 5
家 2 との距離は | 0 - 9 | + | 0 - 4 | = 13
家 3 との距離は | 0 - 5 | + | 0 - 4 | = 9

ご挨拶に伺う家は距離が 10 以下の家なので、家 1 と家 3 にご挨拶に伺います。
ご挨拶に伺う家は 2 軒なので 2 を出力してください。

入力例1
3 10
0 0
2 3
9 4
5 4

出力例1
2
"""

# ASKS = 訪問を検討する件数 , STANDARD = 訪問する距離の基準
ASKS, STANDARD = list(map(int, input().split()))

# myhome_x = 自分家のx軸 myhome_y = 自分家のy軸
myhome_x, myhome_y = list(map(int, input().split()))

# 訪問する件数をカウントするための変数
counter = 0

for _ in range(ASKS):
    # otherhome_x = 訪問先のx軸 , otherhome_y = 訪問先のy軸
    otherhome_x, otherhome_y = list(map(int, input().split()))

    # 家同士の距離は | x_1 - x_2 | + | y_1 - y_2 | で定義
    ## 上記公式に沿って基準値を計算。
    ## absで最終的に絶対数になるよう書いている。
    distance = abs(myhome_x - otherhome_x) + abs(myhome_y - otherhome_y)
    print(f"distance:{distance}")

    # 判定し、Trueなら訪問件数としてカウントする。
    if distance <= STANDARD:
        counter += 1

print(counter)
