import os
from datetime import datetime, timedelta, timezone

import holidays

SLACK_BOT_TOKEN = os.environ.get("SSM_PARAMETER_NAME")
NOTIFY_SLACK_CHANNEL = "#dev-sre-internal"

today = datetime.now()
jp_holidays = holidays.Japan()

# 特定の日が祝日かどうかを判定
is_holiday = today.date() in jp_holidays


# 月初と翌日の日付を取得
now = datetime.now(timezone.utc)
start_date = now.replace(day=1).strftime("%Y-%m-%d")
tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

# 今日の日付抽出
now_date = now.strftime("%d")
has_int_now_date = int(now_date)

# 通知表示用の日付
NOTIFY_START_DATE = now.replace(day=1).strftime("%-m/%-d")
NOTIFY_END_DATE = now.strftime("%-m/%-d")

# 前月の月の数字を取得
LAST_MONTH = (now.month - 1) if now.month > 1 else 12


# 前月の1日を取得
def _get_last_month_dates():
    if today.month == 1:
        last_month_start = datetime(today.year - 1, 12, 1)
        last_month_end = datetime(today.year, 1, 1)
    else:
        last_month_start = datetime(today.year, today.month - 1, 1)
        last_month_end = datetime(today.year, today.month, 1)

    # 文字列形式に変換（YYYY-MM-DD）
    start_date_str = last_month_start.strftime("%Y-%m-%d")
    end_date_str = last_month_end.strftime("%Y-%m-%d")
    return start_date_str, end_date_str


last_start_date, last_end_date = _get_last_month_dates()
