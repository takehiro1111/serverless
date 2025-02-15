import json

from logger import logger
from monitor_ecs_service import (
    check_capacity_provider,
    list_ecs_clusters,
    sts_assume_role,
)
from setting import ACCOUNTS, IAM_ROLE_NAME_MONITOR_ECS
from slack_notify import (
    error_result_slack_notification,
    monitor_result_slack_notification,
)


def lambda_handler(event, context):
    try:
        fargate_ecs = []
        for account in ACCOUNTS:
            ecs_client = sts_assume_role(account["account_name"], account["account_id"])
        valid, account_name, web_acl_name = check_waf_rules(account, waf_client)
        if not valid:
            missing_rule_accounts.append(
                {
                    "account_name": account_name,
                    "account_id": account["account_id"],
                    "web_acl_name": web_acl_name,
                }
            )
        if missing_rule_accounts:
            monitor_result_slack_notification(missing_rule_accounts)
        else:
            logger.info("All accounts have a ReginalLimit set")

        return {"statusCode": 200, "body": json.dumps("WAF rules daily check complete")}

    except Exception as e:
        error_result_slack_notification()
        logger.error(f"handler occured error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps("Error occurred during WAF rules check"),
        }
