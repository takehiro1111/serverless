import boto3
import json

# domain = 'stg.test.com'

# if any(description in domain for description in ('stg','acc')):
#     print('処理をスキップ')
# else:
#     print('処理を継続させる')


# rules = [
#   {'Name': 'RateLimit'},
#   {'Name': 'RegionalLimit'},
#   {'Name': 'IPBlacklist'}
# ]

# # 'RegionalLimit'という名前のルールが存在するかをチェック
# regional_limit_rule_exists = any(rule['Name'] == 'RegionalLimit' for rule in rules)

# print(regional_limit_rule_exists)  # 出力: True

waf = boto3.client('wafv2', region_name = 'us-east-1')

web_acls = waf.list_web_acls(Scope='CLOUDFRONT')['WebACLs']
for web_acl in web_acls:
    web_acl_name = web_acl['Name']
    web_acl_id = web_acl['Id']
    domain = web_acl.get('Description', '')

response = waf.get_web_acl(Name = web_acl_name, Scope = 'CLOUDFRONT', Id = web_acl_id)

formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
# print(formatted_response)

rules = response['WebACL']['Rules'][0]['Name']
print(rules)
