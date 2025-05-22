"""変数、定数を定義するモジュール."""

import os
from datetime import datetime, timedelta, timezone
from os.path import dirname, join

from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# 定数の設定
DEFAULT_REGION_NAME = os.environ.get("DEFAULT_REGION_NAME")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE_NAME")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# タイムスタンプの生成
JST = timezone(timedelta(hours=+9), "JST")
now = datetime.now(JST)
timestamp = now.isoformat()
