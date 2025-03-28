import json
import logging
import os
import re

import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ロガーの設定>
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for data in event["Records"]:
        s3_info = data["s3"]
        bucket = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]

        src = key.split("/")[0]
        directory = key.split("/")[1]
        if directory in ["errors", "error", "manifests"]:
            continue
        else:
            body = get_s3_data(bucket, key)
            process_logs(src, body)

    return


def process_logs(src, body):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("error_logtransfer_v3")
    response = table.get_item(Key={"src": src})

    # item を初期化
    item = {}

    if "Item" in response:
        item = response["Item"]
    else:
        logger.info("srcにマッチするデータが存在しません。DynamoDBを確認してください。")
        return

    notification_settings = item.get("notification_setting", [])
    blacklist_regexp = item.get("blacklist", None)
    channel_id = item.get("channel_id")

    for line in body:
        try:
            json_data = json.loads(line)
            container_name = json_data.get("container_name", "")
        except json.JSONDecodeError:
            continue  # JSON形式でない場合は次の行へ

        if check_notification_conditions(json_data, notification_settings):
            if not is_blacklisted(json_data, blacklist_regexp):
                if channel_id:
                    respond_to_slack(
                        container_name, channel_id, json_data, notification_settings
                    )
                else:
                    logger.info("SlackチャンネルIDが見つかりません。")


def check_notification_conditions(json_data, notification_settings):
    for setting in notification_settings:
        for key, value in setting.items():
            # JSONデータにキーが存在し、値が部分一致するかチェック（大文字小文字を区別しない）
            if (
                key.lower() in (k.lower() for k in json_data)
                and value.lower() in json_data[key].lower()
            ):
                return True
    return False  # どの条件も一致しなかった


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
        logging.error(f"Error posting message: {e}")


def get_s3_data(bucket, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8", "ignore").splitlines()
