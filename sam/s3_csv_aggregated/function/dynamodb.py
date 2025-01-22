"""CSVが処理された後にDynamoDBにメタデータをPutするモジュール."""

import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError
from setting import DEFAULT_REGION_NAME, DYNAMODB_TABLE, d_today, logger


# DynamoDBへput
def dynamodb_put_item(bucket: str, src_obj: str, dst_obj: str) -> Any:
    """Put metadata to DynamoDB after CSV is processed.

    Args:
        bucket (str): The name of the S3 bucket.
        src_obj (str): S3 bucket source object.
        dst_obj (str): S3 bucket destination object.

    Returns:
        Any: DynamoDB Table Items.
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=DEFAULT_REGION_NAME)
        table = dynamodb.Table(DYNAMODB_TABLE)
        item_id = str(uuid.uuid4())

        # date型からISO ISOフォーマット形式の文字列型に変換
        date_str = d_today.isoformat()

        item = {
            "id": item_id,
            "date": date_str,
            "bucket": bucket,
            "src_obj": src_obj,
            "dst_obj": dst_obj,
        }
        response = table.put_item(Item=item)
        logger.info(f"Successfully put item to DynamoDB: id={item_id}")

        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            logger.error(f"Table {DYNAMODB_TABLE} not found")
        else:
            logger.error(
                f"DynamoDB put_item error: {error_code} - {e.response['Error']['Message']}"
            )
        raise
