import aws_cdk as cdk
import json
from  aws_cdk import aws_lambda as _lambda
from  aws_cdk import aws_iam as iam

with open('config.json') as conf:
    config = json.load(conf)

account_id = config.get("account_id")

FUNC = """
import time
from random import choice,randint

def handler(event,context):
  time.sleep(randint(2,5))
  sushi = ["maguro","saba"]
  message = "I like" + choice(sushi)
  print(message)
  return message
"""

class FunctionStack(cdk.Stack):

    def __init__(self, scope:cdk.App , id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role_arn = f'arn:aws:iam::{account_id}:role/lambda-execute-role'
        role = iam.Role.from_role_arn(self, "ImportedRole", role_arn)

        handler = _lambda.Function(self, "cdk_lambda_1",
            function_name="sushi-cdk",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=_lambda.Code.from_inline(FUNC),
            memory_size = 128,
            timeout=cdk.Duration.minutes(5),
            role = role
        )
