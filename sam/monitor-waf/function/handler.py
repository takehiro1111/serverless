import json

from logger import logger
from setting import ACCOUNTS, MONITOR_WAF_RULE
from slack_notify import (
    error_result_slack_notification,
    monitor_result_slack_notification,
)
from waf import assume_role, check_waf_rules


def lambda_handler(event, context):
    """
    EventBridge Schedulerにより日次で監視並びに通知を実行。
    """
    try:
        missing_rule_accounts = []
        for account in ACCOUNTS:
            waf_client = assume_role(
                account["account_name"], account["account_id"], MONITOR_WAF_RULE
            )
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
        logger.error(f"An error occurred during WAF rules check: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps("Error occurred during WAF rules check"),
        }
