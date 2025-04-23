import json

import boto3
import requests
from logger import logger
from setting import SLACK_WEBHOOK_URL


def get_ssm_parameter() -> str:
    ssm = boto3.client("ssm", "ap-northeast-1")
    try:
        response = ssm.get_parameter(Name=SLACK_WEBHOOK_URL, WithDecryption=True)
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound:
        logger.error("SSM parameter not found.")
        raise

    except ssm.exceptions.ParameterVersionNotFound:
        logger.error("SSM parameter version not found.")
        raise

    except Exception as e:
        logger.error(f"Failed to get SSM parameter: {e}")
        raise


def send_slack_notification(cost):
    webhook_url = get_ssm_parameter()

    # Slackに送信するメッセージ
    message = {"text": f"月初から本日までのAWS使用料は ${cost:.2f} です。"}

    # Slack WebhookにPOSTリクエストを送信
    response = requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        logger.error(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
        raise
