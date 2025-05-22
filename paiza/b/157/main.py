# paiza さんは節約が好きです。 今日も節約のために安いスーパーを回って野菜を買うことにしました。

# paiza さんの家の近くに N 軒のスーパーがあります。
# すべてのスーパーで同じ K 種類の野菜が売られていますが、それぞれ値段が異なっています。

# paiza さんは K 種類の野菜をすべて 1 つずつ買いたいです。
# スーパーを回って合計金額が一番安くなるように野菜を購入するとき、最低で何件のスーパーを回る必要があるか出力してください。

# 入力例1
# 3 3
# 100 200 300
# 150 180 210
# 200 150 200

# 出力例1
# 2

stores, vegetables = map(int, input().split())


# [[100, 200, 300], [150, 180, 210], [200, 150, 200]]
total_vegetables = []
for _ in range(stores):
    shop_vegetable_str = input().split()
    shop_vegetable_int = [int(i) for i in shop_vegetable_str]
    total_vegetables.append(shop_vegetable_int)


most_inexpensive_store = set()

for veg_idx in range(vegetables):
    initial_num = float("inf")

    for store_idx in range(stores):

        vege_amount = total_vegetables[store_idx][veg_idx]

        if vege_amount < initial_num:
            initial_num = vege_amount
            most_inexpensive_store_idx = store_idx

    most_inexpensive_store.add(most_inexpensive_store_idx)

print(len(most_inexpensive_store))
