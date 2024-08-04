import requests
import boto3    

ssm = boto3.client('ssm','ap-northeast-1')

def get_ssm_parameter()-> str:
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


def send_slack_notification(web_acl_name,status,rule_name = 'CountOtherRegions' ):
  webhook_url = get_ssm_parameter()

  message = {
    'text': f'Success WebACL:{web_acl_name} / Rule:{rule_name} / Status: {status}'
  }

  try:
    response = requests.post(
      webhook_url, 
      json = message,
      headers = {"Content-Type": "application/json"}
    )
    response.raise_for_status()

  except requests.exceptions.RequestException as e:
    raise ValueError(f"Request to Slack returned an error: {e}")


def monitor_result_slack_notification(missing_rule_accounts):
  webhook_url = get_ssm_parameter()

  result_message = {
    'text': f'Missing RegionalLimit rule in the following WebACLs:\n' +
            '\n'.join([f"Account: {rule['account_name']},Account_ID: {rule['account_id']}, WebACL: {rule['web_acl_name']}" for rule in missing_rule_accounts])
  }

  try:
    response = requests.post(
      webhook_url, 
      json = result_message,
      headers = {"Content-Type": "application/json"}
    )
    response.raise_for_status()

  except requests.exceptions.RequestException as e:
    raise ValueError(f"Request to Slack returned an error: {e}")  
