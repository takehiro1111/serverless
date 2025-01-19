# import string

# with open('.env') as f:
#   t = string.Template(f.read())

# contents = t.substitute(datetime="1")
# print(contents)

# import boto3

# s3 = boto3.resource("s3")
# s3obj = s3.Object("event-bucket-csv-src-dev", "raw/test.csv").get()

# print(s3obj)

# row

{
    "date": "2024-01-15",
    "product_name": "Coffee Beans",
    "category": "Drink",
    "amount": "1200",
}
{"date": "2024-01-15", "product_name": "Sandwich", "category": "Food", "amount": "800"}
{"date": "2024-01-15", "product_name": "Tea", "category": "Drink", "amount": "500"}
{"date": "2024-01-15", "product_name": "Cake", "category": "Food", "amount": "1500"}
{
    "date": "2024-01-16",
    "product_name": "Coffee Beans",
    "category": "Drink",
    "amount": "1400",
}
{"date": "2024-01-16", "product_name": "Sandwich", "category": "Food", "amount": "900"}

from setting import d_today

print(d_today)
