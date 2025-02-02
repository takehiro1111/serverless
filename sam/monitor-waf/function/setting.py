import json
import os

# AWSアカウントのsetting
## ローカルのパスではなくLambdaだと独自のパスになるため不要。
# file_path = os.path.join(os.path.dirname(__file__), "config.json")
with open("config.json") as account_setting_file:
    config = json.load(account_setting_file)

MONITOR_WAF_RULE = config.get("DEFAULT_ROLE_NAME")
WAF_REGION = config.get("US_EAST_1")
ACCOUNTS = config.get("ACCOUNTS")

# SSMパラメータストア
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")
SSM_PARAMS_REGION = os.environ.get("SSM_PARAMS_REGION")
