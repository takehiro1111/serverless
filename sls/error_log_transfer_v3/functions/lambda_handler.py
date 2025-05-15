"""S3イベントからエラーログを取得し解析するLambda関数.

S3バケットからログファイルを読み込み、条件に基づいて処理し、
必要に応じてSlack通知を行う.
"""

import gzip
import io
from typing import Any

import boto3

from .notify_slack import NotifySlackManager
from .parse_log import LogParser
from .setting import IGNORE_DIRS


def get_s3_data(bucket: str, key: str) -> Any:
    """S3バケットからデータを取得して行単位のリストとして返す.

    Args:
        bucket: S3バケット名
        key: S3オブジェクトキー

    Returns:
        取得したデータを行ごとに分割したリスト
    """
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read()

    # ファイル名またはContent-Encodingからgzip圧縮を検出
    is_gzipped = key.endswith(".gz") or response.get("ContentEncoding") == "gzip"

    if is_gzipped:
        # gzipファイルを解凍
        with gzip.GzipFile(fileobj=io.BytesIO(content), mode="rb") as f:
            content = f.read()

    return content.decode("utf-8", "ignore").splitlines()


def lambda_handler(event, context) -> None:
    """Lambda関数のエントリポイント.

    S3イベントからログファイルを取得し、条件に基づいて解析・通知処理を行います.

    Args:
        event: S3トリガーイベント情報
        context: Lambda実行コンテキスト
    """
    if "detail" in event:
        bucket = event["detail"]["bucket"]["name"]
        key = event["detail"]["object"]["key"]

        # Firehoseから転送される際のアプリケーションごとのprefix
        src = key.split("/")[0]

        # アプリケーションに関係ないデータを除外するために変数化.
        directory = key.split("/")[1]

        if directory in IGNORE_DIRS:
            return
        # HBのようなイベントログは通知する必要がなく処理したくないため.
        elif "event-log" in src:
            return

        body = get_s3_data(bucket, key)

        # SLack通知のクラスのインスタンス化
        notify_slack_manager = NotifySlackManager()

        # ログの解析用メソッドを定義しているクラスをインスタンス化
        log_parser = LogParser(notify_slack_manager)

        # S3オブジェクトと一致するDynamoDBのデータを取得
        log_parser.get_dynamodb_item(src)

        # アプリケーションログとDynamoDBの情報を付け合わせして処理.
        log_parser.parse_application_log(src, body)
