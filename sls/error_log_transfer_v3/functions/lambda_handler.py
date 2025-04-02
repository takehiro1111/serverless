import boto3

from .notify_slack import NotifySlackManager
from .parse_log import LogParser
from .setting import ERRORS


def get_s3_data(bucket, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8", "ignore").splitlines()


def lambda_handler(event, context):
    for data in event["Records"]:
        s3_info = data["s3"]
        bucket = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]
        print("key:", key)

        # Firehoseから転送される際のアプリケーションごとのprefix
        src = key.split("/")[0]
        print("src:", src)
        # アプリケーションに関係ないデータを除外するために変数化。
        directory = key.split("/")[1]
        print("directory:", directory)

        if directory in ERRORS:
            continue
        # HBのようなイベントログは通知する必要がなく処理したくないため。
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
            # アプリケーションログとDynamoDBの情報を付け合わせして処理。
            log_parser.parse_application_log(src, body)
