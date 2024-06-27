#!/usr/bin/env python3
import aws_cdk as cdk
from network import NetworkStack
import json
from  func import FunctionStack
with open('config.json') as conf:
    config = json.load(conf)

app = cdk.App()
account_id = config.get("account_id")
env = cdk.Environment(account= account_id, region= "ap-northeast-1")

print(f'アカウントID:{account_id}')

# ./network_stack.py
NetworkStack(app,"vpc-subnet-stack",env=env)
FunctionStack(app,"lambda-cdk-stack",env=env)

app.synth()
