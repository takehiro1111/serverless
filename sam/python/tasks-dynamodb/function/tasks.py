import json
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("tasks")


def lambda_handler(event, context):
    title = event["title"]
    details = event.get("details", "")

    item_id = str(uuid.uuid4())

    timestamp = datetime.now().isoformat()

    item = {
        "id": item_id,
        "title": title,
        "details": details,
        "createAt": timestamp,
        "updateAt": timestamp,
    }

    try:
        table.put_item(Item=item)

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error_excepytion:{str(e)}")}

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task Put Successfully!", "id": item_id}),
    }
