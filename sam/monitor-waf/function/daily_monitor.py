import json
import logging

import boto3
import slack_notify


def load_config(file_path):
    """
    config.jsonを読み込み、辞書として返す。
    """
    try:
        with open(file_path, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logger.error(f"Config file {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from config file {file_path}.")
        raise


# 定数
config = load_config("config.json")
MONITOR_WAF_RULE = config.get("DEFAULT_ROLE_NAME")
ACCOUNTS = config.get("ACCOUNTS")


def setup_logger(name=None, level=logging.INFO):
    """
    ロガーをセットアップする関数。
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # コンソールハンドラを作成
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # フォーマッタを作成してハンドラに追加
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    # ロガーにハンドラを追加
    if not logger.handlers:
        logger.addHandler(ch)

    return logger


logger = setup_logger(__name__)


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
        region_name=config.get("US_EAST_1"),
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
            slack_notify.monitor_result_slack_notification(missing_rule_accounts)
        else:
            logger.info("All accounts have a ReginalLimit set")

        return {
            "statusCode": 200, "body": json.dumps("WAF rules daily check complete")
        }

    except Exception as e:
        slack_notify.error_result_slack_notification()
        logger.error(f"An error occurred during WAF rules check: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps("Error occurred during WAF rules check"),
        }
