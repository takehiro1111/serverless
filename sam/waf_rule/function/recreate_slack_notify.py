from  slack_notify import send_slack_notification


def lambda_handler(event, context):
    try:
        detail = event['detail']
        web_acl_name = detail['requestParameters']['name']
        rules = detail['requestParameters']['rules']
        rule_name = rules[0]['name'] if rules else 'UnknownRule'
        status = detail['eventName']

        send_slack_notification(web_acl_name,status,rule_name)
        
    except KeyError as e:
        raise ValueError(f"KeyError: Missing key in event detail: {e}")
    except Exception as e:
        raise ValueError(f"Error processing event: {e}")
