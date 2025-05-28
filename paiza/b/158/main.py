# paiza さんは遺跡を調査していたところ、床にたくさんの石が積まれた不思議な部屋を見つけました。
# 部屋を調べてみたところ、床面には N×N 個の板が敷き詰められており、板の上には大きさも重さも均一な石が板からはみ出さないように積まれていることが分かりました。

# paiza さんは帰って文献を調べてみたところ、部屋の中心の板を頂上としたピラミッド状に石を積むことで扉が開く仕掛けになっていることが分かりました。
# そこで paiza さんはそれぞれの板の上の石の数を以下の図のようにするため石を運び出すことにしました。


# 1 番外側の円の板の上には 1 個、その 1 つ内側には 2 個、そして中心には (N+1)/2 個とピラミッド状に石を積むようにしたとき、いくつの石を運び出す必要があるか出力してください。
# ただし、i 行 j 列目 (1 ≦ i, j ≦ N) の板に積まれた石はその板に積むべき石の数以上であることが保証されます。


# 入力例 1 の場合、それぞれの板について運び出さなければならない石の数は上図のように左上から順に
# 2 2 2 1 5
# 0 7 2 3 2
# 0 6 1 4 4
# 3 7 0 4 7
# 6 4 7 0 5
# となります。これらを合計すると 84 となるので 84 と出力してください。

# 入力例1
# 5
# 3 3 3 2 6
# 1 9 4 5 3
# 1 8 4 6 5
# 4 9 2 6 8
# 7 5 8 1 6

# 出力例1
# 84

store_row_num = int(input())

stock_store_row = []

for i in range(store_row_num):
    store_row = list(map(int, input().split()))

    match i:
        case 0:
            calc = [i - 1 for i in store_row]

        case 1:
            calc = [i - 1 for i in store_row]

        case 2:
            calc = [i - 1 for i in store_row]

        case 3:
            calc = [i - 1 for i in store_row]

        case 4:
            calc = [i - 1 for i in store_row]

    stock_store_row.extend(calc)

    stock_store_row.append(store_row)


stone_row_num = int(input())

total_carry_stones = 0

for i in range(stone_row_num):
    stone_row = list(map(int, input().split()))

    for j in range(stone_row_num):

        # 現在のマス目の数を取得
        current_stone_position = stone_row[j]

        # 位置によって
        # stone_row_num-1-i マスが下端からどれだけ離れているか（行数）
        # stone_row_num-1-j マスが右端からどれだけ離れているか（列数）
        layer = min(i, j, stone_row_num - 1 - i, stone_row_num - 1 - j)
        target_stones = layer + 1

        # マス目から運び出す石の数
        stones_carry_from_position = current_stone_position - target_stones

        # トータルの数に加算
        total_carry_stones += stones_carry_from_position

print(total_carry_stones)
