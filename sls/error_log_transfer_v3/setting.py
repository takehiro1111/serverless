ERROR_MESG = {
    "empty_notification_settings": "`notification_setting`が空です。DynamoDBにItemを設定してください。",
}


def notification_setting_diff_msg(src, key):
    return f"`{src}`: DynamoDBのKeyがアプリケーションログ(`{key}`)と一致しません。"
