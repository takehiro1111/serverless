"""一連の処理が完了した後にメール通知するモジュール."""

from typing import Any

import boto3
from botocore.exceptions import ClientError
from setting import MAIL, SNS_TOPIC_ARN, date, logger


# SNSを経由してGmailへ送信
def send_completion_email(date_today: date, bucket: str, dest_obj: str) -> Any:
    """Send an email notification after a series of processes is completed.

    Args:
        date_today (date): CSV Processing Date.
        bucket (str): The name of the S3 bucket.
        dest_obj (str): Destination S3 object.

    Returns:
        Any: Mail Templates.
    """
    try:
        sns_client = boto3.client("sns")
        message = MAIL["message"].format(
            datetime=date_today, bucket=bucket, obj=dest_obj
        )

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=MAIL["subject"],
            Message=message,
        )
        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "EndpointDisabled":
            logger.error("This is not a valid email address.")
            raise
        elif error_code == "NotFound":
            logger.error("Indicates that the requested resource does not exist.")
            raise
        else:
            logger.error(f"This is an unexpected error. {e}")
            raise
