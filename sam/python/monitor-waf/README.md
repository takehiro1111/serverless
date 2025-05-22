# monitor-waf

## プロジェクト概要
- AWS SAMを使用してデプロイするLambda関数を管理します。
- Pythonで書かれた関数を使って、各AWSアカウントに配置している本番用のWAFルール(`RegionalLimit`)が設定されているか監視を行い、
設定されていない場合はSlackに通知を送信します。

## 新規AWSアカウント追加や監視対象のアカウントを削除する場合
- `config.json`ファイルを編集し、以下をリストの要素に追加する。
```json
{
  "account_name": "{アカウント名(識別できるような文字列)}",
  "account_id": "{アカウントID}"
}
```

## WAFを監視対象から除外する設定
- STG,ACC環境に存在するWAFルールを監視対象から除外する場合は、Terraform側で
WAFのリソースに専用のタグを付与する。
```hcl
tags = {
  monitor = "false"
}
```

## ディレクトリ構成,各ファイルの役割
```shell
├── README.md
├── function
│   ├── __init__.py
│   ├── config.json
│   ├── daily_monitor.py
│   ├── requirements.txt
│   └── slack_notify.py
├── samconfig.toml
└── template.yaml

2 directories, 8 files

```
- `function`:Lambda関数及び付随して必要なファイルを置くディレクトリ
  - `__init__.py`: パッケージとして認識させるためのファイル
  - `config.json`: 関数で使用する設定ファイル
  - `daily_monitor.py`: WAFルールを監視するためのコードを記述
  - `slack_notify.py`: Slackへの通知を送信するコードを記述
  - `requirements.txt`: Pythonパッケージの依存関係を定義し、必要なパッケージを記述
- `samconfig.toml`: SAM CLI用のデフォルトのデプロイ設定を定義した設定ファイル
- `template.yaml`: AWSリソースの定義を記述したSAMテンプレートファイル

## パッケージのインストール
```shell
pip install -r function/requirements.txt
```

## ビルド
- 以下オプションを付ける際はDockerデーモンを起動している状態であること。
```shell
sam build --use-container
```

> **Note:**　`--use-container` : ローカル環境での依存関係のインストールやビルド環境がデプロイ先のLambda環境と一致するように、コンテナを使用するためのオプション。

## デプロイ
```shell
sam deploy
```

- 初回デプロイの場合
```shell
sam deploy --guided
```

## テスト
- 未デプロイの状態でローカルのコードをテストしたい場合のコマンド
```shell
sam local invoke MonitorWAFRuleFunction
```

- デプロイ後のコードをテストしたい場合のコマンド
```shell
sam remote invoke MonitorWAFRuleFunction --region ap-northeast-1 --stack-name monitor-waf
```

## リソース並びにスタックの削除
```shell
sam destroy
```
