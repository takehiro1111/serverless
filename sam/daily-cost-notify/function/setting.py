import datetime

import holidays

# Get date for slack notification
today = datetime.datetime.now()
weekday = today.strftime("%a")
day_format = today.strftime("%Y/%-m/%-d") + f"({weekday})"

# 日本の祝日カレンダーを作成
jp_holidays = holidays.Japan()
print()

# 特定の日が祝日かどうかを判定
is_holiday = datetime.date(today.year, today.month, today.day) in jp_holidays
