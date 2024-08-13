#!bin/bash
# aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1

# aws wafv2 get-web-acl --name {WAFの名称} --scope CLOUDFRONT --region us-east-1 --id {WAFのID} --output json | jq '
#     .WebACL.Rules = (.WebACL.Rules | map({(.Name): .}) | add) |
#     .WebACL.Scope = "CLOUDFRONT"
# ' > events/{waf名}.json



#!/bin/bash

# 作業ディレクトリ
WORKDIR="events"
mkdir -p "$WORKDIR"

# WAFv2 の Web ACL をリストする
web_acls=$(aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1 --query 'WebACLs[*].[Name,Id]' --output text)

# 各 Web ACL の詳細を取得して JSON ファイルに保存する
while read -r name id; do
  echo "Processing Web ACL: $name (ID: $id)"

  aws wafv2 get-web-acl --name "$name" --scope CLOUDFRONT --region us-east-1 --id "$id" --output json | jq '
      .WebACL.Rules = (.WebACL.Rules | map({(.Name): .}) | add) |
      .WebACL.Scope = "CLOUDFRONT"
  ' > "${WORKDIR}/${name}.json"
done <<< "$web_acls"
