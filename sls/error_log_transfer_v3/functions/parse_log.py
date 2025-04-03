import json
import re

import boto3

from .logger import logger
from .notify_slack import NotifySlackManager
from .setting import (
    SLACK_CHANNEL_ID_SRE_LAMBDA,
    notification_setting_diff_msg,
    notification_setting_empty_msg,
)


class LogParser:
    def __init__(self, notify_slack_manager: NotifySlackManager):
        self.dynamodb = boto3.resource("dynamodb")
        self.item = {}
        self.notify_slack_manager = notify_slack_manager
        self.diff_key_flag = False
        self.empty_item_flag = False
        self.notification_setting_key = None
        self._conteinr_name = None
        self.processed_messages = set()

    # DynamoDBテーブル側の情報を取得
    def get_dynamodb_item(self, src):
        table = self.dynamodb.Table("error_logtransfer_v3")
        response = table.get_item(Key={"src": src})

        if "Item" in response:
            self.item = response["Item"]
            print("item:", self.item)
            return self.item
        else:
            logger.info(
                "srcにマッチするデータが存在しません。DynamoDBを確認してください。"
            )
            if self.empty_item_flag == False:
                dynamodb_empty_msg = notification_setting_empty_msg(src)
                self.notify_slack_manager.notify_slack_infra_mistakes(
                    SLACK_CHANNEL_ID_SRE_LAMBDA, dynamodb_empty_msg
                )
                # DynamoDBが空の場合の通知は1回のみにしたいためのフラグ処理。
                self.empty_item_flag = True
            return None

    # DynamoDBの`notification_setting`のkey情報を取得
    def _get_notification_setting_key(self, notification_settings):
        if not notification_settings:
            logger.warning("notification_settingsのリストが空です")
            return None

        for notification_setting in notification_settings:
            if notification_setting:
                self.notification_setting_key = list(notification_setting.keys())[0]
                break

        return self.notification_setting_key

    def parse_application_log(self, src, body):
        notification_settings = self.item.get("notification_setting", [])
        blacklist_regexp = self.item.get("blacklist", None)
        channel_id = self.item.get("channel_id")

        # notification_settingのlist[dict]からkeyを取得。
        self._get_notification_setting_key(notification_settings)

        for line in body:
            try:
                # S3から取得するログデータをJSON形式に変換
                # 例外処理を追加して、JSON形式でない場合はスキップ
                json_data = json.loads(line)
                print("json_data:", json_data)
                container_name = json_data.get("container_name", "")
                self._conteinr_name = container_name
                print("container_name:", container_name)

                message = json_data.get("message", "")
                timestamp = json_data.get("timestamp", json_data.get("@timestamp", ""))
                message_key = f"{message}_{timestamp}"

                # 重複しないよう、同一のTimeStampとMessageで既に処理したメッセージならスキップ
                if message_key in self.processed_messages:
                    continue

                self.processed_messages.add(message_key)

            except json.JSONDecodeError:
                continue  # JSON形式でない場合は次の行へ

            # ログのバリデーション処理
            validator = LogValidation(
                json_data,
                notification_settings,
                blacklist_regexp,
                channel_id,
                self.notify_slack_manager,
            )
            result_flag = validator.validate_log_and_notify(
                container_name, self.diff_key_flag, src, self.notification_setting_key
            )

            # DynamoDBが空の場合の通知は1回のみにしたいためのフラグ処理。
            if result_flag is not None:
                self.diff_key_flag = True


class BaseValidation:
    def __init__(self, json_data, notification_settings, blacklist_regexp, channel_id):
        self.json_data = json_data
        self.notification_settings = notification_settings
        self.blacklist_regexp = blacklist_regexp
        self.channel_id = channel_id

    # DynamoDBの`notification_setting`のkeyが一致するか確認。
    def check_notification_settings(self):
        for setting in self.notification_settings:
            for key, value in setting.items():
                # ログの重要度を示す値のキーがDynamoDBで設定しているキーと一致しているか
                # 簡略化できないか要確認。
                if key in self.json_data.keys():
                    has_key = key.lower() in (k.lower() for k in self.json_data)
                    has_value = value.lower() in self.json_data[key].lower()

                    if has_key and has_value:
                        return True

                # キーが存在しない場合はFalseを返して設定に不備があることを通知する。
                elif key not in self.json_data.keys():
                    return False

        # どの条件も一致しない場合はNoneを返す。
        return None

    def check_blacklisted(self):
        if self.blacklist_regexp:
            for ignore_keyword in self.blacklist_regexp:
                # S3オブジェクトに入るログのJsonデータの中にblacklistとして指定した文字列が含まれるか確認。
                if re.compile(ignore_keyword).search(str(self.json_data)):
                    print("以下文字列がblacklistにHIT（通知しない）: " + ignore_keyword)
                    return True
        return False


class LogValidation(BaseValidation):
    def __init__(
        self,
        json_data,
        notification_settings,
        blacklist_regexp,
        channel_id,
        notify_slack_manager,
    ):
        super().__init__(json_data, notification_settings, blacklist_regexp, channel_id)
        self.notify_slack_manager = notify_slack_manager

    def validate_log_and_notify(self, container_name, diff_key_flag, src, dynamodb_key):
        check_notification_setting = self.check_notification_settings()
        print(f"※※チャンネルIDが見つからないと警告される件:{self.channel_id}")
        print(f"diff_key_flagの中身:{diff_key_flag}")

        if check_notification_setting and self.json_data.get("message"):
            if not self.check_blacklisted():
                if self.channel_id:
                    self.notify_slack_manager.notify_slack_app_err_msg(
                        container_name,
                        self.channel_id,
                        self.json_data,
                        self.notification_settings,
                    )
                else:
                    logger.info("SlackチャンネルIDが見つかりません。(True)")
        elif check_notification_setting is False and self.json_data.get("message"):
            if self.channel_id and diff_key_flag is False:
                dynamo_key_diff_msg = notification_setting_diff_msg(src, dynamodb_key)
                self.notify_slack_manager.notify_slack_infra_mistakes(
                    self.channel_id, dynamo_key_diff_msg
                )
                # ループの影響で通知が重複しないようにする。
                return True
            else:
                logger.info("SlackチャンネルIDが見つかりません。(False)")
        else:
            logger.info("エラーではないログデータです。")

        return None
