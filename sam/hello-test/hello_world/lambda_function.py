import json

def lambda_handler(event,context):
  print('Hello Mr.Tanaka')
  print(json.dumps(event))
