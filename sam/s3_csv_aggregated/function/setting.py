"""変数、定数を定義するモジュール."""

import os
from datetime import date, datetime, timedelta, timezone
from logging import DEBUG, Formatter, StreamHandler, getLogger
from os.path import dirname, join
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

# タイムスタンプの生成
JST = timezone(timedelta(hours=+9), "JST")
TZ = ZoneInfo("Asia/Tokyo")
now = datetime.now(JST)
date_today = date.today()

# ログ定義
logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 標準出力
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)

# ロガーにハンドラーを追加
logger.addHandler(streamHandler)

# .envファイルの読み込み
dotenv_path = join(dirname(__file__), ".env")
if not load_dotenv(dotenv_path):
    logger.error("Failed to load environment variables from .env file")
elif not os.environ.get("DEFAULT_REGION_NAME"):
    logger.error("Required environment variable DEFAULT_REGION_NAME is not set")

# 定数の設定
DEFAULT_REGION_NAME = os.environ.get("DEFAULT_REGION_NAME")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE_NAME")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
S3_BUCKET_DST = os.environ.get("S3_BUCKET_DST")

# メールテンプレート
MAIL = {
    "subject": "CSV処理完了通知(Lambda)",
    "message": """
        CSVの処理が完了しました。
        処理日時: {datetime}
        S3バケット: {bucket}
        オブジェクト: {obj}
        """,
}
