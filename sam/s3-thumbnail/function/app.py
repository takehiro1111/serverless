"""
処理内容
S3バケットに画像ファイルがアップロードされるとDynamoDBにファイルのメタデータを書き込む。

処理順序
1.srcのS3バケットからファイル情報を取得
2.DynamoDBテーブルに書き込み
3.Slack通知

参考
https://qiita.com/yifey/items/cd97445ecd7085cea444
https://qiita.com/ttkiida/items/6a0c8ea2570821aa7ff8
https://qiita.com/NoriakiOshita/items/2f9e3a16110679e0efac
"""

import json
import logging
import os
import tempfile

import boto3

# 定数
DEFAULT_REGION = "ap-northeast-1"


def get_dynamodb_table():
    dynamodb_client = boto3.resource("dynamodb", region_name=DEFAULT_REGION)
    table_name = dynamodb_client.Table("ThumbnailMetadata").name

    return table_name


def lambda_handler(event, context):
    """ """
    s3_client = boto3.client("s3")
    # S3バケットの取得
    response = s3_client.list_buckets(BucketRegion=DEFAULT_REGION)

    # ファイル情報の取得

    # res = s3_client.get_object(Bucket=bucket, Key=filename)

    # S3バケットのファイルが画像ファイルか精査

    # DynamoDBテーブルへのput items
    table = get_dynamodb_table()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }


# デバッグ用
# if __name__ == "__main__":
#     print(get_dynamodb_table())

#     s3_client = boto3.client('s3')
#     buckets = s3_client.list_buckets()
#     bucket_name = buckets.get('Buckets')
#     bucket = [i.get("Name") for i in bucket_name ]
#     print(bucket)
