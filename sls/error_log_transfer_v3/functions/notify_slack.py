import json
import os

import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .logger import logger
from .setting import TITLE_COLOR_CODE


class NotifySlackManager:
    def __init__(self):
        self._token = self.slack_bot_token
        self._attachment_main = None
        self._attachment_detail = None
        self._thread_message = None

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

    def _build_notification_attachment(self, container_name, json_data, notification_settings):
        # アタッチメントの基本構造を作成
        self._attachment_main = {
            "color": TITLE_COLOR_CODE,
            "title": container_name,
        }
        self._attachment_detail = {
            "fields": []
        }
        self._thread_message = {
            "fields": []
        }

        message_field = json_data.get("message", None)
        if message_field:
            timestamp = json_data.get("timestamp", json_data.get("@timestamp", "Unknown Timestamp"))
            stack_trace = json_data.get("stack_trace", json_data.get("stacktrace", json_data.get("stack", "")))
            logger = json_data.get("logger_name", json_data.get("loggername", json_data.get("logger", "")))

            # TimeStampqを追加
            self._attachment_detail["fields"].append({
                "title": "Timestamp",
                "value": timestamp,
                "short": True
            })

            print("timestamp(_build_notification_attachment):", timestamp)

            # 通知対象のフィールドを追加
            added_fields = self._add_notification_fields(self._attachment_detail, json_data, notification_settings)

            # logger_nameが存在する場合追加、存在しない場合は追加しない
            if logger and "logger_name" not in added_fields:
                self._attachment_detail["fields"].append({
                    "title": "Logger Name",
                    "value": logger,
                    "short": True
                })
            # "message"フィールドが重複していない場合のみ追加
            if "message" not in added_fields:
                self._attachment_detail["fields"].append({
                    "title": "Message",
                    "value": message_field,
                    "short": False
                })



            # stack_traceが存在する場合追加、存在しない場合は追加しない
            if stack_trace:
                self._thread_message["fields"].append({
                    "title": "Stack Trace",
                    "value": stack_trace,
                    "short": False
                })

        else:
            # "message"フィールドがない場合、ログの全文を含める
            full_log = json.dumps(json_data, indent=4)
            self._attachment_main["fields"].append(
                {"title": "Full Log", "value": full_log, "short": False}
            )

        print(f"_build_notification_attachment:{self._attachment_detail["fields"]}")


    def _add_notification_fields(self, attachment, json_data, notification_settings):
        # 通知設定に基づくフィールドを追加
        added_fields = set()
        for setting in notification_settings:
            for key, value in setting.items():
                if key not in added_fields:
                    print(f"_add_notification_fields(Before):{attachment["fields"]}")
                    added_fields.add(key)
                    field_value = json_data.get(key, f"Unknown {key.capitalize()}")
                    attachment["fields"].append(
                        {"title": key.capitalize(), "value": field_value, "short": True}
                    )
        print(f"_add_notification_fields(After):{attachment["fields"]}")
        print(f"added_fields:{added_fields}")
        return added_fields

    def _send_slack_message(self, channel_id):
        client = WebClient(token=self._token)
        try:
            # メインメッセージを送信
            attachment_body = json.dumps([self._attachment_main, self._attachment_detail])
            main_massage = client.chat_postMessage(channel=channel_id, attachments=attachment_body)
            print("main_massage:", main_massage)
            # スレッドのタイムスタンプを取得
            # thread_bodys: [{"fields": []}]
            print("self._thread_message:", self._thread_message)
            thread_bodys = json.dumps([self._thread_message])
            print("thread_bodys:", thread_bodys)

            # スタックトレースのデータが存在する場合のみスレッドに通知する。
            if self._thread_message["fields"]:
                thread_ts = main_massage["ts"] if main_massage else None
                # スレッドにスタックトレースを送信
                client.chat_postMessage(channel=channel_id, attachments=thread_bodys, thread_ts=thread_ts)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")


    # 通知の実行メソッド
    def notify_slack_app_err_msg(self, container_name, channel_id, json_data, notification_settings):
        # Slack通知用のアタッチメントを構築
        self._build_notification_attachment(container_name, json_data, notification_settings)

        # Slack API を使用して送信
        self._send_slack_message(channel_id)

    def notify_slack_infra_mistakes(self, channel_id, attachment_body):
        client = WebClient(token=self._token)
        try:
            client.chat_postMessage(channel=channel_id, text=attachment_body)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
