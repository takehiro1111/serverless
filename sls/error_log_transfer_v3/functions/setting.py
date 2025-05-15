"""config関連のモジュール.

エラーログ転送処理に関する各種設定値と通知メッセージテンプレートを提供する.
"""

import os


def notification_setting_diff_msg(src: str, dynamodb_key: str) -> str:
    """DynamoDBのキーとアプリケーションログのキーが不一致の場合の通知メッセージ.

    Args:
        src: アプリケーション識別子
        dynamodb_key: DynamoDBのキー

    Returns:
        不一致を示す通知メッセージ
    """
    return f"`{src}`: DynamoDBのKey(`{dynamodb_key}`)がアプリケーションログと一致しません.\n設定を見直してください."


def notification_setting_empty_msg(src: str) -> str:
    """DynamoDBに設定漏れがある際の通知メッセージ.

    Args:
        src: アプリケーション識別子

    Returns:
        設定不足を示す通知メッセージ
    """
    return f"`{src}`: インフラの設定漏れです.DynamoDBにItemを設定してください."


# Config
ERRORS: list[str] = ["errors", "error", "manifests"]
SLACK_CHANNEL_ID_SRE_LAMBDA = "C07EFGAE81J"
TITLE_COLOR_CODE = "FFC859"
ENV = os.getenv("stage")
