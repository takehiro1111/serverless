import boto3
from botocore.exceptions import ClientError
from setting import MAIL, SNS_TOPIC_ARN, logger


# SNSを経由してGmailへ送信
def publish_sns(date_today, bucket, dest_obj):
    try:
        sns_client = boto3.client("sns")
        topic_arn = SNS_TOPIC_ARN

        message = MAIL["message"].format(
            datetime=date_today, bucket=bucket, obj=dest_obj
        )

        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=MAIL["subject"],
            Message=message,
        )
        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "EndpointDisabled":
            logger.error(f"This is not a valid email address.")
            raise
        elif error_code == "NotFound":
            logger.error(f"Indicates that the requested resource does not exist.")
            raise
        else:
            logger.error(f"This is an unexpected error. {e}")
            raise
