# 1.構成
![構成](monitor-ecs-capacity-provider.svg)


# 2.処理手順
1. 月-金PM23時にLambda関数を呼び出す。
2. 各アカウントの認証情報を取得。
3. 全アカウントを対象にSTG環境のECSサービスのCapacityProviderStrategyのweightがFARAGATE_SPOTに戻っているか監視しにいく。
  - FARGATE_SPOTの場合は何もしない。
  - FARGATEの場合は、以降の手順へ進む。
  - 例外でFARGATEにしているものはタグで`monitor_ecs_capacity_provider=false`が入っていればcontinueで処理を抜けさせて対象外にする。
4. Capacity Provider Strategyで以下の割合にする。
  - FARAGATEを0
  - FARGATE_SPOTを1
    - 新しいデプロイメントを強制化する。(タスクが起動していない時間帯のため、必要か要確認)
5. FARGATEから戻し忘れていたECSサービスをSlack通知。

# 3.AWSアカウントの追加・削除時の対応
- AWS アカウントの管理は `accounts.yaml` ファイルを通じて行います。
新しいアカウントの追加や既存アカウントの削除が必要な場合は、以下の手順に従ってください。

```yaml:accounts.yaml
accounts:
  - name: account-name
    id: 123456789012
    # 必要に応じて追加,削除を行う。
```

- AssumeRoleの処理時に必要な設定として以下対応を行う必要があります。
  - `template.yaml`ファイルのLambda実行ロールの`sts_policy`にIAMロールのARNを追記する。
```yaml:template.yaml
# 例
- arn:aws:iam::650251692423:role/monitor-ecs-service-capacity-provider # development
```

# 4.pipenvで仮想環境の構築（mac）

Macで`pipenv`を使用してPython環境を構築する手順は以下の通りです。
`pipenv`は、Pythonのパッケージ管理と仮想環境を統合して扱うツールです。

### 1. Pipenvのインストール
- Homebrewを使って`pipenv`をインストールします。

```bash
brew install pipenv

```

### 3. 仮想環境のアクティベート
- 仮想環境をアクティベートするには、以下のコマンドを実行します。

```bash
pipenv shell

```

### 4. 仮想環境の終了
- 仮想環境を終了するには、以下のコマンドでシェルを抜けます。

```bash
exit

```
