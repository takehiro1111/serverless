import os

# 定数
S3_BUCKET = os.getenv("S3_BUCKET")
PRODUCT = os.getenv("PRODUCT")
CLUSTERS = os.getenv("CLUSTERS").split(",")
LOG_TYPES = os.getenv("LOG_TYPES").split(",")
