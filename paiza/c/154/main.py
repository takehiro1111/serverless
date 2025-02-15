"""C154:半額クーポン
あなたはスーパーで N 個の商品を購入しました。それぞれの商品の価格は u_i 円です。

あなたは 1 枚の半額クーポンを持っています。
半額クーポンは L 円以上の商品があれば、その中でもっとも高額な 1 つの商品に自動的に適用されます。
お会計の合計金額を出力してください。

図1

たとえば、入力例 1 では 1292円, 1274円, 1546円 の3つの商品を購入します。
クーポンが適用できるのは 703円 以上からなので、購入するすべての商品にクーポンを適用可能です。

購入する商品の中でもっとも高額な商品は 1546円 の商品なので、この商品にクーポンを適用して 773円 で購入します。
このときの合計金額は 3339円 となります。

入力例1
3 703
1292 1274 1546

出力例1
3339

"""

import math

# 入力
## 商品数 N, クーポンの基準金額 L
# 3 703
N, L = map(int, input().split())

## 食べ物ごとに金額をリストで受け取り
### [1292, 1274, 1546]
orders = [int(i) for i in input().split()]

max_order = max(orders)
orders.remove(max_order)
if max_order >= L:
    discount_price = max_order / 2
    orders.append(discount_price)
elif max_order <= L:
    orders.append(max_order)

total = 0
for x in orders:
    total += x

print(math.floor(total))
