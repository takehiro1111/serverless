"""

あなたは、株の売買でのお金儲けを考えています。
N 日の間、1 日に一度株価をチェックし、以下のルールに従い売買をします。

・株価が c_1 円以下の場合、1 株買う
・株価が c_2 円以上の場合、持ち株「を」すべて売る
・株価が c_1 円、c_2 円の間の場合は、何もしない
・N 日目には、上記を行わず持ち株をすべて売る

N 日目に持ち株をすべて売ったあとでの損益を出力してください。ただし、入力例 2 のように損益がマイナスになる場合があることに注意してください。

入力例1
5 110 120
110
100
120
130
105

出力例1
30
"""

DAYS, stock_price_lower, stock_price_max = list(map(int, input().split()))

# 持ち株
holdings = 0

# 利益
profit = 0


for i in range(1, DAYS + 1):
    # 日々の株価の入力を受け取る。
    stock_price_daily = int(input())

    if i == DAYS:
        # 最終日は持ち株をすべて売る
        last_day_holdings = stock_price_daily * holdings
        profit += last_day_holdings
        holdings = 0
    else:
        if stock_price_daily <= stock_price_lower:
            holdings += 1
            print(f"{i}.holdings:{holdings}")
            print(f"{i}.stock_price_daily:{stock_price_daily}")
            profit -= stock_price_daily
            print(f"{i}.profit:{profit}")
        elif stock_price_daily >= stock_price_max:
            print(f"{i}.stock_price_daily:{stock_price_daily}")
            profit += stock_price_daily * holdings
            print(f"{i}.profit:{profit}")
            holdings = 0
            print(f"{i}.holdings:{holdings}")
        elif i == DAYS:
            # 最終日は持ち株をすべて売る
            last_day_holdings = stock_price_daily * holdings
            profit += last_day_holdings
            holdings = 0


print(profit)

# 1.holdings:1
# 1.stock_price_daily:80
# 1.profit:-80

# 2.holdings:2
# 2.stock_price_daily:80
# 2.profit:-160

# -160


# 1.holdings:1
# 1.stock_price_daily:110
# 1.profit:-110

# 2.holdings:2
# 2.stock_price_daily:100
# 2.profit:-210

# 3.stock_price_daily:120
# 3.profit:30
# 3.holdings:0

# 4.stock_price_daily:130
# 4.profit:30
# 4.holdings:0

# 5.holdings:1
# 5.stock_price_daily:105
# 5.profit:-75
