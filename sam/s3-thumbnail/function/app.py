"""S3に画像ファイルがアップロードされるとDynamoDBにメタデータを保存しSlack通知するモジュール."""

import json
import os
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError
from config import DEFAULT_REGION, DYNAMODB_TABLE, timestamp
from logger import logger
from slack import send_slack_notification


def dynamodb_put_item(bucket: str, obj: str) -> None:
    """Put an item into the DynamoDB table.

    Args:
        bucket (str): event-bucket-thumbnail-dev
        obj    (str): Files added to an S3 bucket as events

    Raises:
        botocore.exceptions.ClientError: If writing to DynamoDB fails
        ResourceNotFoundException: DynamoDB table not found

    Note:
        - image_id: UUIDv4
        - created_at: timestamp
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=DEFAULT_REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)

        item_id = str(uuid.uuid4())
        item = {
            "image_id": item_id,
            "bucket": bucket,
            "original_filename": obj,
            "created_at": timestamp,
        }
        table.put_item(Item=item)

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error("Table Not Found")
            raise
        else:
            logger.error(f"An unexpected error occurred: {e}")
            raise


def is_valid_extensions(obj: str) -> bool:
    """Determine if the file is an image.

    Args:
        obj (str): Files added to an S3 bucket as events

    Returns:
        bool: Returns true if the file extension is an image file.
    """
    is_valid_extensions = {"png", "jpg", "jpeg"}
    ext = os.path.splitext(obj)[1][1:]

    return ext in is_valid_extensions


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Put the metadata into DynamoDB and notify Slack.

    Args:
        event (Dict[str, Any]): S3 Event Metadata
        context (Any): Lambda Execution Context

    Returns:
        Dict[str, Any]: If the operation is successful, status code 200 is returned.

    Raises:
        Exception: Catching all errors
    """
    try:
        for record in event["Records"]:
            bucket_name = record["s3"]["bucket"]["name"]
            obj_name = record["s3"]["object"]["key"]

            # S3バケットのファイルが画像ファイル出ない場合は処理しない。
            if not is_valid_extensions(obj_name):
                break

            # DynamoDBへメタデータをput
            dynamodb_put_item(bucket_name, obj_name)

            # DynamoDBに格納できたらSlack通知
            send_slack_notification(obj_name)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "success lambda_handler"}),
        }

    except Exception as e:
        logger.error(f"Error lambda_handler: {e}")
        raise
