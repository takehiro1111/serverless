import csv
import io
import pprint
from collections import defaultdict

import boto3
from botocore.exceptions import ClientError
from setting import DEFAULT_REGION_NAME, logger

s3 = boto3.resource("s3")
s3_client = boto3.client("s3")


def get_s3file(bucket_name, key):
    s3obj = s3.Object(bucket_name, key).get()
    data = io.TextIOWrapper(io.BytesIO(s3obj["Body"].read()))
    print(data)
    return data


def read_csv_data(csv_file):
    dict_reader = csv.DictReader(csv_file)
    rows = list(dict_reader)
    pprint.pprint(rows, width=100)

    return rows


# csvを整形
def process_csv_data(process_csv_file):
    reader = process_csv_file

    sales = {}

    for old_row in reader:
        date = old_row["date"]
        category = old_row["category"]
        amount = int(old_row["amount"])
        # transaction_count = old_row["date"]

        key = f"{date}_{category}"

        if key in sales:
            sales[key] += amount
        else:
            sales[key] = amount
    print(sales)

    return sales


# CSVに変換
def convert_dict_to_csv(sales_data):
    # 1. 新しいCSVファイルを作るための準備
    output = io.StringIO()
    writer = csv.writer(output)

    # 2. ヘッダー行を書き込む
    writer.writerow(["date", "category", "amount"])

    # 3. 辞書のデータをCSV形式に変換
    for key, amount in sales_data.items():
        # キー（例：'2024-01-15_Drink'）を日付とカテゴリーに分割
        date, category = key.split("_")
        # 1行分のデータを書き込む
        writer.writerow([date, category, amount])

    # 4. 文字列をバイト形式に変換
    print(output.getvalue().encode("utf-8"))
    return output.getvalue().encode("utf-8")


# S3にアップロード
def upload_to_s3(bucket_name, key, row):
    """CSVデータをS3にアップロード"""
    content = row
    if not content:
        raise ValueError("CSV data is empty")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=row,
            # ContentType='text/csv'
        )
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise


if __name__ == "__main__":
    csv_file = get_s3file("event-bucket-csv-src-dev", "raw/test.csv")
    row = read_csv_data(csv_file)
    process_csv = process_csv_data(row)
    convert_csv = convert_dict_to_csv(process_csv)
    upload_to_s3("event-bucket-csv-src-dev", "deggregate/test.csv", convert_csv)


# row
# [{'amount': '1200', 'category': 'Drink', 'date': '2024-01-15', 'product_name': 'Coffee Beans'},
#  {'amount': '800', 'category': 'Food', 'date': '2024-01-15', 'product_name': 'Sandwich'},
#  {'amount': '500', 'category': 'Drink', 'date': '2024-01-15', 'product_name': 'Tea'},
#  {'amount': '1500', 'category': 'Food', 'date': '2024-01-15', 'product_name': 'Cake'},
#  {'amount': '1400', 'category': 'Drink', 'date': '2024-01-16', 'product_name': 'Coffee Beans'},
#  {'amount': '900', 'category': 'Food', 'date': '2024-01-16', 'product_name': 'Sandwich'}]
