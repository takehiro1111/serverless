import json
import boto3
from datetime import datetime,timedelta,timezone
from slack_notify import send_slack_notification

def get_costs():
  client = boto3.client('ce', region_name='us-east-1')
  
  # 現在の日時（UTC）
  now = datetime.now(timezone.utc)

  # 月初の日付を取得（例: 2024-08-01）
  start_date = now.replace(day=1).strftime('%Y-%m-%d')

  # 現在の日付と時刻を取得（例: 2024-08-24）
  end_date = now.date().strftime('%Y-%m-%d')

  # Cost Explorer APIの呼び出し
  response = client.get_cost_and_usage(
      TimePeriod={
          'Start': start_date,
          'End': end_date
      },
      Granularity='DAILY',
      Metrics=['UnblendedCost']
  )

  # コストデータの取得
      # 月初からの合計コストを計算
  total_cost = 0
  for result in response['ResultsByTime']:
      daily_cost = float(result['Total']['UnblendedCost']['Amount'])
      total_cost += daily_cost

  return total_cost


def lambda_handler(event, context):
  # コストを取得してSlackに通知
  cost = get_costs()
  send_slack_notification(cost)

  return {
      'statusCode': 200,
      'body': json.dumps(f"Success Notify Cost Status ")
  }
