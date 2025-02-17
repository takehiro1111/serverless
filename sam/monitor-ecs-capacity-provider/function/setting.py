import datetime
import json
import os

# AWSアカウントのsetting
## ローカルのパスではなくLambdaだと独自のパスになるため不要。
# file_path = os.path.join(os.path.dirname(__file__), "config.json")
with open("config.json") as accounts:
    config = json.load(accounts)

IAM_ROLE_NAME_MONITOR_ECS = config.get("DEFAULT_ROLE_NAME")
DEFAULT_REGION = config.get("DEFAULT_REGION")
ACCOUNTS = config.get("ACCOUNTS")

# SSMパラメータストア
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")
