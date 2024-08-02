import boto3
import json
from  slack_notify import monitor_result_slack_notification

waf = boto3.client('wafv2', region_name = 'us-east-1')

# WAFの情報を取得する各アカウントのリスト
accounts = [
    {'account': 'sekigaku' , 'account_id': '123456789012', 'role_name': 'CrossAccountWAFRole'},
    {'account': 'hoge' , 'account_id': '123456789012', 'role_name': 'CrossAccountWAFRole'},
]

def assume_role(account_id, role_name):
    sts = boto3.client('sts')

    # 各アカウントに配置したIAMロールを取得
    response = sts.assume_role(
        RoleArn =f'arn:aws:iam::{account_id}:role/{role_name}',
        RoleSessionName ='waf_monitor_session'
    )

    credentials = response['Credentials']

    # 戻り値として、各アカウントの認証情報を設定。(これ見えるかは確認しておく。)
    return boto3.client(
        'wafv2',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken']
    )

def check_waf_rules():
  web_acls = waf.list_web_acls(Scope='CLOUDFRONT')['WebACLs']
  for web_acl in web_acls:
    web_acl_name = web_acl['Name']
    web_acl_id = web_acl['Id']
    domain = web_acl.get('Description', '')

    # 'stg' or 'acc' を部分的にDescriptionに含むWebACLの場合はcontinueで処理をスキップ
    # これでproduction用のWAFのみ検知できる想定。
    if any(description in domain for description in ('stg','acc')):
      continue

    response = waf.get_web_acl(Name = web_acl_name, Scope = 'CLOUDFRONT', Id = web_acl_id)
    rules = response['WebACL']['Rules']

    regional_limit_rule_exists = any(rule['Name'] == 'RegionalLimit' for rule in rules)

    if not regional_limit_rule_exists:
        monitor_result_slack_notification(domain, web_acl_name)

# EventBridgeにより日次で関数を実行する。
def lambda_handler(event, context):
  missing_rule_accounts = []
  for account in accounts:
    waf_client = assume_role(account['account_id'], account['role_name'])
    valid, web_acl_name = check_waf_rules(waf_client)
    if not valid:
      missing_rule_accounts.append({'account_id': account['account_id'], 'web_acl_name': web_acl_name})

  if missing_rule_accounts:
    # 通知の実装（例: Slack通知）
    monitor_result_slack_notification(missing_rule_accounts)

  return {
      'statusCode': 200,
      'body': json.dumps('WAF rules daily check complete')
  }
