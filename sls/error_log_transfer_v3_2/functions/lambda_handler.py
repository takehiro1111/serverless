"""S3イベントからエラーログを取得し解析するLambda関数.

S3バケットからログファイルを読み込み、条件に基づいて処理し、
必要に応じてSlack通知を行う.
"""

import gzip
import io

import boto3

from .logger import logger
from .notify_slack import NotifySlackManager
from .parse_log import LogParser
from .setting import ERRORS


def get_s3_data(bucket: str, key: str) -> list[str]:
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
    print(f"content: {content}")
    print("response", response)

    # ファイル名またはContent-Encodingからgzip圧縮を検出
    content_type_from_headers = (
        response.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("content-type")
    )
    is_gzipped = (
        key.endswith(".gz") or content_type_from_headers == "application/x-gzip"
    )

    if is_gzipped:
        # gzipファイルを解凍
        with gzip.GzipFile(fileobj=io.BytesIO(content), mode="rb") as f:
            content = f.read()

    print("デコード後", content.decode("utf-8", "ignore").splitlines())

    return content.decode("utf-8", "ignore").splitlines()


def lambda_handler(event, context) -> None:
    """Lambda関数のエントリポイント.

    S3イベントからログファイルを取得し、条件に基づいて解析・通知処理を行います.

    Args:
        event: S3トリガーイベント情報
        context: Lambda実行コンテキスト
    """
    for data in event["Records"]:
        s3_info = data["s3"]
        bucket = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]
        print("key:", key)

        # Firehoseから転送される際のアプリケーションごとのprefix
        src = key.split("/")[0]
        print("src:", src)
        # アプリケーションに関係ないデータを除外するために変数化.
        directory = key.split("/")[1]
        print("directory:", directory)

        if directory in ERRORS:
            continue
        # HBのようなイベントログは通知する必要がなく処理したくないため.
        elif "event-log" in src:
            break
        else:
            body = get_s3_data(bucket, key)

            # SLack通知のクラスのインスタンス化
            notify_slack_manager = NotifySlackManager()

            # ログの解析用メソッドを定義しているクラスをインスタンス化
            log_parser = LogParser(notify_slack_manager)

            # S3オブジェクトと一致するDynamoDBのデータを取得
            log_parser.get_dynamodb_item(src)

            # アプリケーションログとDynamoDBの情報を付け合わせして処理.
            log_parser.parse_application_log(src, body)
