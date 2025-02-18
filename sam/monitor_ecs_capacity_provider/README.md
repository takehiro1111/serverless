# 処理手順
1. 月-金AM7時にLambda関数を呼び出す。
2. 各アカウントの認証情報を取得。
3. 全アカウントを対象にSTG環境のECSサービスのCapacityProviderStrategyのweightがFARAGATE_SPOTに戻っているか監視しにいく。
  - FARGATE_SPOTの場合は何もしない。
  - FARGATEの場合は、以降の手順へ進む。
  - 例外でFARGATEにしているものはタグで`monitor=False`が入っていればcontinueで処理を抜けさせて対象外にする。
4. Capacity Provider Strategyで以下の割合にする。
  - FARAGATEを0
  - FARGATE_SPOTを1
    - 新しいデプロイメントを強制化する。(タスクが起動していない時間帯のため、必要か要確認)
5. FARGATEから戻し忘れていたECSサービスをSlack通知。


# pipenvで仮想環境の構築（mac）

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
