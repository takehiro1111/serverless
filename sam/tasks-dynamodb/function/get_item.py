import json

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("tasks")


def lambda_handler(event, context):
    try:
        response = table.scan(Limit=3)
        items = response.get("Items", [])

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error_scan:{str(e)}")}

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task Get Successfully!", "tasks": items}),
    }
