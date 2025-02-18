"""This module sets up the configuration."""

import datetime
import json
import os

# AWSアカウントのsetting
# ローカルのパスではなくLambdaだと独自のパスになるため不要。
# file_path = os.path.join(os.path.dirname(__file__), "config.json")
with open("config.json") as accounts:
    config = json.load(accounts)

IAM_ROLE_NAME_MONITOR_ECS = config.get("DEFAULT_ROLE_NAME")
DEFAULT_REGION = os.environ.get("AWS_REGION")
ACCOUNTS = config.get("ACCOUNTS")

# SSMパラメータストア
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")

# 現在の日時を取得
day = datetime.datetime.now()
weekday = day.strftime("%a")
# 日付と曜日の表示形式を変更
day_format = day.strftime("%Y/%-m/%-d") + f"({weekday})"
