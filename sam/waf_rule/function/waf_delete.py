import boto3
from slack_notify import send_slack_notification

waf = boto3.client("wafv2", "us-east-1")


def lambda_handler(event, context):
    web_acl_name = event["WebACL"]["Name"]
    rule_name_to_delete = event["WebACL"]["Rules"]["CountOtherRegions"]["Name"]
    web_acl_id = event["WebACL"]["Id"]
    scope = event["WebACL"]["Scope"]

    # Get the Web ACL
    web_acl = waf.get_web_acl(
        Name=web_acl_name,
        Scope=scope,
        Id=web_acl_id,
    )

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

        # Send notification to Slack
        send_slack_notification(web_acl_name, rule_name_to_delete, "Delete")

    except Exception as e:
        print(f"Error Delete Web ACL Rule: {e}")
        # Send error notification to Slack
        send_slack_notification(web_acl_name, rule_name_to_delete, f"Failed: {e}")
        raise e

    return response
