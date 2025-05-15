## トリガー
- 以下のS3バケットに対して、`s3:ObjectCreated:*`が発生したタイミングで実行される想定
    - stg: `nextbeat-stats-fluentd-log-stg`
    - prod: `nextbeat-stats-fluentd-log`
- S3とLambdaのトリガー紐づけは、terraformリポジトリの以下で行っている。
    - https://github.com/nextbeat-dev/terraform/blob/master/stats/production/storage.tf#L56-L63

## デプロイ
- パッケージインストール
```
$ npm install

※エラーが出る場合、バージョンによる影響と思われます。
（2023/11/12時点、以下で対応できる）

$ nodebrew ls-remote
→使用可能なverを確認

$ nodebrew install v20.9.0
→LTSバージョンをインストール

$ nodebrew use v20.9.0
→LTSバージョンを使用する

$ npm install
→エラー出ないことを確認する
```

- slsデプロイ実施
```
# ステージング環境
$ sls deploy -s stg

# 本番環境
$ sls deploy -s prod

デプロイ時に以下エラーが出る場合、
Error: `pipenv lock --requirements --keep-outdated` Exited with code 2
pipenvバージョンを固定する必要あり

$ pip install pipenv==2022.8.5
→再度デプロイをしてエラーが発生しないことを確認
```

## Serverless Framework
```

```
