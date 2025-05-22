# num = abs(float(("-5.252200000000001e-06")))

# # 科学表記法の文字列に変換して解析
# num_str = f"{num:e}"
# print(num_str)
# mantissa, exponent = num_str.split('e')

# # 仮数部だけを浮動小数点数として取得
# mantissa_value = float(mantissa)

# print(f"{mantissa_value:.2f}")
import pprint
from datetime import datetime, timedelta, timezone

import boto3


def get_costs():
    client = boto3.client("ce", region_name="us-east-1")

    # 現在の日時（UTC）
    now = datetime.now(timezone.utc)

    # 月初の日付を取得（例: 2024-08-01）
    start_date = now.replace(day=1).strftime("%Y-%m-%d")
    print(f"start_date:{start_date}")

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

    print(response)

    monthly_cost = abs(
        float(response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])
    )

    print(f"monthly_cost:{monthly_cost}")
    # 科学表記法の文字列に変換して解析(eをsplitで区切りたいため。)
    monthly_cost_e = f"{monthly_cost:e}"
    num, char = monthly_cost_e.split("e")
    print(f"{float(num):.2f}")

    # コストデータの取得
    # 月初からの合計コストを計算
    # for result in response["ResultsByTime"]:
    #     # print(f"response[\"ResultsByTime\"]:{response["ResultsByTime"]}")
    #     daily_cost = abs(float((result["Total"]["UnblendedCost"]["Amount"])))

    #     # 科学表記法の文字列に変換して解析(eをsplitで区切りたいため。)
    #     daily_cost_e = f"{daily_cost:e}"
    #     num, char = daily_cost_e.split("e")
    #     total_cost += float(num)

    return f"{float(num):.2f}"


# def get_costs() -> float:
#     client = boto3.client("ce", region_name="us-east-1")

#     # 現在の日時（UTC）
#     now = datetime.now(timezone.utc)

#     # 月初の日付を取得
#     start_date = now.replace(day=1).strftime("%Y-%m-%d")
#     print(f"Start date: {start_date}")

#     # 翌月の1日を終了日として設定（排他的なため月末までを含める）
#     if now.month == 12:
#         end_date = f"{now.year + 1}-01-01"
#     else:
#         end_date = f"{now.year}-{now.month + 1:02d}-01"
#     print(f"End date: {end_date}")

#     # クレジットとリファンドを除外するフィルターを追加
#     response = client.get_cost_and_usage(
#         TimePeriod={"Start": start_date, "End": end_date},
#         Granularity="MONTHLY",
#         Metrics=["UnblendedCost"],
#         Filter={
#             "Not": {
#                 "Dimensions": {
#                     "Key": "RECORD_TYPE",
#                     "Values": ["Refund", "Credit"]
#                 }
#             }
#         }
#     )

#     print(f"API Response: {response}")

#     # 全体のコストを取得
#     monthly_cost = float(response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])

#     print(f"Raw monthly cost: {monthly_cost}")

#     return monthly_cost

cost = get_costs()

import datetime

import holidays

# Get date for slack notification
today = datetime.datetime.now()
weekday = today.strftime("%a")
day_format = today.strftime("%Y/%-m/%-d") + f"({weekday})"

# 日本の祝日カレンダーを作成
jp_holidays = holidays.Japan()
print(jp_holidays)

# 特定の日が祝日かどうかを判定
is_holiday = datetime.date(today.year, today.month, today.day) in jp_holidays
print(is_holiday)
