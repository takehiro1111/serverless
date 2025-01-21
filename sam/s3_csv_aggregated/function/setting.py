"""変数、定数を定義するモジュール."""

import os
from datetime import date, datetime, timedelta, timezone
from logging import DEBUG, Formatter, StreamHandler, getLogger
from os.path import dirname, join
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# 定数の設定
DEFAULT_REGION_NAME = os.environ.get("DEFAULT_REGION_NAME")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE_NAME")
SUBJECT = os.environ.get("MAIL")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
S3_BUCKET_DST = os.environ.get("S3_BUCKET_DST")

# タイムスタンプの生成
JST = timezone(timedelta(hours=+9), "JST")
TZ = ZoneInfo("Asia/Tokyo")
now = datetime.now(JST)
timestamp = now.isoformat()
d_today = date.today()

# ロギング
## ログ定義
logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

## 標準出力
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)

## ロガーにハンドラーを追加
logger.addHandler(streamHandler)


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
