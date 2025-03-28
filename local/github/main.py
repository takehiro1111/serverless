import json
import os
import time

import jwt
import requests

# GithubAppのinstallationIDを取得する処理。
# GitHub App設定
app_id = "273743"
private_key_path = "private_key.pem"

# 秘密鍵を読み込む
with open(private_key_path) as f:
    private_key = f.read()


# JWTトークンを生成
def create_jwt():
    now = int(time.time())
    payload = {"iat": now, "exp": now + (10 * 60), "iss": app_id}  # 10分間有効
    token = jwt.encode(payload, private_key, algorithm="RS256")
    print("token", token)
    if isinstance(token, bytes):
        token = token.decode("utf-8")  # Python 3.5 以前の場合必要

    return token


# GitHub APIを呼び出してインストール一覧を取得
jwt_token = create_jwt()
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github.v3+json",
}

response = requests.get("https://api.github.com/app/installations", headers=headers)
installations = response.json()  # レスポンスをJSONとして解析

for installation in installations:
    print(
        f"Installation ID: {installation['id']}, Account: {installation['account']['login']}"
    )
