"""
処理順序    
    - 
"""

import boto3
import tempfile
import os
import zipfile
from pathlib import Path

def lambda_handler(event,context):
    s3 = boto3.resource('s3')
    tmpdir=tempfile.TemporaryDirectory();
    for record in event['Records']:
        bucket_name = record["s3"]["bucket"]["name"]
        obj_name = record["s3"]["object"]["key"]
        
        # ファイルにアクセスするためのオブジェクトを取得。
        obj = s3.Object(bucket_name,obj_name)
        
        # ファイル情報の取得
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/object/get.html
        response = obj.get()
        
        # 一時ディレクトリにダウンロード
        # Bodyは実際のデータとなる
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/object/get.html
        src_file = os.path.join(tmpdir.name,obj_name)
        with open(src_file,'wb') as src:
            src.write(response['Body'].read())
            
        # zipfile_name = tempfile.mkstemp(suffix='.zip')
        # os.chdir(tmpdir.name)
        fd, zip_path = tempfile.mkstemp(suffix='.zip')
        os.close(fd) 
        
        # ZIPファイルを作成
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(src_file, os.path.basename(src_file))
        
        # 転送先のバケットへ書き込み。
        # 環境変数からバケット名を取得
        dst_bucket_name = os.environ['OUTPUTBUCKET']
        # ファイル名から拡張子を除いたファイル名を取得
        zip_obj_name = f"{Path(obj_name).stem}.zip"
        # ファイルにアクセスするためのオブジェクトを取得
        obj2 = s3.Object(dst_bucket_name,zip_obj_name )
        
        # アップロード時もwith文で処理
        with open(zip_path, 'rb') as dst:
            response = obj2.put(Body=dst)
            
        # 一時zipファイルの削除（追加）
        os.unlink(zip_path)
        
        tmpdir.cleanup()
            
