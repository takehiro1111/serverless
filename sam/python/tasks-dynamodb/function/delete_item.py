import json

import boto3

dynamodb = boto3.resource("dynamodb")
table_name = "tasks"
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    if "id" not in event:
        return {"statusCode": 400, "body": json.dumps("event does not exist")}

    item_id = event["id"]

    response = table.delete_item(Key={"id": item_id})

    try:
        response

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error_exception:{str(e)}")}

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task Deleted Successfully!", "id": item_id}),
    }
