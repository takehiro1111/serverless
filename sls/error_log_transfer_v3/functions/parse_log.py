import json
import re

import boto3

from .logger import logger
from .notify_slack import NotifySlackManager
from .setting import (
    PROD_SRE_LAMBDA,
    notification_setting_diff_msg,
    notification_setting_empty_msg,
)

# item: {'blacklist': ['INFO'], 'src': 'test-error-logtransfer',
#         'notification_setting': [{'level': 'error'}], 'channel_id': 'C02PY437UM6'}

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


class LogParser:
    def __init__(self, notify_slack_manager: NotifySlackManager):
        self.dynamodb = boto3.resource("dynamodb")
        self.item = {}
        self.notify_slack_manager = notify_slack_manager
        self.diff_key_flag = False
        self.empty_item_flag = False
        self.notification_setting_key = None

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
                self.notify_slack_manager.notify_slack_template(
                    PROD_SRE_LAMBDA, dynamodb_empty_msg
                )
                self.empty_item_flag = True
            return None

    # DynamoDBの`notification_setting`のkey情報を取得
    def get_notification_setting_key(self, notification_settings):
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
        self.get_notification_setting_key(notification_settings)

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

            # ログのバリデーション処理
            validator = LogValidation(
                json_data, notification_settings, blacklist_regexp, channel_id
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
                ##簡略化できないか要確認。
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
    def __init__(self, json_data, notification_settings, blacklist_regexp, channel_id):
        super().__init__(json_data, notification_settings, blacklist_regexp, channel_id)
        self.notify_slack_manager = NotifySlackManager()

    def validate_log_and_notify(self, container_name, diff_key_flag, src, dynamodb_key):
        check_notification_setting = self.check_notification_settings()
        print(f"※※チャンネルIDが見つからないと警告される件:{self.channel_id}")
        print(f"diff_key_flagの中身:{diff_key_flag}")

        if check_notification_setting:
            if not self.check_blacklisted():
                if self.channel_id:
                    self.notify_slack_manager.respond_to_slack(
                        self.channel_id, self.json_data, self.notification_settings
                    )
                else:
                    logger.error("SlackチャンネルIDが見つかりません。(True)")
        elif check_notification_setting is False:
            if self.channel_id and diff_key_flag is False:
                dynamo_key_diff_msg = notification_setting_diff_msg(src, dynamodb_key)
                self.notify_slack_manager.notify_slack_template(
                    self.channel_id, dynamo_key_diff_msg
                )
                # ループの影響で通知が重複しないようにする。
                return True
            else:
                logger.error("SlackチャンネルIDが見つかりません。(False)")
        else:
            logger.info("エラーではないログです。")

        return None
