import os
from datetime import datetime, timedelta, timezone

import holidays

SLACK_WEBHOOK_URL = os.environ.get("SSM_PARAMETER_NAME")

today = datetime.now()
# weekday = today.strftime("%a")
# day_format = today.strftime("%Y/%-m/%-d") + f"({weekday})"

jp_holidays = holidays.Japan()

# 特定の日が祝日かどうかを判定
is_holiday = today.date() in jp_holidays


now = datetime.now(timezone.utc)

# 月初の日付を取得（例: 2024-08-01）
start_date = now.replace(day=1).strftime("%Y-%m-%d")
print(start_date)

# 現在の日付と時刻を取得（例: 2024-08-24）
tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
print(tomorrow)
