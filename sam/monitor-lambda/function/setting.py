"""This module sets up the configuration."""

import datetime
import json
import os
from pathlib import Path

# environment variables
DEFAULT_REGION = os.environ.get("AWS_REGION")
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")
# ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
ACCOUNT_ID = "685339645368"

print(ACCOUNT_ID)

# setting.pyの絶対パスを取得
current_file = Path(__file__).resolve()
print(current_file)

# setting.pyのディレクトリ（function/）を取得
current_dir = current_file.parent
print(current_dir)

# 親ディレクトリ（プロジェクトルート）に移動してからconfigディレクトリに移動
config_dir = current_dir.parent / "config"
print(config_dir)

# アカウント名の取得
with open(f"{config_dir}/mapping.json") as f:
    config = json.load(f)
print(config)
ACCOUNT_NAME = config["account_mapping"].get(str(ACCOUNT_ID))
print(ACCOUNT_NAME)

# lambda関数名を設定しているjsonファイルの読み込み
with open(f"{config_dir}/{ACCOUNT_NAME}/lambda.json") as f:
    functions = json.load(f)
FUNCTIONS = functions["lambda"]
print(FUNCTIONS)


# Get date for slack notification
today = datetime.datetime.now()
weekday = today.strftime("%a")
day_format = today.strftime("%Y/%-m/%-d") + f"({weekday})"
