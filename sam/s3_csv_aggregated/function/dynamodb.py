import uuid

import boto3
from botocore.exceptions import ClientError
from setting import DYNAMODB_TABLE, date, logger


# DynamoDBへput
def dynamodb_put_item(bucket, src_obj, dst_obj):
    try:
        dynamodb_client = boto3.client("dynamodb")
        item_id = str(uuid.uuid4())
        item = {
            "id": item_id,
            "date": date,
            "bucket": bucket,
            "src_obj": src_obj,
            "dst_obj": dst_obj,
        }
        response = dynamodb_client.put_item(TableName=DYNAMODB_TABLE, Item=item)

        return response

    except dynamodb_client.Client.exceptions.ResourceNotFoundException:
        logger.error(f"Resource NotFound")
        raise

    except ClientError as e:
        logger.error(f"dynamodb_put_item: {e}")
        raise
