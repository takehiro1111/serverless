import requests
from bs4 import BeautifulSoup

# HTMLの取得(GET)
req = requests.get("html/sampleGet.html")
req.encoding = req.apparent_encoding  # 日本語の文字化け防止

# HTMLの解析
bsObj = BeautifulSoup(req.text, "html.parser")

# 要素の抽出
items = bsObj.find_all("li")
item = items.find("a").get("href")


if __name__ == "__main__":
    print(item)
