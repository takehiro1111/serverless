"""A module for checking ECS Capacity Provider Strategy and sending Slack notifications.

This module defines a Lambda function that checks the ECS Capacity Provider Strategy
in the STG environment and notifies Slack if any services other than FARGATE are running.
"""

import json
from typing import Any

from logger import logger
from manage_ecs import ECSManager
from setting import ACCOUNTS, IAM_ROLE_NAME_MONITOR_ECS, day_format, is_holiday
from slack_notify import SlackNotify


def process_account(account: dict) -> list:
    """Process ECS operations for a single AWS account.

    Args:
        account: Dictionary containing account info (name and ID)

    Returns:
        List of services running on FARGATE
    """
    ecs_manager = ECSManager(account["name"], account["id"], IAM_ROLE_NAME_MONITOR_ECS)

    ecs_clusters = ecs_manager.list_ecs_clusters()
    ecs_services = ecs_manager.list_ecs_services()

    main_processing = ecs_manager.main_ecs_processing(ecs_clusters, ecs_services)

    return main_processing


def collect_fargate_services(accounts: list) -> list:
    """Collect FARGATE service information from all AWS accounts.

    Args:
        accounts: List of account dictionaries containing name and ID

    Returns:
        List of FARGATE services grouped by account
    """
    fargate_services = []
    for account in accounts:
        has_fargate = process_account(account)
        if has_fargate:
            fargate_services.append(
                {
                    "account": account["name"],
                    "ecs_service": has_fargate,
                }
            )
    logger.debug(f"has_fargate_services_list:{fargate_services}")

    return fargate_services


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Check and update ECS Capacity Provider Strategy.

    Args:
        event: Lambda event object
        context: Lambda context object

    Returns:
        Dict with status code and execution result
    """
    try:
        # FargateになっているままのECSサービスを要素に含んだリスト
        fargate_services = collect_fargate_services(ACCOUNTS)

        # Slack通知の処理
        slack_notifier = SlackNotify(day_format, fargate_services)
        if fargate_services and not is_holiday:
            slack_notifier.monitor_result_slack_notification()
        else:
            logger.info("All ECS services are running on FARGATE_SPOT successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps("ECS ServiceEs daily check complete", indent=4),
        }

    except Exception as e:
        if not is_holiday:
            slack_notifier.error_result_slack_notification()
        logger.error(f"handler occured error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps(
                "Error occurred during ECS ServiceEs daily check", indent=4
            ),
        }
