import aws_cdk as cdk
from  aws_cdk import aws_lambda as _lambda
import json
import os

FUNC = """
import time
from random import choice,randint

def handler(event,context):
  time.sleep(randit(2,5))
  sushi = ["maguro","saba"]
  message = "I like" + choice(sushi)
  print(message)
  return message
"""

class FunctionStack(cdk.Stack):

    def __init__(self, scope:cdk.App , id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        handler = _lambda.Function(self, "cdk_lambda_1",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=_lambda.Code.from_inline(FUNC),
            memory_size = 128,
            timeout=cdk.Duration.minutes(5),
            role = "lambda-execute-role"
        )

