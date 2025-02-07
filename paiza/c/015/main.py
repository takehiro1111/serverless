"""C015:ポイントカードの計算
今は月末。そろそろ今月の家計簿をつけないといけません。 あなたの手元には、とあるスーパーマーケットのレシートの山があります。

スーパーマーケットにはポイントカードが導入されていて、買い物をするたびに購入金額に応じたポイントがたまります。
加算されるポイントは次の 3 つのルールに従って決定されます。

1. 通常は購入金額の 1 ％（小数点以下切り捨て）とする
2. 3 のつく日は購入金額の 3 ％（小数点以下切り捨て）とする
3. 5 のつく日は購入金額の 5 ％（小数点以下切り捨て）とする

あなたはポイントカードに、今、何ポイントたまっているのかが気になりました。
レシートの数が多いので、手で計算するのは大変です。

早速、これを計算するプログラムを書きましょう。
ただし、今月のはじめには全くポイントがたまっておらず（0 ポイント）、また、今月中ポイントは消費されなかったものとします。

入力例1
3
1 1024
11 2048
21 4196

N　　　　#各レシートの数
d_1 p_1　#1枚目のレシートの日付 d_1 日, 購入金額 p_1 円
d_2 p_2　#2枚目のレシートの日付 d_2 日, 購入金額 p_2 円
...
d_N p_N　#N枚目のレシートの日付 d_N 日, 購入金額 p_N 円

出力例1
71

"""

import math

RECEIPT = int(input())

point = 0
for _ in range(RECEIPT):
    # 日付と金額の入力
    day, price = map(int, input().split())

    # ポイントの付与ルールの定義
    three_double = (3, 13, 23, 30, 31)
    five_double = (5, 15, 25)

    # レシート分のポイントを計算
    if day in three_double:
        point += math.floor(price * 0.03)
    elif day in five_double:
        point += math.floor(price * 0.05)
    else:
        point += math.floor(price * 0.01)

print(point)
