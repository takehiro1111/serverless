import boto3
import json

# 子アカウントのリスト
accounts = [
    {'account_id': '123456789012', 'role_name': 'CrossAccountWAFRole'},
    {'account_id': '234567890123', 'role_name': 'CrossAccountWAFRole'}
]

def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/{role_name}',
        RoleSessionName='CrossAccountWAFSession'
    )
    credentials = response['Credentials']
    return boto3.client(
        'wafv2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

def check_waf_rules(waf_client):
    web_acls = waf_client.list_web_acls(Scope='REGIONAL')['WebACLs']
    for web_acl in web_acls:
        web_acl_name = web_acl['Name']
        web_acl_id = web_acl['Id']
        response = waf_client.get_web_acl(Name=web_acl_name, Scope='REGIONAL', Id=web_acl_id)
        rules = response['WebACL']['Rules']
        regional_limit_rule_exists = any(rule['Name'] == 'RegionalLimit' for rule in rules)
        if not regional_limit_rule_exists:
            return False, web_acl_name
    return True, None

def lambda_handler(event, context):
    missing_rules = []
    for account in accounts:
        waf_client = assume_role(account['account_id'], account['role_name'])
        valid, web_acl_name = check_waf_rules(waf_client)
        if not valid:
            missing_rules.append({'account_id': account['account_id'], 'web_acl_name': web_acl_name})

    if missing_rules:
        # 通知の実装（例: Slack通知）
        notify_slack(missing_rules)
    
    return {
        'statusCode': 200,
        'body': json.dumps('WAF rules check complete')
    }

def notify_slack(missing_rules):
    webhook_url = get_ssm_parameter()
    result_message = {
        'text': f'Missing RegionalLimit rule in the following WebACLs:\n' +
                '\n'.join([f"Account: {rule['account_id']}, WebACL: {rule['web_acl_name']}" for rule in missing_rules])
    }
    try:
        response = requests.post(
            webhook_url,
            json=result_message,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request to Slack returned an error: {e}")

def get_ssm_parameter():
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(
            Name='/waf_update_rule/SLACK_WEBHOOK',
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        raise ValueError("SSM parameter not found.")
    except ssm.exceptions.ParameterVersionNotFound:
        raise ValueError("SSM parameter version not found.")
    except Exception as e:
        raise ValueError(f"Failed to get SSM parameter: {e}")
