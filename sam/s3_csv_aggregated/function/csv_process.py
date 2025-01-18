import csv
import io
from collections import defaultdict

import boto3
from setting import DEFAULT_REGION_NAME, logger

s3 = boto3.resource("s3", region_name=DEFAULT_REGION_NAME)
s3_client = boto3.client("s3", region_name=DEFAULT_REGION_NAME)


def get_s3file(bucket_name, key):
    """S3からファイルを読み込む"""
    try:
        if not s3_client.Object(bucket_name, key).load():
            raise FileNotFoundError(
                f"File not found in S3: bucket={bucket_name}, key={key}"
            )

        s3obj = s3.Object(bucket_name, key).get()
        return io.TextIOWrapper(io.BytesIO(s3obj["Body"].read()))
    except Exception as e:
        logger.error(f"Error reading file from S3: {str(e)}")
        raise


def process_data(file_object):
    """売上データを集計する"""
    try:
        sales_summary = defaultdict(
            lambda: defaultdict(lambda: {"total": 0, "count": 0})
        )
        reader = csv.DictReader(file_object)
        for row in reader:
            date = row["date"]
            category = row["category"]
            amount = int(row["amount"])

            sales_summary[date][category]["total"] += amount
            sales_summary[date][category]["count"] += 1

        return sales_summary
    except Exception as e:
        logger.error(f"Error processing CSV data: {str(e)}")
        raise


def write_to_s3(bucket_name, key, sales_summary):
    """集計結果をS3に書き込む"""
    # メモリ上でCSVを作成
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "category", "total_amount", "transaction_count"])

    for date in sorted(sales_summary.keys()):
        for category in sorted(sales_summary[date].keys()):
            writer.writerow(
                [
                    date,
                    category,
                    sales_summary[date][category]["total"],
                    sales_summary[date][category]["count"],
                ]
            )

    # S3にアップロード
    s3.Object(bucket_name, key).put(Body=output.getvalue().encode("utf-8"))
