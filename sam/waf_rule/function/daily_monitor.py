import boto3
import json
from  slack_notify import monitor_result_slack_notification

waf = boto3.client('wafv2', region_name='us-west-1')

def check_waf_rules():
  web_acls = waf.list_web_acls(Scope='CLOUDFRONT')['WebACLs']
  for web_acl in web_acls:
      web_acl_name = web_acl['Name']
      web_acl_id = web_acl['Id']
      domain = web_acl['Description']

      response = waf.get_web_acl(Name = web_acl_name, Scop = 'CLOUDFRONT', Id = web_acl_id)
      rules = response['WebACL']['Rules']

      regional_limit_rule_exists = any(rule['Name'] == 'RegionalLimit' for rule in rules)

      if not regional_limit_rule_exists:
          monitor_result_slack_notification(domain, web_acl_name)

def lambda_handler(event, context):
    check_waf_rules()
    return {
        'statusCode': 200,
        'body': json.dumps('WAF rules check complete')
    }
