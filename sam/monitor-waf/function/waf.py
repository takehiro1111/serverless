import boto3
from setting import MONITOR_WAF_RULE, WAF_REGION


def assume_role(account_name, account_id, role_name=MONITOR_WAF_RULE):
    """
    各AWSアカウントの認証情報を取得する。
    """
    sts = boto3.client("sts")

    response = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=f"waf_monitor_daily_{account_name}_{account_id}",
    )
    credentials = response["Credentials"]

    waf_client = boto3.client(
        "wafv2",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=WAF_REGION,
    )

    return waf_client


def check_waf_rules(account, waf_client):
    """
    各アカウントのWAFで地域制限のルールが設定されているか確認する。
    """
    web_acls = waf_client.list_web_acls(Scope="CLOUDFRONT")["WebACLs"]
    for web_acl in web_acls:
        web_acl_name = web_acl["Name"]
        web_acl_id = web_acl["Id"]

        # タグ情報を取得
        tags = waf_client.list_tags_for_resource(ResourceARN=web_acl["ARN"])[
            "TagInfoForResource"
        ]["TagList"]

        # 本番環境を除くリソース等は、監視対象から外すよう処理をスキップ
        if any(tag["Key"] == "monitor" and tag["Value"] == "false" for tag in tags):
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
