"""A module for checking ECS Capacity Provider Strategy and sending Slack notifications.

This module defines a Lambda function that checks the ECS Capacity Provider Strategy
in the STG environment and notifies Slack if any services other than FARGATE are running.
"""

import json

from logger import logger
from manage_ecs import ECSManager
from setting import ACCOUNTS, IAM_ROLE_NAME_MONITOR_ECS, day_format
from slack_notify import SlackNotify


def lambda_handler(event, context):
    """Check ECS Capacity Provider Strategy and update services to use FARGATE_SPOT.

    This function checks all ECS services across specified AWS accounts for any
    services running on FARGATE. If found, it updates them to use FARGATE_SPOT
    and sends a notification through Slack.

    Args:
        event: AWS Lambda event object containing event data
        context: AWS Lambda context object providing runtime information

    Returns:
        dict: Response containing status code and execution result
            {
                'statusCode': int,
                'body': str
            }

    Raises:
        Exception: Any unexpected errors during execution will be caught,
            logged, and notified via Slack
    """
    fargate_services = []
    slack_notifier = SlackNotify(day_format, fargate_services)
    try:
        for account in ACCOUNTS:
            # AssumeRoleして各アカウントのリソースへの認可行う。
            # クラスのインスタンス化学
            ecs_manager = ECSManager(
                account["name"], account["id"], IAM_ROLE_NAME_MONITOR_ECS
            )

            # ECSクラスターのリストを取得
            ecs_clusters = ecs_manager.list_ecs_clusters()

            # ECSサービスの一覧を取得
            ecs_services = ecs_manager.list_ecs_services()

            # FaragateになっていたECSサービスがリストとして入る。
            has_fargate = ecs_manager.update_capacity_provider(
                ecs_clusters, ecs_services
            )

            # Slack通知用にFargateになっていたECSサービスをリストへ追加。
            if has_fargate:
                fargate_services.append(
                    {
                        "account": account["name"],
                        "ecs_service": has_fargate,
                    }
                )
        logger.info(f"has_fargate_services_list:{fargate_services}")

        if fargate_services:
            slack_notifier.monitor_result_slack_notification()
        else:
            logger.info("All ECS services are running on FARGATE_SPOT successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps("ECS ServiceEs daily check complete", indent=4),
        }

    except Exception as e:
        slack_notifier.error_result_slack_notification()
        logger.error(f"handler occured error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps(
                "Error occurred during ECS ServiceEs daily check", indent=4
            ),
        }
