"""C048:タダ飲みコーヒー

あなたがよく利用しているコーヒーショップは本日限定であるサービスを行っています。

・コーヒーをお買い上げした際に、次のお買い上げの値段を更に P% off!
・毎回の値下げにおいて小数点以下切り捨て

あなたは値下げが累積する事に目をつけました。
コーヒーを何回も飲んでいれば、タダでコーヒーを飲めるようになるのです。

図1

タダで頼みたいあなたは、何円払えば以後タダで注文できるのか計算したくなりました。
実際にプログラムを書いて計算してみましょう。

入力例1
300 50
出力例1
596
"""

import math

# 入力の受け取り
X, P = map(int, input().split())

total = X  # 支払い総額
price = X  # 現在の価格

# 処理
while True:
    # 次回の価格を計算（前回の価格から割引率を適用）
    next_price = math.floor(price - (price * P / 100))
    # next_price = math.floor(price * (100 - P) / 100)

    # 支払額が0円になったら終了
    if next_price == 0:
        break

    # 合計に加算
    total += next_price
    # 次回の価格を更新
    price = next_price

print(total)


# import math
# # 入力の受け取り
# ## コーヒーの最初の単価 割引率
# X, P = map(int,input().split())
# # 300 50

# #初期値の設定
# ## あらかじめ最初の金額(300円)を入れておく。
# amount = X

# # 処理
# ## 支払いの処理だが、回数が決まってないためwhileを使用。
# while True:
#   # 単価から50%分を支払う
#   # 最初は、300*0.5
#   # 割引後の金額を計算
#   X = X * ((100 - P) * 0.01)
#   amount += math.floor(X)

#   if math.floor(X) == 0:
#     break

# print(math.floor(amount))
