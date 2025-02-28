# num = abs(float(("-5.252200000000001e-06")))

# # 科学表記法の文字列に変換して解析
# num_str = f"{num:e}"
# print(num_str)
# mantissa, exponent = num_str.split('e')

# # 仮数部だけを浮動小数点数として取得
# mantissa_value = float(mantissa)

# print(f"{mantissa_value:.2f}")
import pprint
from datetime import datetime, timezone

import boto3


def get_costs():
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


cost = get_costs()
