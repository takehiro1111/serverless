"""This module sets up the configuration."""

import datetime
import os

import yaml

# config
with open("accounts.yaml") as accounts:
    config = yaml.safe_load(accounts)

ACCOUNTS = config.get("accounts", [])
IAM_ROLE_NAME_MONITOR_ECS = "monitor-ecs-service-capacity-provider"


# environment variables
DEFAULT_REGION = os.environ.get("AWS_REGION")
SSM_PARAMETER_NAME = os.environ.get("SSM_PARAMETER_NAME")

# Get date for slack notification
day = datetime.datetime.now()
weekday = day.strftime("%a")
day_format = day.strftime("%Y/%-m/%-d") + f"({weekday})"
