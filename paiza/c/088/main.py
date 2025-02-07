"""
RPG の道具屋での買い物をシミュレートしてみましょう。
具体的には、最初の所持金と注文履歴から、最終的な残金を計算します。
ただし、注文時に所持金が足りない場合、その注文は無視されます。

入力例 1 では、お金の単位を G として、ある道具屋での単価が下の表のようになっています。

ここで、初期の所持金が 300 G であり、注文履歴が

1. やくそう 5 個
2. せいすい 3 個
3. きのぼう 1 個
4. せいすい 1 個
5. やくそう 3 個

であるため、残金は次のように計算できます。

1. やくそう 5 個を買える所持金があるので、残金は 300 - 10 × 5 = 250 G
2. せいすい 3 個を買える所持金はないので、残金は 250 G
3. きのぼう 1 個を買える所持金があるので、残金は 250 - 50 × 1 = 200 G
4. せいすい 1 個を買える所持金があるので、残金は 200 - 100 × 1 = 100 G
5. やくそう 3 個を買える所持金があるので、残金は 100 - 10 × 3 = 70 G

よって、最終的な残金は 70 G です。

このような計算をシミュレートするプログラムを作成してください。

入力される値
入力は以下のフォーマットで与えられます。

入力例1
3
10 100 50
300 5
1 5
2 3
3 1
2 1
1 3

N
a_1 ... a_N
T Q
x_1 k_1
...
x_Q k_Q
・1 行目には、道具の個数を表す整数 N が与えられます。
・2 行目には、 N 個の各道具の単価が半角スペース区切りで与えられます。
　・ここで、 a_i (1 ≦ i ≦ N) は i 番目の道具の単価を表します。
　・3 行目には、最初の所持金を表す整数 T と注文回数を表す整数 Q が与えられます。
・3 + j 行目 (1 ≦ j ≦ Q) には、 j 回目の注文の情報が以下の形式で与えられます。
　・購入したい道具の番号を表す整数 x_j とその個数 k_j が半角スペース区切りで与えられます。
・入力は合計で Q + 3 行となり、入力値最終行の末尾に改行が 1 つ入ります。


出力例1
70
"""

# 道具の数の入力
# 3
ITEMS = int(input())

# 各道具の単価/G
# herb(薬草):10 -> 1 聖水(holy_water):100 -> 2 木の棒(wood):50 -> 3
tool_amount = [int(i) for i in input().split()]

# 最初の所持金/Gと注文回数の受け取り
# 300 5
money, orders = map(int, input().split())

for _ in range(orders):
    # 道具のIDと購入数の受け取り
    tool_id, tool_num = map(int, input().split())

    # 買い物時の計算実施
    ## tool_amount[tool_id-1] -> 道具のIDと単価をマッピング
    trade = tool_amount[tool_id - 1] * tool_num
    if money >= trade:
        money -= trade
    # 所持金が購入金額よりも小さければ処理をスキップして買わない。
    elif money < trade:
        continue

print(money)


####################################################################
# より良い書き方
####################################################################
# 関数化でコードの責任範囲を限定
def can_afford(money: int, price: int, quantity: int) -> bool:
    return money >= price * quantity


def process_order(money: int, prices: list, order_id: int, quantity: int) -> int:
    total_cost = prices[order_id - 1] * quantity
    if can_afford(money, prices[order_id - 1], quantity):
        return money - total_cost
    return money


# Input processing
item_count = int(input())
prices = list(map(int, input().split()))
money, order_count = map(int, input().split())

# Process orders
for _ in range(order_count):
    item_id, quantity = map(int, input().split())
    money = process_order(money, prices, item_id, quantity)

print(money)
