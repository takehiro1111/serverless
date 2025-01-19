import json
import urllib.parse

from csv_process import (
    convert_dict_to_csv,
    get_s3file,
    process_csv_data,
    read_csv_data,
    upload_to_s3,
)
from dynamodb import dynamodb_put_item
from mail import publish_sns
from setting import d_today


def lambda_handler(event, context):
    try:
        #######################################################
        # S3 Event
        #######################################################
        # S3のeventをキャッチ
        src_s3 = event["Records"][0]
        bucket_name = src_s3["s3"]["bucket"]["name"]
        obj_name = urllib.parse.unquote_plus(src_s3["s3"]["object"]["key"],encoding='utf-8')
        print(src_s3)
        print(f"urllib前:{src_s3["s3"]["object"]["key"]}")
        print(f"urllib適用後:{urllib.parse.unquote_plus(src_s3["s3"]["object"]["key"],encoding='utf-8')}")
        destination_key = f"deggregate/test-{d_today}.csv"

        #######################################################
        # CSV
        #######################################################
        print(f"bucket_name:{bucket_name}")
        print(f"obj_name:{obj_name}")
        print(f"destination_key:{destination_key}")

        # S3からファイルを読み込む
        input_file = get_s3file(bucket_name, "raw/test.csv")

        # ファイルからCSVのデータをdistのリストで読み込む。
        src_csv_data = read_csv_data(input_file)

        # srcのデータを整形する。
        process_csv = process_csv_data(src_csv_data)

        # 整形したdictのリストのデータをCSVに変換する。
        convert_csv = convert_dict_to_csv(process_csv)

        # CSVに変換されたため、S3の異なるキーにアップロードする。
        upload_to_s3("event-bucket-csv-dst-dev", destination_key, convert_csv)

        #######################################################
        # DynamoDB
        #######################################################
        # CSVファイルを更新した際のメタデータをDynamoDBテーブルにPUTする。
        dynamodb_put_item(
            "event-bucket-csv-dst-dev",
            "raw/test.csv",
            destination_key,
        )

        #######################################################
        # SNS Publish
        #######################################################
        # SNSをpublishしてメールアドレスにファイルが更新されたことを通知。
        publish_sns(d_today,bucket_name,destination_key)

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
