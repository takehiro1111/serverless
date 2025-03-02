## 目的
- Lambda監視に必要な`CloudwatchLogs SubscriptionFilter`と`Cloudwatch Alarm`をTerraformで管理しているが、追加や削除対応を開発チーム内で完結させるためLambdaでの管理に移行する。
  - コミュニケーションコストの削減により、双方でより重要なタスクへ時間を割くことができる。

## 処理内容
- 作成時
  - `CloudwatchLogs SubscriptionFilter`と`Cloudwatch Alarm`の既存リソースとconfig内のjsonのキー(lambda関数名)を比較し、差分のみにフィルターしてリソースを作成する。

## 懸念点
- 削除対応時にどうするか
  - 別プロジェクトで管理する
