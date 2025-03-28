import time

import jwt
import requests
from cryptography.hazmat.primitives import serialization

# GitHub App の情報
APP_ID = "273743"  # GitHub App の ID
PRIVATE_KEY_PATH = "private_key.pem"  # ダウンロードした .pem ファイル
ORG_NAME = "nextbeat-dev"  # Organization 名

# **1. JWT を作成（GitHub App 認証）**
with open(PRIVATE_KEY_PATH) as f:
    private_key = serialization.load_pem_private_key(f.read().encode(), password=None)

payload = {
    "iat": int(time.time()),  # 発行時間
    "exp": int(time.time()) + (10 * 60),  # 10分間有効
    "iss": APP_ID,
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

# **2. Installation ID を取得**
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json",
}
response = requests.get(
    f"https://api.github.com/orgs/{ORG_NAME}/installation", headers=headers
)

if response.status_code != 200:
    raise Exception(f"Failed to get installation ID: {response.text}")

installation_id = response.json()["id"]

# **3. Installation Token を取得**
token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
response = requests.post(token_url, headers=headers)

if response.status_code != 201:
    raise Exception(f"Failed to get access token: {response.text}")

access_token = response.json()["token"]

# **4. Organization の Owner ID を取得**
org_url = f"https://api.github.com/orgs/{ORG_NAME}"
headers = {
    "Authorization": f"token {access_token}",
    "Accept": "application/vnd.github+json",
}

response = requests.get(org_url, headers=headers)
if response.status_code == 200:
    owner_id = response.json()["node_id"]
    print(f"Organization Owner ID: {owner_id}")
else:
    print(f"Error: {response.status_code}, {response.text}")
