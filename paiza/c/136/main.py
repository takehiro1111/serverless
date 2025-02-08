"""C136:ダイエットの連続記録
A さんは、体重の増減を気にしています。
A さんは、気が向いた時だけダイエットをしており、ダイエットをしているときは、
体重が落ち、ダイエットをしていないときは、体重が増えます。A さんの体重の記録が与えられるので、
過去に最大何日連続でダイエットが続いたかと最大何日連続でダイエットを怠ったかを求めてください。

入力例 1 の場合、以下の図のように、最大 3 日間連続でダイエットを続けました。
また、最大 2 日間連続でダイエットを怠り続けました。

入力例1
8
55
56
57
55
56
53
52
50

出力例1
3 2
"""

# 入力
##  体重の総数を表す整数 N
N = int(input())

weight_record = []

## 体重の記録
for i in range(N):
    weight = int(input())
    weight_record.append(weight)

print(weight_record)
# [55, 56, 57, 55, 56, 53, 52, 50]

# ダイエットをした日とサボった日のカウンター
success_diet_days = 0
max_success_record = 0

failed_diet_days = 0
max_failed_record = 0

# 処理
for i, element in enumerate(weight_record):
    if i < 1:
        continue
    elif weight_record[i] < weight_record[i - 1]:
        # 前日より体重が落ちたのでダイエット成功として1日を加算
        success_diet_days += 1

        # 失敗の記録はリセット
        failed_diet_days = 0

        # 連続記録の値の維持
        max_success_record = max(max_success_record, success_diet_days)

    elif weight_record[i] > weight_record[i - 1]:
        # 前日より体重が落ちたのでダイエット失敗として1日を加算
        failed_diet_days += 1

        # 成功のストリークはリセット
        success_diet_days = 0

        # 連続記録の値の維持
        max_failed_record = max(max_failed_record, failed_diet_days)

print(f"{max_success_record} {max_failed_record}")
