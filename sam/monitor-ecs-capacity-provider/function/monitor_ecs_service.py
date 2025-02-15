import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from logger import logger
from setting import DEFAULT_REGION, IAM_ROLE_NAME_MONITOR_ECS


# IAMの認証
## sre-management(master)アカウントのlambdaから各アカウントのstsでAssumeRoleする。
def sts_assume_role(account_name, account_id, role_name=IAM_ROLE_NAME_MONITOR_ECS):
    sts = boto3.client = "sts"
    try:
        # AssumeRoleで一時クレデンシャルを取得
        response = sts.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
            RoleSessionName=f"monitor_ecs_service_{account_name}_{account_id}",
        )

        temp_credentials = response["Credentials"]

        ecs_client = boto3.client(
            "ecs",
            aws_access_key_id=temp_credentials["Credentials"]["AccessKeyId"],
            aws_secret_access_key=temp_credentials["Credentials"]["SecretAccessKey"],
            aws_session_token=temp_credentials["Credentials"]["SessionToken"],
            region_name=DEFAULT_REGION,
        )

        return ecs_client

    except sts.Client.exceptions.MalformedPolicyDocumentException as e:
        logger.error(f"This is not how to write a valid policy.: {e}")
        raise
    except sts.Client.exceptions.ExpiredTokenException as e:
        logger.error(f"Your credentials have expired.: {e}")
        raise

    except ClientError as e:
        logger.error(f"An unexpected error occurred.: {e}")
        raise


# クラスター名の取得から
def list_ecs_clusters(ecs_client):
    ecs_clusters = ecs_client.list_clusters()

    stg_cluster_arns = []
    for cluster_arn in ecs_clusters["clusterArns"]:
        if "stg" in cluster_arn.lower():
            stg_cluster_arns.append(cluster_arn)

    # ECSクラスターをARNではなく、nameで取得したいため。
    cluster_names = [arn.split("/")[-1] for arn in stg_cluster_arns]

    # STG環境のECSクラスターのarnを返り値とする。
    return cluster_names


# ECSサービス名の取得
def check_capacity_provider(ecs_client):
    assume_role = sts_assume_role()  # configでアカウント情報書いたら引数を入れる！
    ecs_cluster_names = list_ecs_clusters(assume_role)

    ecs_service_arn = []
    for cluster in ecs_cluster_names:
        response = ecs_client.list_services(
            cluster=cluster,
        )
        ecs_service_arn.append(response["serviceArns"])

    # ECSサービスをARNではなく、nameで取得したいため。
    ecs_service_names = [arn.split("/")[-1] for arn in ecs_service_arn]

    # 個々のECSサービス(stg)でキャパシティプロバイダを確認する。
    ## もし、FARGATEのものがあればそのサービス名を出力する。
    has_fargate_services = []
    for cluster_name in ecs_cluster_names:
        for service in ecs_service_names:
            response = ecs_client.describe_services(
                cluster=cluster_name, services=service
            )

            # タグ情報を取得
            tags = ecs_client.list_tags_for_resource(resourceArn=service["serviceArn"])[
                "tags"
            ]

            # 本番環境を除くリソース等は、監視対象から外すよう処理をスキップ
            if any(
                tag["Key"] == "monitor-ecs" and tag["Value"] == "false" for tag in tags
            ):
                continue

            if response["capacityProviderStrategy"]["capacityProvider"] == "FARGATE":
                # タグ情報でignore可否を見にいく。
                if response["capacityProviderStrategy"]["weight"] >= 1:
                    # Slack通知もするため出力用に要素をリストに追加する。
                    has_fargate_services.append(service)

                    # update_ecs_serviceの処理を書く。
                    # 新しいデプロイのAPIは一旦後回し。
                    response = ecs_client.update_service(
                        cluster=cluster_name,
                        service=service,
                        capacityProviderStrategy=[
                            {"capacityProvider": "FARGATE", "weight": 0, "base": 0},
                            {
                                "capacityProvider": "FARGATE_SPOT",
                                "weight": 0,
                                "base": 1,
                            },
                        ],
                    )
    return has_fargate_services


# ECSサービスでキャパシティプロバイダー戦略の監視、必要なら修正
# list_services
# describe_services
# update_service

## 監視と修正の処理の関するを分けるかどうか。
