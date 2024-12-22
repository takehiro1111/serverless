import datetime
import zoneinfo

# UTC = datetime.timezone.utc
JST = datetime.timezone(datetime.timedelta(hours=9), name="JST")

now = datetime.datetime.now(JST)
# print(now) # 2024-12-21 13:53:44.904444 ※実行時の数値
# print(now.isoformat())
# print(now.strftime('%Y/%m/%d-%H:%M:%S'))

# # JST（日本標準時）を定義（UTC+9時間）


# # 現在の日時をJSTで取得
now_jst = datetime.datetime.now(JST)
print(now_jst)
print(now_jst.strftime('%Y/%m/%d-%H:%M:%S%X')) 

TZ = zoneinfo.ZoneInfo("Asia/Tokyo")
# date_time = datetime.datetime(year=2024, month=12, day=21, hour=9,minute=3,second=5,microsecond=10,tzinfo=TZ)
# print(date_time.strftime('%Y/%m/%d-%p%H:%M:%S:%f(%Z)'))
# print(date_time.strptime('%Y/%m/%d-%p%H:%M:%S:%f(%Z)'))

# time = datetime.time(hour=9,minute=3,second=5,microsecond=10,tzinfo=TZ)
# print(time)

# date = datetime.date(year=2024,month=12,day=21)
# print(date.strftime('%Y/%m/%d'))


# 現在の日付と時間
# now = datetime.datetime.now()
# print("現在の日時:", now)

# # 5日後の日時
# future_date = now + datetime.timedelta(days=5)
# print("5日後の日時:", future_date)

# # 3日前の日時
# past_date = now - datetime.timedelta(days=3)
# print("3日前の日時:", past_date)

# date_str = '2024/12/21 15:30:45'

# # 文字列を解析してdatetimeオブジェクトに変換
# parsed_date = datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
# print(f"strptime の結果: {parsed_date}")  # 例: 2024-04-27 15:30:45

# # 二つの日付の差を計算
# date1 = datetime.datetime(2024, 12, 21, 12, 0, 0)
# date2 = datetime.datetime(2024, 12, 25, 18, 30, 0)

# # Pythonが内部でtimedeltaを生成して差を表現している。
# delta = date2 - date1
# print(f"日数: {delta.days} 日")  # 日数: 4 日
# print(f"総秒数: {delta.total_seconds()} 秒")  # 総秒数: 384600.0 秒
