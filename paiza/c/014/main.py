"""C014:ボールが入る箱.

半径r のお気に入りのボールを手に入れたあなたは、それを収納することができる箱を探しています。

今、n 個の箱があり、i (1 ≦ i ≦ n) 番目の箱は高さh_i、幅w_i、奥行きd_i です。各箱においてボールの直径が、
箱の高さ、幅、奥行きの3つの長さのうち最も短いもの以下であれば、無事にボールを収納することができます。


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


def box_size_decision(radius: int, height: int, width: int, depth: int) -> bool:
    """ボールが箱のサイズ以下かどうかを判定する関数.

    Args:
        radius (int): ボールの半径
        height (int): 箱の高さ
        width (int): 箱の幅
        depth (int): 箱の奥行き

    Returns:
        bool: ボールが箱のサイズ以下の場合にTrueを返す。
    """
    # 箱のサイズで高さ、幅、奥行きで最も短いものを判定。
    min_dimension = min(height, width, depth)

    # ボール(直径)と上記で判定されたサイズを比較してボールが箱のサイズ以下であればTrueを返す。
    result = radius * 2 <= min_dimension

    # 判定結果を返す
    return result


# boxes = 箱の数 radius = 基準となるボールの半径
BOXES, RADIUS = list(map(int, input().split()))

for i in range(1, BOXES + 1):
    # 繰り返し処理で箱のサイズを取得
    height, width, depth = list(map(int, input().split()))

    # 関数の戻り値がTrue(ボールが箱のサイズ以下)の箱の番号を出力。
    if box_size_decision(RADIUS, height, width, depth):
        print(i)
