"""C096:夏休み
子供は夏休みまっただ中。家族や親戚を誘ってお出かけしたいですが、みんなで休みを合わせないといけません。
子供を除いたお出かけに行くメンバーの数と、各メンバーの休みを取れる期間が与えられます。その中でメンバー全員に共通する日があれば "OK"、なければ "NG" と出力してください。

例)
お出かけのメンバー： 2人
父が休みを取れる期間： 16~19
母が休みを取れる期間： 14~17
→ OK (入力例 1)

お出かけのメンバー： 3人
母が休みを取れる期間： 22~23
祖父が休みを取れる期間： 17~20
祖母が休みを取れる期間： 14~19
→ NG (入力例 2)

この結果を図に示すと以下のようになります。

入力例1
2
16 19
14 17

出力例1
OK
"""

# 人数の受け取り
# MEMBERS =  int(input())

# # 処理
# periods = []
# for _ in range(MEMBERS):
#     start, end = map(int, input().split())
#     periods.append((start, end))
# print(periods) # [(16, 19), (14, 17)]
# # [(22, 23), (17, 20), (14, 19)]

test = [(18, 23), (17, 20), (14, 30)]


# 共通する日を探す
def has_common_day():
    # 最も遅い開始日
    latest_start = max(start for start, _ in test)
    print(latest_start)

    # 最も早い終了日
    earliest_end = min(end for _, end in test)
    print(earliest_end)

    # 共通期間があるかチェック
    ## 最も遅い開始日と最も早い終了日が重複していたらTrue
    return latest_start <= earliest_end


print("OK" if has_common_day() else "NG")


## 休みが重複している日を抽出する。
###  メンバー全員に共通する日があれば "OK"、なければ "NG"
# holidays = [int(i) for i in input().split()]
# print(holidays)

# start_holidays = [] # [16, 14]
# finish_holidays = [] # [19, 17]
# for i in range(MEMBERS):
#   holiday_start,holiday_finish = list(map(int,input().split()))
#   print(holiday_start)
#   print(holiday_finish)

#   start_holidays.append(holiday_start)
#   finish_holidays.append(holiday_finish)

# for i, x, y in enumerate(zip(start_holidays,finish_holidays)):
#   if range(x,y+1)
