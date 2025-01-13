import json

import boto3
from slack_notify import monitor_result_slack_notification

# WAFを監視したいアカウントのリスト
accounts = [
    # {'account_name': 'sekigaku' , 'account_id': '421643133281', 'role_name': 'lambda-execute-waf '},
    {
        "account_name": "my_account",
        "account_id": "685339645368",
        "role_name": "monitor-waf-rule",
    }
]


# 各アカウントの認証情報を取得
def assume_role(account_id, role_name):
    sts = boto3.client("sts")

    # 各アカウントに配置したIAMロールを取得
    response = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=f"waf_monitor_daily_{account_id}",
    )
    credentials = response["Credentials"]

    waf_client = boto3.client(
        "wafv2",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name="us-east-1",
    )

    return waf_client


# 各アカウントのWAFで地域制限のルールが設定されているか確認。
def check_waf_rules(account, waf_client):
    web_acls = waf_client.list_web_acls(Scope="CLOUDFRONT")["WebACLs"]
    print(web_acls)
    for web_acl in web_acls:
        web_acl_name = web_acl["Name"]
        web_acl_id = web_acl["Id"]
        domain = web_acl.get("Description", "")

        # WebACLのDescriptionに'stg' or 'acc' の文字列が入っている場合は監視対象から外すよう処理をスキップ
        if any(description in domain for description in ("stg", "acc")):
            continue

        response = waf_client.get_web_acl(
            Name=web_acl_name, Scope="CLOUDFRONT", Id=web_acl_id
        )
        rules = response["WebACL"]["Rules"]

        regional_limit_rule_exists = any(
            rule["Name"] == "RegionalLimit" for rule in rules
        )

        if not regional_limit_rule_exists:
            return False, account["account_name"], web_acl_name

    return True, None, None


# EventBridge Schedulerにより日次で関数を実行。
def lambda_handler(event, context):
    missing_rule_accounts = []
    for account in accounts:
        waf_client = assume_role(account["account_id"], account["role_name"])
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

    return {"statusCode": 200, "body": json.dumps("WAF rules daily check complete")}
