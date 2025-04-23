import json

import boto3
from setting import is_holiday, start_date, tomorrow
from slack_notify import send_slack_notification


def get_costs(start_date, end_date) -> float:
    client = boto3.client("ce", region_name="us-east-1")

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": end_date},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        Filter={
            "Not": {
                "Dimensions": {"Key": "RECORD_TYPE", "Values": ["Refund", "Credit"]}
            }
        },
    )

    monthly_cost = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    return float(monthly_cost)


def lambda_handler(event, context):
    print("is_holiday", is_holiday)
    # 祝日なら早期リターンで処理しない。
    if is_holiday:
        return

    months_total_cost = get_costs(start_date, tomorrow)
    send_slack_notification(months_total_cost)

    return {
        "statusCode": 200,
        "body": json.dumps(f"Success Notify Cost Status: ${months_total_cost}"),
    }
