import datetime
from typing import Any

import boto3
import requests
from setting import DEFAULT_REGION, SSM_PARAMETER_NAME


def get_ssm_parameter(ssm_param_name: str) -> Any:
    """
    SSMパラメータに格納しているWebHookのURLを取得
    """
    ssm = boto3.client("ssm")
    print(f"ssm type: {type(ssm)}")
    try:
        response = ssm.get_parameter(
            Name=ssm_param_name,
            WithDecryption=True,
        )
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound:
        raise ValueError("SSM parameter not found.")

    except ssm.exceptions.ParameterVersionNotFound:
        raise ValueError("SSM parameter version not found.")

    except Exception as e:
        raise ValueError(f"Failed to get SSM parameter: {e}")


def monitor_result_slack_notification(has_fargate: list[dict[str, str]]) -> None:
    """
    RegionalLimitのルールが設定されていない場合は、日次でSlack通知を行う。
    """
    try:
        slack_webhook_url = get_ssm_parameter(SSM_PARAMETER_NAME)
        # 現在の日時を取得
        day = datetime.datetime.now()
        weekday = day.strftime("%a")
        # 日付と曜日の表示形式を変更
        day_format = day.strftime("%Y/%-m/%-d") + f"({weekday})"
        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{day_format}*\n\n*:bell: ECS Capacity Provider was not returning*",
                    },
                },
                {"type": "divider"},
            ]
        }

        for rule in has_fargate:
            ecs_services = [i["service"] for i in rule["ecs_service"]]
            result_message["blocks"].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        # データ構造を確認しておく。
                        "text": f"*Account:* `{rule['account']}` / *ID:* `{rule['account_id']}` / *ECS:* `{ecs_services}`",
                    },
                }
            )

        response = requests.post(
            slack_webhook_url,
            json=result_message,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Slack returned an error: {e}")


def error_result_slack_notification() -> None:
    """
    何らかの理由でエラーになった場合のSlack通知する。
    """
    try:
        webhook_url = get_ssm_parameter(SSM_PARAMETER_NAME)
        # 現在の日時を取得
        day = datetime.datetime.now()
        weekday = day.strftime("%a")
        # 日付と曜日の表示形式を変更
        day_format = day.strftime("%Y/%-m/%-d") + f"({weekday})"
        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{day_format}*\n\n*:no_entry_sign: Error occurred during ECS Capacity Provider check*",
                    },
                }
            ]
        }
        response = requests.post(
            webhook_url,
            json=result_message,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(
            f"[error_result_slack_notification]Request to Slack returned an error: {e}"
        )
