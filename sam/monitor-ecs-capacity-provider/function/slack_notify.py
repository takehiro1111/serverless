from typing import Any

import boto3
import requests
from logger import logger
from setting import DEFAULT_REGION, SSM_PARAMETER_NAME


def get_ssm_parameter(ssm_param_name: str) -> Any:
    """
    SSMパラメータに格納しているWebHookのURLを取得
    """
    ssm = boto3.client("ssm", region_name=DEFAULT_REGION)
    print(f"ssm type: {type(ssm)}")
    try:
        response = ssm.get_parameter(
            Name=ssm_param_name,
            WithDecryption=True,
        )
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound as e:
        logger.error(f"SSM parameter not found.:{e}")
        raise
    except ssm.exceptions.ParameterVersionNotFound as e:
        logger.error(f"SSM parameter version not found.:{e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred.: {e}")
        raise


def monitor_result_slack_notification(
    has_fargate: list[dict[str, str]], day_format
) -> None:
    """
    RegionalLimitのルールが設定されていない場合は、日次でSlack通知を行う。
    """
    try:
        slack_webhook_url = get_ssm_parameter(SSM_PARAMETER_NAME)
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
            ecs_services_list = [i["service"] for i in rule["ecs_service"]]
            print(f"ecs_services_list:{ecs_services_list}")

            ecs_services_str = ",".join(
                [f"{i}.`{service}`" for i, service in enumerate(ecs_services_list, 1)]
            )
            print(f"ecs_services_str:{ecs_services_str}")

            result_message["blocks"].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Account:* `{rule['account']}` / *ID:* `{rule['account_id']}` / *ECS:* {ecs_services_str}",
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
        logger.error(f"Request to Slack returned an error: {e}")
        raise


def error_result_slack_notification(day_format) -> None:
    """
    何らかの理由でエラーになった場合のSlack通知する。
    """
    try:
        webhook_url = get_ssm_parameter(SSM_PARAMETER_NAME)
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
        logger.error(
            f"error_result_slack_notification Request to Slack returned an error: {e}"
        )
        raise
