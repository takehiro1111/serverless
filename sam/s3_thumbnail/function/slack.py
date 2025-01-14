"""SSMパラメータストアからSlackのWebhookURLを取得し、Slack通知するモジュール."""

import json

import boto3
import requests
from config import DEFAULT_REGION, SLACK_WEBHOOK_URL
from logger import logger


def get_ssm_parameter() -> str:
    """Get the SSM parameter store that stores the Slack Webhook URL.

    Returns:
        str: Returns the Slack webhook URL stored in the parameter store.

    Raises:
        ssm.exceptions.ParameterNotFound: If the parameter store is not found
        Exception: Catching other errors
    """
    try:
        ssm = boto3.client("ssm", DEFAULT_REGION)
        response = ssm.get_parameter(Name=SLACK_WEBHOOK_URL, WithDecryption=True)
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound:
        logger.error("Value not found.")
        raise

    except Exception as e:
        logger.error(f"Failed to get SSM parameter: {e}")
        raise


def send_slack_notification(file: str) -> None:
    """Send a request to Slack using the Post method.

    Args:
        file (str): Files added to an S3 bucket as events

    Returns:
        None: Returns True if the request is successful.
    """
    try:
        webhook_url = get_ssm_parameter()

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
        logger.error(f"An HTTP error occurred: {e}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"The request failed:{e}")
        raise
