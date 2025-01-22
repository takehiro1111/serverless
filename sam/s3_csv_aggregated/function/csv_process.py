"""CSVファイルを加工処理するモジュール."""

import csv
import io
import pprint

import boto3
from botocore.exceptions import ClientError
from setting import logger

s3 = boto3.resource("s3")
s3_client = boto3.client("s3")


def get_s3file(bucket_name: str, key: str) -> str:
    """Read objects from source S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key (str): S3 object key name

    Returns:
        str: CSV data decoded from binary to text.
    """
    try:
        s3obj = s3.Object(bucket_name, key).get()
        print(f"s3obj:{s3obj}")

        # ioモジュール -> バイナリデータとテキストデータの変換を担当
        # io.TextIOWrapper -> バイナリデータをテキストとして扱えるように変換
        # io.BytesIO -> バイト列をファイルライクなオブジェクトに変換する
        # 実際の動作はデコード（バイナリ→テキスト）
        # encoding属性 -> このエンコーディングを使ってデコードするという意味の属性値
        data = io.TextIOWrapper(
            io.BytesIO(s3obj["Body"].read()),
            encoding="utf-8",  # 「UTF-8としてデコードせよ」という指示
        )

        print(f"get_s3file:{data.read()}")
        return data.read()

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            logger.error("key not found")
        else:
            logger.error("Unexpected error message")
        raise


# get_s3file:date,product_name,category,amount
# 2024-01-15,Coffee Beans,Drink,1200
# 2024-01-15,Sandwich,Food,800
# 2024-01-15,Tea,Drink,500
# 2024-01-15,Cake,Food,1500
# 2024-01-16,Coffee Beans,Drink,1400
# 2024-01-16,Sandwich,Food,900


# デコードされたCSVファイルをリスト(辞書)に変換
def read_csv_data(csv_file: str) -> list[dict[str, str]]:
    """Convert CSV content to list of dictionaries.

    Args:
        csv_file (str): Decoded CSV data.

    Returns:
        list[dict[str, str]]: Data that is compiled into a dictionary and then listed.
    """
    try:
        dict_reader = csv.DictReader(csv_file)
        rows = list(dict_reader)
        pprint.pprint(f"read_csv_data:{rows}", width=100)

        return rows

    except csv.Error as e:
        logger.error(f"CSV Error:{e} ")
        raise

    except Exception as e:
        logger.error(f"Exception:{e} ")
        raise


# rows
# [{'amount': '1200', 'category': 'Drink', 'date': '2024-01-15', 'product_name': 'Coffee Beans'},
#  {'amount': '800', 'category': 'Food', 'date': '2024-01-15', 'product_name': 'Sandwich'},
#  {'amount': '500', 'category': 'Drink', 'date': '2024-01-15', 'product_name': 'Tea'},
#  {'amount': '1500', 'category': 'Food', 'date': '2024-01-15', 'product_name': 'Cake'},
#  {'amount': '1400', 'category': 'Drink', 'date': '2024-01-16', 'product_name': 'Coffee Beans'},
#  {'amount': '900', 'category': 'Food', 'date': '2024-01-16', 'product_name': 'Sandwich'}]


# csvを整形
def process_csv_data(process_csv_file: list[dict[str, str]]) -> dict[str, int]:
    """Format CSV data according to specifications.

    Args:
        process_csv_file (list[dict[str, str]]): CSV data stored as a dictionary in a list.

    Returns:
        dict[str, int]: Dictionary-format Data organized by date and amount.
    """
    try:
        reader = process_csv_file

        sales: dict[str, int] = {}
        for old_row in reader:
            date = old_row["date"]
            category = old_row["category"]
            amount = int(old_row["amount"])

            key = f"{date}_{category}"

            if key in sales:
                sales[key] += amount
            else:
                sales[key] = amount
            print(f"process_csv_data:{sales[key]}")

        return sales

    except (KeyError, ValueError) as e:
        logger.error(f"An error occurred while processing the data:{e} ")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred process_csv_data: {e}")
        raise


# sales
# {
# '2024-01-15_Drink': 1700,
# '2024-01-15_Food': 2300,
# '2024-01-16_Drink': 1400,
# '2024-01-16_Food': 90
# }


# 整形後のデータをファイルに書き込み
def convert_dict_to_csv(sales_data: dict[str, str]) -> bytes:
    """Write formatted data to destination.

    Args:
        sales_data (dict[str, str]): Dictionary-format Data organized by date and amount.

    Returns:
        bytes: Formatted and written CSV data.
    """
    try:
        # 1. 新しいCSVファイルを作るための準備
        # io.StringIO() -> 文字列をファイルのように扱うためのクラス
        # メモリ上に文字列データを保持し、ファイルと同じような操作（read, write など）が可能。
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
        # getvalue()メソッド -> StringIO や BytesIO オブジェクトでのみ使用可能,バッファの全内容を取得する。
        # encodeメソッド -> 文字列（str型）オブジェクトでのみ使用可能。文字列をバイト列に変換するメソッド。
        converted_binary_data = output.getvalue().encode("utf-8")
        print(f"convert_dict_to_csv{converted_binary_data.decode()}")
        return converted_binary_data

    except csv.Error as e:
        logger.error(f"CSV Error:{e} ")
        raise

    except io.BlockingIOError as e:
        logger.error(f"BlockingIOError:{e} ")
        raise

    except io.UnsupportedOperation as e:
        logger.error(f"UnsupportedOperation:{e} ")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred convert_dict_to_csv: {e}")
        raise


# S3にアップロード
def upload_to_s3(bucket_name: str, key: str, row: bytes) -> None:
    """Upload to S3 bucket.

    Args:
        bucket_name (str): The Name of Destination S3 Bucket.
        key (str): Destination S3 Key.
        row (bytes): CSV data after processing.

    Raises:
        ValueError: If CSV data is empty or cannot be detected.
    """
    if not row:
        raise ValueError("CSV data is empty")

    try:
        s3_client.put_object(
            Bucket=bucket_name, Key=key, Body=row, ContentType="text/csv"
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            logger.error("key not found")
        else:
            logger.error("Unexpected error message")
        raise

    except s3_client.exceptions.InvalidRequest as e:
        logger.error(f"Invalid request: {e}")
        raise


# デバッグ用
# if __name__ == "__main__":
#     csv_file = get_s3file("event-bucket-csv-src-dev", "raw/test.csv")
#     row = read_csv_data(csv_file)
#     process_csv = process_csv_data(row)
#     convert_csv = convert_dict_to_csv(process_csv)
#     upload_to_s3("event-bucket-csv-src-dev", "deggregate/test.csv", convert_csv)
