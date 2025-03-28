import json
import os
import re

import boto3
import logger
from logger import logger
from setting import notification_setting_diff_msg, notification_setting_empty_msg
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def lambda_handler(event, context):
    for data in event["Records"]:
        s3_info = data["s3"]
        bucket = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]
        print("key:", key)

        src = key.split("/")[0]
        print("src:", src)
        directory = key.split("/")[1]
        print("directory:", directory)

        if directory in ["errors", "error", "manifests"]:
            continue
        elif "event-log" in src:
            break
        else:
            body = get_s3_data(bucket, key)
            process_logs(src, body)

    return


# item: {'blacklist': ['INFO'], 'src': 'test-error-logtransfer',
#         'notification_setting': [{'level': 'error'}], 'channel_id': 'C02PY437UM6'}


def process_logs(src, body):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("error_logtransfer_v3")
    response = table.get_item(Key={"src": src})
    print("response:", response)

    # item を初期化
    item = {}

    if "Item" in response:
        item = response["Item"]
        print("item:", item)
    else:
        logger.info("srcにマッチするデータが存在しません。DynamoDBを確認してください。")
        # そもそもDynamoDBにsrcが存在しない場合の検知用通知のチャンネルIDは別で持つ必要がある。
        # チャンネルIDは変数化する
        dynamodb_empty_mesg = notification_setting_empty_msg(src)
        notify_slack_template("", dynamodb_empty_mesg)
        return

    notification_settings = item.get("notification_setting", [])
    blacklist_regexp = item.get("blacklist", None)
    channel_id = item.get("channel_id")

    # フラグを初期化
    diff_key_notified = False

    # notification_settingのlist[dict]からkeyを取得。
    for notification_setting in notification_settings:
        dynamodb_key = list(notification_setting.keys())[0]

    print("notification_settings:", notification_settings)

    for line in body:
        try:
            # S3から取得するログデータをJSON形式に変換
            # 例外処理を追加して、JSON形式でない場合はスキップ
            json_data = json.loads(line)
            print("json_data:", json_data)
            container_name = json_data.get("container_name", "")
            print("container_name:", container_name)
        except json.JSONDecodeError:
            continue  # JSON形式でない場合は次の行へ

        check_notification_setting = check_notification_conditions(
            json_data, notification_settings
        )

        if check_notification_setting:
            if not is_blacklisted(json_data, blacklist_regexp):
                if channel_id:
                    respond_to_slack(
                        container_name, channel_id, json_data, notification_settings
                    )
                else:
                    logger.info("SlackチャンネルIDが見つかりません。")
        elif check_notification_setting is False:
            if channel_id and diff_key_notified is False:
                dynamo_key_diff_msg = notification_setting_diff_msg(src, dynamodb_key)
                notify_slack_template(channel_id, dynamo_key_diff_msg)
                # ループの影響で通知が重複しないようにする。
                diff_key_notified = True
            else:
                logger.info("SlackチャンネルIDが見つかりません。")
        else:
            logger.info("エラーではないログです。")
            continue


def get_slack_bot_token():
    # botトークン取得
    stage = os.getenv("stage")
    ssm = boto3.client("ssm")
    params = {"Name": f"/stats/{stage}/slack/bot_token", "WithDecryption": True}
    ret = ssm.get_parameter(**params)
    SLACK_BOT_TOKEN = ret["Parameter"]["Value"]

    return SLACK_BOT_TOKEN


def notify_slack_template(channel_id, text):
    # Slack接続
    client = WebClient(token=get_slack_bot_token())
    try:
        client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


# json_data: {
#             '@timestamp': '2025-03-27T10:50:34.548+09:00', 'log': 'WARN', 'message': 'Not found: /favicon.ico',
#             'timestamp': '2025-03-27T10:50:34.548+09:00', 'type': 'applog',
#             'url': 'https://stg.student.hoikushibank.com/favicon.ico',
#             'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
#             'Chrome/123.0.0.0 Safari/537.36', 'source': 'stdout', 'container_id': '7a925a6dfb5d42b6b9ea9243e05a80ec-0813150757',
#             'container_name': 'hb-stu-v2-web-stg', 'ecs_cluster': 'hb-stu-stg',
#             'ecs_task_arn': 'arn:aws:ecs:ap-northeast-1:749918949857:task/hb-stu-stg/7a925a6dfb5d42b6b9ea9243e05a80ec',
#             'ecs_task_definition': 'hb-stu-v2-web-stg:184'
#           }


# notification_settings: [{'level': 'error'}]


# DYnamoDBのnotification_settingのkeyが一致するか確認。
def check_notification_conditions(json_data, notification_settings):
    for setting in notification_settings:
        for key, value in setting.items():

            # ログの重要度を示す値のキーがDynamoDBで設定しているキーと一致しているか
            if key in json_data.keys():
                has_key = key.lower() in (k.lower() for k in json_data)
                has_value = value.lower() in json_data[key].lower()

                if has_key and has_value:
                    return True

            elif key not in json_data.keys():
                return False  # キーが存在しない場合はFalseを返す

    return None  # どの条件も一致しなかった


def is_blacklisted(json_data, blacklist_regexp):
    if blacklist_regexp:
        for keyword in blacklist_regexp:
            if re.compile(keyword).search(str(json_data)):
                print("以下文字列がblacklistにHIT（通知しない）: " + keyword)
                return True
    return False


def respond_to_slack(container_name, channel_id, json_data, notification_settings):
    # 'message'フィールドの確認
    message_field = json_data.get("message", None)

    # Slack通知用のメッセージを構築
    attachment_main = {
        "color": "FFC859",
        "title": "Error Log Notification",
        "fields": [],
    }

    if message_field:
        # 'message'フィールドがある場合
        timestamp = json_data.get("timestamp", "Unknown Timestamp")
        container_name = json_data.get("container_name", "Unknown Container Name")

        attachment_main["fields"].append(
            {"title": "Timestamp", "value": timestamp, "short": False}
        )

        attachment_main["fields"].append(
            {"title": "ContainerName", "value": container_name, "short": False}
        )

        # notification_settingsから特定のフィールドを取得
        added_fields = set()  # 重複を避けるために追加されたフィールドを記録
        for setting in notification_settings:
            for key, value in setting.items():
                if key not in added_fields:  # 重複を避ける
                    added_fields.add(key)
                    value = json_data.get(key, f"Unknown {key.capitalize()}")
                    attachment_main["fields"].append(
                        {"title": key.capitalize(), "value": value, "short": False}
                    )

        # 'message'フィールドが重複していない場合のみ追加
        if "message" not in added_fields:
            attachment_main["fields"].append(
                {"title": "Message", "value": message_field, "short": False}
            )

    else:
        # 'message'フィールドがない場合、ログの全文を含める
        full_log = json.dumps(json_data, indent=4)
        attachment_main["fields"].append(
            {"title": "Full Log", "value": full_log, "short": False}
        )

    attachment_body = json.dumps([attachment_main])

    # botトークン取得
    stage = os.getenv("stage")
    ssm = boto3.client("ssm")
    params = {"Name": f"/stats/{stage}/slack/bot_token", "WithDecryption": True}
    ret = ssm.get_parameter(**params)
    SLACK_BOT_TOKEN = ret["Parameter"]["Value"]

    # Slack接続
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        client.chat_postMessage(channel=channel_id, attachments=attachment_body)
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def get_s3_data(bucket, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8", "ignore").splitlines()
