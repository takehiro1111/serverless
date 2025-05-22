import boto3
import requests

ssm = boto3.client("ssm", "ap-northeast-1")


def get_ssm_parameter() -> str:
    try:
        response = ssm.get_parameter(
            Name="/common/waf-update/SLACK_WEBHOOK", WithDecryption=True
        )
        return response["Parameter"]["Value"]

    except ssm.exceptions.ParameterNotFound:
        raise ValueError("SSM parameter not found.")

    except ssm.exceptions.ParameterVersionNotFound:
        raise ValueError("SSM parameter version not found.")

    except Exception as e:
        raise ValueError(f"Failed to get SSM parameter: {e}")


def send_slack_notification(process, account, account_id, web_acl_name, status, emoji):
    webhook_url = get_ssm_parameter()

    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{emoji}{process} WebACL RegionalLimit : `{status}`*",
                },
            },
            {"type": "divider"},
        ]
    }
    message["blocks"].append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Account:* `{account}` / *ID:* `{account_id}` / *WebACL:* `{web_acl_name}`",
            },
        }
    )

    try:
        response = requests.post(
            webhook_url, json=message, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Slack returned an error: {e}")
