import json
from datetime import datetime, timedelta, timezone

import boto3
from setting import is_holiday
from slack_notify import send_slack_notification


def get_costs() -> float:
    client = boto3.client("ce", region_name="us-east-1")

    # 現在の日時（UTC）
    now = datetime.now(timezone.utc)

    # 月初の日付を取得（例: 2024-08-01）
    start_date = now.replace(day=1).strftime("%Y-%m-%d")
    print(start_date)

    # 現在の日付と時刻を取得（例: 2024-08-24）
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    print(tomorrow)

    # Cost Explorer APIの呼び出し
    response = client.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": tomorrow},
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

    cost = get_costs()
    send_slack_notification(cost)

    return {
        "statusCode": 200,
        "body": json.dumps(f"Success Notify Cost Status: {cost}"),
    }
