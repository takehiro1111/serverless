"""変数、定数を定義するモジュール."""

import configparser
import os
from datetime import datetime, timedelta, timezone

# AWSリージョン名の取得
config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
DEFAULT_REGION = config_ini["DEFAULT"]["DEFAULT_REGION"]

# タイムスタンプの生成
JST = timezone(timedelta(hours=+9), "JST")
now = datetime.now(JST)
timestamp = now.isoformat()

# 定数
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE_NAME")
