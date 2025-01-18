import json

from csv_process import get_s3file, process_data, write_to_s3
from dynamodb import dynamodb_put_item
from mail import publish_sns
from setting import date


def lambda_handler(event, context):
    try:
        #######################################################
        # S3 Event
        #######################################################
        # S3のeventをキャッチ
        for record in event["Records"]:
            bucket_name = record["s3"]["bucket"]["name"]
            obj_name = record["s3"]["object"]["key"]
            destination_key = f"deggregate/test-{date}.csv"

            #######################################################
            # CSV
            #######################################################
            print(bucket_name)
            print(obj_name)
            print(destination_key)

            # S3からファイルを読み込む
            input_file = get_s3file(bucket_name, obj_name)

            # CSVのデータを集計する。
            aggregation = process_data(input_file)

            # 集計結果を加工して別のファイルとしてS3に書き込む。
            write_to_s3(bucket_name, destination_key, aggregation)

            #######################################################
            # DynamoDB
            #######################################################
            # CSVファイルを更新した際のメタデータをDynamoDBテーブルにPUTする。
            dynamodb_put_item(
                bucket_name,
                obj_name,
                destination_key,
            )

            #######################################################
            # SNS Publish
            #######################################################
            # SNSをpublishしてメールアドレスにファイルが更新されたことを通知。
            publish_sns()

            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "message": "Lambda Handler Success!!!",
                    }
                ),
            }

    except Exception as e:
        print(e)
        raise
