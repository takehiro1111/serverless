import logging
import time
from datetime import datetime

import boto3

# ロガーを作成
# ロガーを作成
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# StreamHandlerを作成と設定
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

# ロガーにハンドラーを追加
logger.addHandler(stream_handler)


def assume_role(*args, **kwargs):
    """
    各AWSアカウントの認証情報を取得する。
    一時的な検証用のコードのため、IAMロールではなく、認証情報を貼り付ける構成にしている...
    """
    sts = boto3.client("sts")
    # id_info = sts.get_caller_identity()

    # response = sts.assume_role(
    #     RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
    #     RoleSessionName=f"get_s3_object_{account_id}",
    # )
    # credentials = response["Credentials"]

    s3_client = boto3.client(
        "s3",
        # aws_access_key_id=credentials["AccessKeyId"],
        # aws_secret_access_key=credentials["SecretAccessKey"],
        # aws_session_token=credentials["SessionToken"],
    )

    return s3_client


def get_s3_object(*args, **kwargs):
    """
    S3からオブジェクトを取得し、実行時間とレスポンスを表示する

    Args:
        bucket_name (str): S3バケット名
        object_key (str): オブジェクトのキー

    Returns:
        dict: get_objectのレスポンス
    """
    try:
        s3_client = assume_role()

        start_time = time.time()

        response = s3_client.get_object(
            Bucket="hoge",
            Key="fuga",
        )

        # 終了時間を記録と実行時間の計算
        end_time = time.time()
        execution_time = end_time - start_time

        # レスポンスの内容を表示
        logger.info(f"Response metadata: {response['ResponseMetadata']}")
        logger.info(f"Content length: {response['ContentLength']} bytes")
        logger.info(f"Last modified: {response['LastModified']}")

        # 実行時間の表示
        logger.info(f"Execution time: {execution_time:.3f} sec")

        return response["Body"].read()

    except Exception as e:
        logger.error(f"Error: {e}")
        raise


# このファイル名での実行の場合の処理
if __name__ == "__main__":
    BUCKET_NAME = "hoge"
    OBJECT_KEY = "fuga"

    response = get_s3_object(BUCKET_NAME, OBJECT_KEY)
