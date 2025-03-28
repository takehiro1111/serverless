def notification_setting_diff_msg(src, dynamodb_key):
    return f"`{src}`: DynamoDBのKey(`{dynamodb_key}`)がアプリケーションログと一致しません。\n設定を見直してください。"


def notification_setting_empty_msg(src):
    return f"`{src}`: インフラの設定漏れです。DynamoDBにItemを設定してください。"
