"""S3に保存しているCSVファイルを加工して別バケットに転送するモジュール."""

import json
import urllib.parse
from typing import Any

from csv_process import (
    convert_dict_to_csv,
    get_s3file,
    process_csv_data,
    read_csv_data,
    upload_to_s3,
)
from dynamodb import dynamodb_put_item
from mail import publish_sns
from setting import S3_BUCKET_DST, d_today


def lambda_handler(event: dict[str, Any], context) -> dict[str, int | str]:
    """Process CSV files from source S3 bucket and transfer to destination bucket.

    Args:
        event (dict[str, Any]): S3 Event Metadata.
        context (_type_): Lambda Execution Context.

    Returns:
        dict[str, int | str]: If the operation is successful, status code 200 is returned.
    """
    try:
        # S3のeventをキャッチ
        src_s3 = event["Records"][0]
        bucket_name = src_s3["s3"]["bucket"]["name"]
        #  S3のキー名に日本語を使用する場合を想定したモジュールの使用(文字化けや文字変換系のエラー対策)
        obj_name = urllib.parse.unquote_plus(
            src_s3["s3"]["object"]["key"], encoding="utf-8"
        )
        destination_key = f"deggregate/test-{d_today}.csv"

        # csv_process.py
        # S3からファイルを読み込む
        input_file = get_s3file(bucket_name, obj_name)

        # ファイルからCSVのデータをdistのリストで読み込む。
        src_csv_data = read_csv_data(input_file)

        # srcのデータを整形する。
        process_csv = process_csv_data(src_csv_data)

        # 整形したdictのリストのデータをCSVに変換する。
        convert_csv = convert_dict_to_csv(process_csv)

        # CSVに変換されたため、S3の異なるキーにアップロードする。
        upload_to_s3(S3_BUCKET_DST, destination_key, convert_csv)

        # dynamodb.py
        # CSVファイルを更新した際のメタデータをDynamoDBテーブルにPUTする。
        dynamodb_put_item(
            S3_BUCKET_DST,
            obj_name,
            destination_key,
        )

        # mail.py
        # SNSをpublishしてメールアドレスにファイルが更新されたことを通知。
        publish_sns(d_today, bucket_name, destination_key)

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
