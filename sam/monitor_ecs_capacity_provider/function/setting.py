"""This module sets up the configuration."""

import datetime
import os

import holidays
import yaml

# config
with open("accounts.yaml") as accounts:
    config = yaml.safe_load(accounts)

ACCOUNTS = config.get("accounts", [])
IAM_ROLE_NAME_MONITOR_ECS = "monitor-ecs-service-capacity-provider"


# environment variables
DEFAULT_REGION = os.environ.get("AWS_REGION")
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")

# Get date for slack notification
today = datetime.datetime.now()
weekday = today.strftime("%a")
day_format = today.strftime("%Y/%-m/%-d") + f"({weekday})"

# 日本の祝日カレンダーを作成
jp_holidays = holidays.Japan()

# 特定の日が祝日かどうかを判定
is_holiday = datetime.date(today.year, today.month, today.day) in jp_holidays
