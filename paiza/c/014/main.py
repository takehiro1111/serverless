"""C014:ボールが入る箱
半径r のお気に入りのボールを手に入れたあなたは、それを収納することができる箱を探しています。

今、n 個の箱があり、i (1 ≦ i ≦ n) 番目の箱は高さh_i、幅w_i、奥行きd_i です。各箱においてボールの直径が、箱の高さ、幅、奥行きの3つの長さのうち最も短いもの以下であれば、無事にボールを収納することができます。


入力例1 の図
offside figure2

ボールの半径と箱の情報が与えられるので、ボールを収納することができる箱の番号を昇順にすべて答えてください。

入力例1
4 2
6 6 6
4 6 4
6 1 1
4 4 4

n r #箱の数n, ボールの半径r 表す整数
h_1 w_1 d_1 #1個目の箱の高さ、幅、奥行きを表す整数
h_2 w_2 d_2 #2個目の箱の高さ、幅、奥行きを表す整数

出力例1
1
2
4
"""

# boxes = 箱の数 radius = 基準となるボールの半径
BOXES, RADIUS = list(map(int, input().split()))

for i in range(1, BOXES + 1):
    # 繰り返し処理で箱のサイズを取得
    high, width, depth = list(map(int, input().split()))

    # 箱のサイズで高さ、幅、奥行きで最も短いものを判定。
    minimum = min(high, width, depth)

    # ボールの直径を定義
    diameter = RADIUS * 2

    # ボール(直径)と上記で判定されたサイズを比較してボールが箱のサイズ以下であれば出力する。
    if diameter <= minimum:
        print(i)
