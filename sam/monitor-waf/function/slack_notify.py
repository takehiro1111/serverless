import datetime

import boto3
import requests


def get_ssm_parameter() -> str:
    """
    SSMパラメータに格納しているWebHookのURLを取得
    """
    try:
        ssm = boto3.client("ssm", "ap-northeast-1")
        response = ssm.get_parameter(
            Name="/serverless/monitor-waf/SLACK_WEBHOOK_URL",
            WithDecryption=True,
        )
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound:
        raise ValueError("SSM parameter not found.")

    except ssm.exceptions.ParameterVersionNotFound:
        raise ValueError("SSM parameter version not found.")

    except Exception as e:
        raise ValueError(f"Failed to get SSM parameter: {e}")


def monitor_result_slack_notification(missing_rule_accounts):
    """
    RegionalLimitのルールが設定されていない場合は、日次でSlack通知を行う。
    """
    try:
        slack_webhook_url = get_ssm_parameter()
        # 現在の日時を取得
        day = datetime.datetime.now()
        weekday = day.strftime("%a")

        # 日付と曜日の表示形式を変更
        date_str = day.strftime("%Y/%-m/%-d") + f"({weekday})"

        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{date_str}*\n\n*:rotating_light: WebACL RegionalLimit are not enabled*",
                    },
                },
                {"type": "divider"},
            ]
        }

        for rule in missing_rule_accounts:
            result_message["blocks"].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Account:* `{rule['account_name']}` / *ID:* `{rule['account_id']}` / *WebACL:* `{rule['web_acl_name']}`",
                    },
                }
            )
        response = requests.post(
            slack_webhook_url,
            json=result_message,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Slack returned an error: {e}")


def error_result_slack_notification():
    """
    WAFの処理が何らかの理由でエラーになった場合のSlack通知する。
    """
    try:
        webhook_url = get_ssm_parameter()
        # 現在の日時を取得
        day = datetime.datetime.now()
        weekday = day.strftime("%a")

        # 日付と曜日の表示形式を変更
        date_str = day.strftime("%Y/%-m/%-d") + f"({weekday})"

        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{date_str}*\n\n*:no_entry_sign: Error occurred during WAF rules check*",
                    },
                }
            ]
        }
        response = requests.post(
            webhook_url,
            json=result_message,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(
            f"[error_result_slack_notification]Request to Slack returned an error: {e}"
        )
