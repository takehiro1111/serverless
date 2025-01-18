# import string

# with open('.env') as f:
#   t = string.Template(f.read())

# contents = t.substitute(datetime="1")
# print(contents)

import boto3

s3 = boto3.resource("s3")
s3obj = s3.Object("event-bucket-csv-src-dev", "raw/test.csv").get()

print(s3obj)
