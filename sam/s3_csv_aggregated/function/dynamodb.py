import uuid

import boto3
from botocore.exceptions import ClientError
from setting import DEFAULT_REGION_NAME, DYNAMODB_TABLE, date, datetime, logger


# DynamoDBへput
def dynamodb_put_item(bucket, src_obj, dst_obj):
    try:
        dynamodb = boto3.resource("dynamodb", region_name=DEFAULT_REGION_NAME)
        table = dynamodb.Table(DYNAMODB_TABLE)
        item_id = str(uuid.uuid4())
        # datetimeオブジェクトをISO形式の文字列に変換
        if isinstance(date, datetime):
            date_str = date.isoformat()
        else:
            date_str = date

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

    except ClientError as e:
        logger.error(f"dynamodb_put_item: {e}")
        raise
