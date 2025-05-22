import gzip
import os
import urllib.request
from datetime import datetime, timedelta
from io import BytesIO
from typing import List

import boto3
import botocore.auth as auth
from botocore.awsrequest import AWSRequest

# 定数
S3_BUCKET = os.getenv("S3_BUCKET")
PRODUCT = os.getenv("PRODUCT")
CLUSTERS = os.getenv("CLUSTERS").split(",")
LOG_TYPES = os.getenv("LOG_TYPES").split(",")

# クライアント
rds_client = boto3.client("rds")
s3_client = boto3.client("s3")

# セッション情報
session = boto3.session.Session()
region = session.region_name
credentials = session.get_credentials()

# SigV4署名
sigv4auth = auth.SigV4Auth(credentials, "rds", region)


# 指定期間内に最終更新されたログファイルの一覧を取得(期間指定はミリ秒)
def get_target_log_file_names(
    instance_name: str, start_time: int, end_time: int
) -> list[str]:
    download_log_file_names = []

    marker = None
    while True:
        params = {
            "DBInstanceIdentifier": instance_name,
            "FileLastWritten": start_time,
            "MaxRecords": 256,
        }
        if marker:
            params["Marker"] = marker

        logs = rds_client.describe_db_log_files(**params)

        download_log_file_names.extend(
            [
                log["LogFileName"]
                for log in logs["DescribeDBLogFiles"]
                if start_time <= log["LastWritten"] < end_time
            ]
        )

        marker = logs.get("Marker")
        if not marker:
            break

    return download_log_file_names


# ログファイルをダウンロードし、圧縮する
def download_and_compress_log(instance_name: str, log_file_name: str) -> BytesIO:
    # 署名付きURLを生成
    host = f"rds.{region}.amazonaws.com"
    url = f"https://{host}/v13/downloadCompleteLogFile/{instance_name}/{log_file_name}"
    awsreq = AWSRequest(method="GET", url=url)
    sigv4auth.add_auth(awsreq)

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": awsreq.headers["Authorization"],
            "Host": host,
            "X-Amz-Date": awsreq.context["timestamp"],
            "X-Amz-Security-Token": credentials.token,
        },
    )

    # ログファイルをダウンロード
    with urllib.request.urlopen(req) as response:
        log_data = response.read()

    # ファイルが空の場合は除外
    if len(log_data) == 0:
        print(f"Log file {log_file_name} is empty. Skipping.")
        return None

    # ログファイルを圧縮
    compressed_data = BytesIO()
    with gzip.GzipFile(fileobj=compressed_data, mode="wb") as f:
        f.write(log_data)
    compressed_data.seek(0)

    return compressed_data


def main(event, context):
    # 最終更新時刻が2時間15分前から1時間前までのログを処理対象とする
    now = datetime.now()
    two_hours_ago = int((now - timedelta(hours=2, minutes=15)).timestamp() * 1000)
    one_hour_ago = int((now - timedelta(hours=1)).timestamp() * 1000)

    # クラスター一覧を取得し、ループ処理
    clusters = rds_client.describe_db_clusters(
        Filters=[{"Name": "db-cluster-id", "Values": CLUSTERS}]
    )
    for cluster in clusters["DBClusters"]:
        cluster_name = cluster["DBClusterIdentifier"]

        print(f"Processing cluster: {cluster_name}")

        # インスタンス一覧を取得し、ループ処理
        instances = cluster["DBClusterMembers"]
        for instance in instances:
            instance_name = instance["DBInstanceIdentifier"]
            print(f"Processing instance: {instance_name}")

            # 対象のログファイル一覧を取得し、ループ処理
            target_log_file_names = get_target_log_file_names(
                instance_name, two_hours_ago, one_hour_ago
            )
            for log_file_name in target_log_file_names:
                log_type = log_file_name.split("/")[0]

                # ログ種別が対象の場合のみ処理を続行
                if log_type not in LOG_TYPES:
                    continue

                print(f"Processing log file: {log_file_name}")

                # S3オブジェクトキーを生成
                if log_type == "audit":
                    timestamp = datetime.strptime(
                        log_file_name.split(".")[3], "%Y-%m-%d-%H-%M"
                    )
                    object_key = f"{PRODUCT}/{cluster_name}/{log_type}/{timestamp.year}/{timestamp.month:02}/{timestamp.day:02}/{timestamp.hour:02}/{instance_name}/{log_file_name.split('/')[-1]}.gz"
                elif log_type in ["error", "slowquery"]:
                    timestamp = datetime.strptime(
                        log_file_name.split(".")[2], "%Y-%m-%d"
                    )
                    object_key = f"{PRODUCT}/{cluster_name}/{log_type}/{timestamp.year}/{timestamp.month:02}/{timestamp.day:02}/{log_file_name.split('.')[3]}/{instance_name}/{log_file_name.split('/')[-1]}.gz"

                # S3で同一のファイル名が存在するか確認
                try:
                    s3_client.head_object(Bucket=S3_BUCKET, Key=object_key)
                    print(f"File already exists in S3: {object_key}. Skipped.")
                    continue  # ファイルが存在する場合は、処理をスキップ
                except s3_client.exceptions.ClientError as e:
                    pass  # ファイルが存在しない場合は、処理を続行

                # ダウンロードし、圧縮したログファイルを取得(データが空の場合はスキップ)
                compressed_data = download_and_compress_log(
                    instance_name, log_file_name
                )
                if compressed_data is None:
                    continue

                # S3にアップロード
                s3_client.upload_fileobj(
                    Fileobj=compressed_data, Bucket=S3_BUCKET, Key=object_key
                )

    return {"statusCode": 200, "body": "Log file processing completed."}
