import string

import boto3
from botocore.exceptions import ClientError
from setting import SNS_TOPIC_ARN, SUBJECT, logger, timestamp


# SNSを経由してGmailへ送信
def publish_sns(bucket_name, obj_name):
    try:
        sns_client = boto3.client("sns")
        topic_arn = SNS_TOPIC_ARN

        # メールのテンプレート文の変数に値を定義
        with open(SUBJECT["message"]) as f:
            t = string.Template(f.read())

        message_contents = t.substitute(
            datetime=timestamp, bucket=bucket_name, obj=obj_name
        )

        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=SUBJECT["subject"],
            Message=message_contents,
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
            logger.error(f"This is an unexpected error.")
            raise
