"""
S3バケットのリストを取得。
Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListBuckets.html  
"""

import boto3

s3_client = boto3.client('s3',region_name="ap-northeast-1")

response = s3_client.list_buckets(
  MaxBuckets=3,
  BucketRegion='ap-northeast-1'
)

if __name__ == "__main__":
  # print(response['Buckets'][0]["Name"])

  # 複数要素を取得したい場合
  bucket_names = [bucket['Name'] for bucket in response['Buckets']]
  print(bucket_names)
