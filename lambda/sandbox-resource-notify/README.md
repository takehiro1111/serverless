# sandbox-resource-notify

sandbox アカウントにリソースが残っていたら、毎週月曜 09:00 (JST) に Slack へ通知する Lambda (Go)。

## 検知対象

- EC2 インスタンス (terminated 以外) / EBS ボリューム / Elastic IP / NAT Gateway
- RDS インスタンス / RDS クラスター
- ELB (ALB / NLB)
- ECS クラスター / EKS クラスター
- Lambda 関数 (自分自身を除く)
- CloudFormation スタック (自分自身と `aws-sam-cli-managed-default` を除く)
- S3 バケット (SAM のデプロイ用バケットを除く)

対象リージョンは `template.yaml` の `TARGET_REGIONS` (カンマ区切り) で指定する。S3 は 1 回だけ確認する。

## Slack

`slack.go` の `slackWebhookURL` / `slackChannel` は仮の値。デプロイ前に実際の値へ置き換える。

## デプロイ

```bash
sam build
sam deploy
```

## ローカル実行

```bash
sam build
sam local invoke SandboxResourceNotifyFunction
```
