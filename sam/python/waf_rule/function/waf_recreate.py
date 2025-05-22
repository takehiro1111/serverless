import boto3
from slack_notify import send_slack_notification

waf = boto3.client("wafv2", "us-east-1")


def lambda_handler(event, context):
    web_acl_name = event["WebACL"]["Name"]
    web_acl_id = event["WebACL"]["Id"]
    scope = event["WebACL"]["Scope"]
    recreate_rule_name = event["WebACL"]["Rules"]["CountOtherRegions"]["Name"]
    statement = event["WebACL"]["Rules"]["CountOtherRegions"]["Statement"]
    priority = event["WebACL"]["Rules"]["CountOtherRegions"]["Priority"]

    # Get the Web ACL
    web_acl = waf.get_web_acl(Name=web_acl_name, Scope=scope, Id=web_acl_id)

    # Add the New Rule
    new_rule = {
        "Name": recreate_rule_name,
        "Priority": priority,
        "Action": {"Block": {}},
        "Statement": statement,
        "VisibilityConfig": {
            "SampledRequestsEnabled": True,
            "CloudWatchMetricsEnabled": True,
            "MetricName": web_acl_name,
        },
    }

    # Adding CountOtherRegions to Existing Rules
    updated_rules = web_acl["WebACL"]["Rules"] + [new_rule]

    try:
        # Update the Web ACL with the New Rule
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
        send_slack_notification(web_acl_name, recreate_rule_name, "Recreate")

    except Exception as e:
        print(f"Error Recreate Web ACL Rule: {e}")
        # Send error notification to Slack
        send_slack_notification(web_acl_name, recreate_rule_name, f"Failed: {e}")
        raise e

    return response
