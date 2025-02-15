import datetime
from typing import Any

import boto3
import requests
from setting import SSM_PARAMETER_NAME, SSM_PARAMS_REGION


def get_ssm_parameter(default_region: str, ssm_param_name: str) -> Any:
    """
    SSMパラメータに格納しているWebHookのURLを取得
    """
    ssm = boto3.client("ssm", default_region)
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


def monitor_result_slack_notification(
    missing_rule_accounts: list[dict[str, str]], date
) -> None:
    """
    RegionalLimitのルールが設定されていない場合は、日次でSlack通知を行う。
    """
    try:
        slack_webhook_url = get_ssm_parameter(SSM_PARAMS_REGION, SSM_PARAMETER_NAME)
        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{date}*\n\n*:rotating_light: ECS Capacity Provider was not returning*",
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
                        # データ構造を確認しておく。
                        "text": f"*Account:* `{rule['account_name']}` / *ID:* `{rule['account_id']}` / *ECS:* `{rule['web_acl_name']}`",
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


def error_result_slack_notification(date) -> None:
    """
    WAFの処理が何らかの理由でエラーになった場合のSlack通知する。
    """
    try:
        webhook_url = get_ssm_parameter(SSM_PARAMS_REGION, SSM_PARAMETER_NAME)
        result_message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{date}*\n\n*:no_entry_sign: Error occurred during WAF rules check*",
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
