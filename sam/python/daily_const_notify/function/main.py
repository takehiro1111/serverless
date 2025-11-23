import json

from cost_manage import CostExplorerManager
from setting import (
    has_int_now_date,
    is_holiday,
    last_end_date,
    last_start_date,
    start_date,
    tomorrow,
)
from slack_manage import SlackManager


def lambda_handler(event, context):
    if is_holiday:
        return {"statusCode": 200, "body": json.dumps("Skipped: Holiday")}

    cost_manager = CostExplorerManager()
    slack_manager = SlackManager()

    # 基本的なコスト情報
    months_total_cost = cost_manager.get_cost_monthly_total(start_date, tomorrow)
    last_months_total_cost = cost_manager.get_cost_monthly_total(
        last_start_date, last_end_date
    )

    # ユーザー別コストを取得(月初の場合は前月の期間)
    if has_int_now_date == 1:
        users_by_cost = cost_manager.get_users_by_cost(last_start_date, last_end_date)
        user_service_details = cost_manager.get_cost_by_service_for_users(
            last_start_date, last_end_date, users_by_cost
        )
        user_cost = cost_manager.format_user_details(user_service_details)
    else:
        users_by_cost = cost_manager.get_users_by_cost(start_date, tomorrow)
        user_service_details = cost_manager.get_cost_by_service_for_users(
            start_date, tomorrow, users_by_cost
        )
        user_cost = cost_manager.format_user_details(user_service_details)

    slack_manager.send_slack_notification(
        months_total_cost,
        last_months_total_cost,
        user_cost,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": f"Success Notify Cost Status: ${months_total_cost}",
                "total_cost": months_total_cost,
                "user_count": users_by_cost,
            }
        ),
    }
