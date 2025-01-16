"""SSMパラメータストアからSlackのWebhookURLを取得し、Slack通知するモジュール."""

import json
from typing import Any

import boto3
import requests
from botocore.exceptions import ClientError
from logger import logger
from setting import DEFAULT_REGION_NAME, SLACK_WEBHOOK_URL


def get_slack_webhook_url_from_ssm() -> Any:
    """Get the SSM parameter store that stores the Slack Webhook URL.

    Returns:
        str: Returns the Slack webhook URL stored in the parameter store.

    Raises:
        ssm.exceptions.ParameterNotFound: If the parameter store is not found
        Exception: Catching other errors
    """
    try:
        ssm = boto3.client("ssm", DEFAULT_REGION_NAME)
        response = ssm.get_parameter(Name=SLACK_WEBHOOK_URL, WithDecryption=True)

        return response["Parameter"]["Value"]

    except ClientError as e:
        if e.response["Error"]["Code"] == "ParameterNotFound":
            logger.error(f"SSM parameter Not Found {SLACK_WEBHOOK_URL}")
        else:
            logger.error(f"An unexpected error occurred:{e}")
            raise


def send_slack_notification(file: str) -> Any:
    """Send a request to Slack using the Post method.

    Args:
        file (str): Files added to an S3 bucket as events

    Returns:
        None: Returns True if the request is successful.
    """
    try:
        webhook_url = get_slack_webhook_url_from_ssm()

        # Slackに送信するメッセージ
        message = {"text": f"新しく{file}が追加されました。"}

        # Slack WebhookにPOSTリクエストを送信
        response = requests.post(
            webhook_url,
            data=json.dumps(message),
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        # レスポンスのステータスコードを確認
        status = response.raise_for_status()

        return status

    except requests.exceptions.Timeout:
        logger.error("The request timed out")
        raise

    except requests.exceptions.HTTPError as e:
        logger.error(f"Status Code {e.response.status_code}")
        logger.error(f"Response {e.response.text}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"An unexpected error occurred:{e}")
        raise
