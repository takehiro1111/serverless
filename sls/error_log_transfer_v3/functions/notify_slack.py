import json
import os

import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .logger import logger


class NotifySlackManager:
    def __init__(self):
        self._token = self.slack_bot_token

    @property
    def slack_bot_token(self):
        # botトークン取得
        stage = os.getenv("stage")
        ssm = boto3.client("ssm")
        params = {"Name": f"/stats/{stage}/slack/bot_token", "WithDecryption": True}
        ret = ssm.get_parameter(**params)
        SLACK_BOT_TOKEN = ret["Parameter"]["Value"]

        return SLACK_BOT_TOKEN

    @slack_bot_token.setter
    def slack_bot_token(self, value):
        self._token = value

    def notify_slack_template(self, channel_id, text):
        client = WebClient(token=self._token)
        try:
            client.chat_postMessage(channel=channel_id, text=text)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")

    def respond_to_slack(self, channel_id, json_data, notification_settings):
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

    # def respond_to_slack(self, container_name, channel_id, json_data, notification_settings):
    #     # Slack通知用のアタッチメントを構築
    #     attachment = self._build_notification_attachment(container_name, json_data, notification_settings)

    #     # Slack API を使用して送信
    #     self._send_slack_message(channel_id, attachment)

    # def _build_notification_attachment(self, container_name, json_data, notification_settings):
    #     message_field = json_data.get("message", None)

    #     # アタッチメントの基本構造を作成
    #     attachment_main = {
    #         "color": "FFC859",
    #         "title": "Error Log Notification",
    #         "fields": []
    #     }

    #     timestamp = json_data.get("timestamp", "Unknown Timestamp")
    #     container_name = json_data.get("container_name", "Unknown Container Name")

    #     # 基本情報を追加
    #     attachment_main["fields"].append([
    #         {"title": "Timestamp", "value": timestamp, "short": False},
    #         {"title": "ContainerName", "value": container_name, "short": False}
    #     ])

    #     # 通知対象のフィールドを追加
    #     added_fields = self._add_notification_fields(attachment_main, json_data, notification_settings)

    #     # メッセージフィールドの処理
    #     if message_field and "message" not in added_fields:
    #         attachment_main["fields"].append(
    #             {"title": "Message", "value": message_field, "short": False}
    #         )
    #     elif not message_field and not attachment_main["fields"]:
    #         # メッセージがなく、他のフィールドもない場合はログ全体を表示
    #         full_log = json.dumps(json_data, indent=4)
    #         attachment_main["fields"].append(
    #             {"title": "Full Log", "value": full_log, "short": False}
    #         )

    #     return [attachment_main]

    # def _add_notification_fields(self, attachment, json_data, notification_settings):
    #     # 通知設定に基づくフィールドを追加
    #     added_fields = set()
    #     for setting in notification_settings:
    #         for key, value in setting.items():
    #             if key not in added_fields:
    #                 added_fields.add(key)
    #                 field_value = json_data.get(key, f"Unknown {key.capitalize()}")
    #                 attachment["fields"].append(
    #                     {"title": key.capitalize(), "value": field_value, "short": False}
    #                 )
    #     return added_fields

    # def _send_slack_message(self, channel_id, attachments):
    #     # Slackメッセージ送信
    #     attachment_body = json.dumps(attachments)
    #     client = WebClient(token=self._token)
    #     try:
    #         client.chat_postMessage(channel=channel_id, attachments=attachment_body)
    #     except SlackApiError as e:
    #         logger.error(f"Error posting message: {e}")
