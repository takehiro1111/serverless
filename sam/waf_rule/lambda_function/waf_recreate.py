import boto3

waf = boto3.client('wafv2','us-east-1')

def lambda_handler(event, context):
    web_acl_name = event['WebACL']['Name']
    web_acl_id = event['WebACL']['Id']
    scope = event['WebACL']['Scope']
    recreate_rule_name = event['WebACL']['Rules'][0]['Name']
    statement = event['WebACL']['Rules'][0]['Statement']
    priority = event['WebACL']['Rules'][0]['Priority']
    
    # Get the Web ACL
    web_acl = waf.get_web_acl(
        Name = web_acl_name,
        Scope = scope,
        Id = web_acl_id
    )
    
    # Add the new rule
    new_rule = {
        'Name': recreate_rule_name,
        'Priority': priority,
        'Action': {'Block': {}},
        'Statement': statement,
        'VisibilityConfig': {
            'SampledRequestsEnabled': True,
            'CloudWatchMetricsEnabled': True,
            'MetricName': web_acl_name
        }
    }
    
    updated_rules = web_acl['WebACL']['Rules'] + [new_rule]
    
    try:
    # Update the Web ACL with the new rule
        response = waf.update_web_acl(
            Name = web_acl_name,
            Scope = scope,
            Id = web_acl_id,
            DefaultAction = web_acl['WebACL']['DefaultAction'],
            Rules = updated_rules,
            VisibilityConfig = web_acl['WebACL']['VisibilityConfig'],
            LockToken = web_acl['LockToken']
        )
    except Exception as e:
        print(f"Error Recreate Web ACL Rule: {e}")
        raise e
    
    return response
