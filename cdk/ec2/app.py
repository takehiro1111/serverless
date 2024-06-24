#!/usr/bin/env python3
import aws_cdk as cdk
from network_stack import NetworkStack
import json

with open('config.json') as conf:
    config = json.load(conf)

app = cdk.App()
account_id = config.get("account_id")
env = cdk.Environment(account= account_id, region= "ap-northeast-1")

print(f'アカウントID:{account_id}')

# ./network_stack.py
NetworkStack(app,"vpc-subnet-stack",env=env)

app.synth()
