"""Lambda Handler.

This module defines a Lambda function that checks the ECS Capacity Provider Strategy
in the STG environment and notifies Slack if any services other than FARGATE are running.
"""

import json

from check_ecs import (
    check_capacity_provider,
    get_ecs_service,
    list_ecs_clusters,
    sts_assume_role,
)
from logger import logger
from setting import ACCOUNTS, IAM_ROLE_NAME_MONITOR_ECS, day_format
from slack_notify import (
    error_result_slack_notification,
    monitor_result_slack_notification,
)


def lambda_handler(event, context):
    """lambda_handler.

    Check the ECS Capacity Provider Strategy, and if there is any ECS running on FARGATE,
    modify the service to FARGATE_SPOT and notify Slack.

    :param event: Event information
    :param context: Lambda execution context
    :return: A dictionary containing a status code and a message
    """
    try:
        fargate_services = []
        for account in ACCOUNTS:
            # AssumeRoleして認証する。
            ecs_client = sts_assume_role(
                account["account_name"],
                account["account_id"],
                IAM_ROLE_NAME_MONITOR_ECS,
            )

            # ECSクラスターのリストを取得
            ecs_clusters = list_ecs_clusters(ecs_client)

            # ECSサービスの一覧を取得
            ecs_services = get_ecs_service(ecs_client)

            # FaragateになっていたECSサービスがリストとして入る。
            has_fargate = check_capacity_provider(
                ecs_client, ecs_clusters, ecs_services
            )

        if has_fargate:
            fargate_services.append(
                {
                    "account": account["account_name"],
                    "account_id": account["account_id"],
                    "ecs_service": has_fargate,
                }
            )

        if fargate_services:
            # Slack通知。
            monitor_result_slack_notification(fargate_services, day_format)
        else:
            logger.info("All ECS services are running on FARGATE_SPOT successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps("ECS ServiceEs daily check complete", indent=4),
        }

    except Exception as e:
        error_result_slack_notification(day_format)
        logger.error(f"handler occured error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps(
                "Error occurred during ECS ServiceEs daily check", indent=4
            ),
        }
