import requests
import boto3
import json

def get_ssm_parameter()-> str:
  ssm = boto3.client("ssm","ap-northeast-1")
  try:
    response = ssm.get_parameter(
      Name="/development/daily-cost-notify/SLACK_WEBHOOK_URL",
      WithDecryption=True
    )
    return response["Parameter"]["Value"]
  
  except ssm.exceptions.ParameterNotFound:
    raise ValueError("SSM parameter not found.")
  
  except ssm.exceptions.ParameterVersionNotFound:
    raise ValueError("SSM parameter version not found.")
  
  except Exception as e:
    raise ValueError(f"Failed to get SSM parameter: {e}")
  

def send_slack_notification(cost):
  webhook_url = get_ssm_parameter()

  # Slackに送信するメッセージ
  message = {
    "text": f"月初から本日までのAWS使用料は ${cost:.2f} です。"
  }

  # Slack WebhookにPOSTリクエストを送信
  response = requests.post(webhook_url, data = json.dumps(message), headers = {"Content-Type": "application/json"})
  
  if response.status_code != 200:
    raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
