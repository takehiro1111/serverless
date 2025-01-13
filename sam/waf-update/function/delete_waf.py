import json
import logging

import boto3
from send_slack_notify import send_slack_notification

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# configの取得
with open("config.json") as f:
    config = json.load(f)
    account = config.get("account")
    account_id = config.get("account_id")

waf = boto3.client("wafv2", "us-east-1")


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    web_acl_name = event["WebACL"]["Name"]
    rule_name_to_delete = event["WebACL"]["Rules"]["RegionalLimit"]["Name"]
    web_acl_id = event["WebACL"]["Id"]
    scope = event["WebACL"]["Scope"]

    logger.info(
        f"Attempting to delete rule {rule_name_to_delete} from WebACL {web_acl_name}"
    )

    # Get the Web ACL
    try:
        web_acl = waf.get_web_acl(
            Name=web_acl_name,
            Scope=scope,
            Id=web_acl_id,
        )
        logger.info(f"Get Web ACL {web_acl_name} retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving Get Web ACL: {e}")
        send_slack_notification(
            "Failed", account, account_id, web_acl_name, "get_web_acl", ":x:"
        )
        raise e

    # Filter out the rule to delete
    updated_rules = [
        rule
        for rule in web_acl["WebACL"]["Rules"]
        if rule["Name"] != rule_name_to_delete
    ]

    try:
        # Update the Web ACL without the deleted rule
        response = waf.update_web_acl(
            Name=web_acl_name,
            Scope=scope,
            Id=web_acl_id,
            DefaultAction=web_acl["WebACL"]["DefaultAction"],
            Rules=updated_rules,
            VisibilityConfig=web_acl["WebACL"]["VisibilityConfig"],
            LockToken=web_acl["LockToken"],
        )
        logger.info(
            f"Rule {rule_name_to_delete} deleted successfully from WebACL {web_acl_name}"
        )
        # Send notification to Slack
        send_slack_notification(
            "Success", account, account_id, web_acl_name, "Delete", ":white_check_mark:"
        )

    except Exception as e:
        logger.error(f"Error deleting Web ACL Rule: {e}")
        # Send error notification to Slack
        send_slack_notification(
            "Faliled", account, account_id, web_acl_name, "Delete", ":x:"
        )
        raise e

    return response
