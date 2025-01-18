import csv
import io
from collections import defaultdict

import boto3
from botocore.exceptions import ClientError
from setting import DEFAULT_REGION_NAME, logger

s3 = boto3.resource("s3", region_name=DEFAULT_REGION_NAME)
s3_client = boto3.client("s3", region_name=DEFAULT_REGION_NAME)

def get_s3file(bucket_name, key):
    """S3からファイルを読み込む"""
    try:
        # ファイルの存在確認を効率的に行う
        try:
            s3_client.head_object(Bucket=bucket_name, Key="test.csv")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise FileNotFoundError(
                    f"File not found in S3: bucket={bucket_name}, key={key}"
                )
            else:
                logger.error(f"head error :{e}")
                raise

        s3obj = s3.Object(bucket_name, key).get()
        return io.TextIOWrapper(io.BytesIO(s3obj["Body"].read()))
    except Exception as e:
        logger.error(f"Error reading file from S3: {str(e)}")
        raise


def process_data(file_object):
    """売上データを集計する"""
    try:
        # date と category でグループ化して集計するための辞書
        sales_summary = defaultdict(
            lambda: defaultdict(lambda: {"total_amount": 0, "transaction_count": 0})
        )
        reader = csv.DictReader(file_object)
        
        # ヘッダーの検証
        required_fields = {"date", "category", "amount", "product_name"}
        if not set(reader.fieldnames) >= required_fields:
            missing = required_fields - set(reader.fieldnames)
            raise ValueError(f"Missing required fields: {missing}")

        row_number = 0
        for row in reader:
            row_number += 1
            try:
                date = row["date"].strip()
                category = row["category"].strip()
                
                # 金額を数値に変換
                try:
                    amount = int(row["amount"])
                except ValueError:
                    logger.error(f"Row {row_number}: Invalid amount format: {row['amount']}")
                    continue

                # date と category でグループ化して集計
                sales_summary[date][category]["total_amount"] += amount
                sales_summary[date][category]["transaction_count"] += 1

            except Exception as e:
                logger.error(f"Error processing row {row_number}: {str(e)}")
                continue

        if not sales_summary:
            raise ValueError("No valid data to aggregate")

        logger.info(f"Successfully aggregated {row_number} rows")
        return sales_summary

    except Exception as e:
        logger.error(f"Error processing CSV data: {str(e)}")
        raise


def write_to_s3(bucket_name, key, sales_summary):
    """集計結果をS3に書き込む"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)

        # ヘッダー行を書き込む
        writer.writerow(["date", "category", "total_amount", "transaction_count"])

        # 日付とカテゴリでソートして結果を書き込む
        for date in sorted(sales_summary.keys()):
            for category in sorted(sales_summary[date].keys()):
                writer.writerow([
                    date,
                    category,
                    sales_summary[date][category]["total_amount"],
                    sales_summary[date][category]["transaction_count"]
                ])

        # S3にアップロード
        s3.Object(bucket_name, key).put(
            Body=output.getvalue().encode("utf-8"),
            ContentType='text/csv'
        )
        logger.info(f"Successfully wrote aggregated data to S3: {key}")

    except Exception as e:
        logger.error(f"Error writing to S3: {str(e)}")
        raise
