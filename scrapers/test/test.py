import requests
from bs4 import BeautifulSoup

url = ""
response = requests.get(url)
html = response.text
# print(response.text)

soup = BeautifulSoup(html, "html.parser")
title = soup.find("title").text
print(title)

# タグで囲まれた情報を取得
# tag_obj = soup.title # 例として<title></title>に括られている内容を取得
# text = tag_obj.string
# tags = soup.


# h2_tags = soup.find_all("h1")
# # print(h2_tag[1])

# h2_all = [i for i in h2_tags]
# print(h2_all)
