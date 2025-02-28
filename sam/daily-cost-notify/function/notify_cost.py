import json
from datetime import datetime, timezone

import boto3
from slack_notify import send_slack_notification


def get_costs() -> float:
    client = boto3.client("ce", region_name="us-east-1")

    # 現在の日時（UTC）
    now = datetime.now(timezone.utc)

    # 月初の日付を取得（例: 2024-08-01）
    start_date = now.replace(day=1).strftime("%Y-%m-%d")

    # 現在の日付と時刻を取得（例: 2024-08-24）
    end_date = now.date().strftime("%Y-%m-%d")

    # Cost Explorer APIの呼び出し
    response = client.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": end_date},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    monthly_cost = abs(
        float(response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])
    )
    # 科学表記法の文字列に変換して解析(eをsplitで区切りたいため。)
    monthly_cost_e = f"{monthly_cost:e}"
    num, char = monthly_cost_e.split("e")
    # print(f"{float(num):.2f}")

    return float(num)


def lambda_handler(event, context):
    # コストを取得してSlackに通知
    cost = get_costs()
    send_slack_notification(cost)

    return {
        "statusCode": 200,
        "body": json.dumps(f"Success Notify Cost Status: {cost}"),
    }
