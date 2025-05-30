#!/usr/bin/env python3
import json

import aws_cdk as cdk
from func import FunctionStack
from network import NetworkStack

with open("config.json") as conf:
    config = json.load(conf)

app = cdk.App()
account_id = config.get("account_id")
env = cdk.Environment(account=account_id, region="ap-northeast-1")

print(f"アカウントID:{account_id}")

# ./network_stack.py
network_stack = NetworkStack(
    app,
    "NetworkStack",
    env={"account": config["account_id"], "region": config["region"]},
)

FunctionStack(app, "lambda-cdk-stack", env=env)

app.synth()
