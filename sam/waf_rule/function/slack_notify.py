import requests    

def send_slack_notification(web_acl_name, rule_name, status):
    webhook_url = ''
    recreate_message = {
        'text': f'Success WebACL:{web_acl_name} / Rule:{rule_name} / Status: {status}'
    }

    try:
        response = requests.post(
            webhook_url, 
            json = recreate_message,
            headers = {"Content-Type": "application/json"}
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Slack returned an error: {e}")
