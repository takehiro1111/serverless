import boto3
from botocore.exceptions import ClientError
from logger import logger
from setting import DEFAULT_REGION


# IAMの認証
## sre-management(master)アカウントのlambdaから各アカウントのstsでAssumeRoleする。
def sts_assume_role(account_name, account_id, role_name):
    sts = boto3.client("sts")
    try:
        # AssumeRoleで一時クレデンシャルを取得
        print(f"account_name:{account_name}")
        print(f"account_id:{account_id}")
        response = sts.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
            RoleSessionName=f"monitor_ecs_service_{account_name}_{account_id}",
        )

        ecs_client = boto3.client(
            "ecs",
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
            region_name=DEFAULT_REGION,
        )

        return ecs_client

    except sts.exceptions.MalformedPolicyDocumentException as e:
        logger.error(f"This is not how to write a valid policy.: {e}")
        raise
    except sts.exceptions.ExpiredTokenException as e:
        logger.error(f"Your credentials have expired.: {e}")
        raise
    except ClientError as e:
        logger.error(f"An unexpected error occurred.: {e}")
        raise


# クラスター名の取得から
def list_ecs_clusters(ecs_client):
    try:
        ecs_clusters = ecs_client.list_clusters()

        stg_cluster_arns = []
        for cluster_arn in ecs_clusters["clusterArns"]:
            # stgが含まれるクラスターに限定する。
            if "stg" in cluster_arn.lower():
                stg_cluster_arns.append(cluster_arn)

        # ECSクラスターをARNではなく、nameで取得したいため。
        cluster_names = [arn.split("/")[-1] for arn in stg_cluster_arns]

        # STG環境のECSクラスターのarnを返り値とする。

        print(f"cluster_names:{cluster_names}")
        return cluster_names

    except ClientError as e:
        logger.error(f"An unexpected error occurred list_cluster: {e}")
        raise


# ECSサービス名の取得
def get_ecs_service(ecs_client):
    try:
        ecs_cluster_names = list_ecs_clusters(ecs_client)

        ecs_service_arn = []
        for cluster in ecs_cluster_names:
            response = ecs_client.list_services(
                cluster=cluster,
            )
            # 多次元配列で持つ。
            ecs_service_arn.extend(response["serviceArns"])
        print(f"ecs_service_arn:{ecs_service_arn}")

        # ECSサービスをARNではなく、nameで取得したいため。
        ecs_service_names = [arn.split("/")[-1] for arn in ecs_service_arn]

        print(f"ecs_service_names:{ecs_service_names}")

        return ecs_service_names

    except ecs_client.exceptions.ClusterNotFoundException as e:
        logger.error(f"The specified cluster was not found.: {e}")
        raise
    except ecs_client.exceptions.ServerException as e:
        logger.error(f"A 500 server error occurred related to the API call.: {e}")
        raise
    except ClientError as e:
        logger.error(f"An unexpected error occurred get_ecs_service: {e}")
        raise


# キャパシティプロバイダー戦略の確認 & 必要に応じて修正
def check_capacity_provider(ecs_client, ecs_cluster, ecs_service):
    try:
        # 個々のECSサービス(stg)でキャパシティプロバイダを確認する。
        ## もし、FARGATEのものがあればそのサービス名を出力する。
        has_fargate_services = []
        for cluster in ecs_cluster:
            response = ecs_client.describe_services(
                cluster=cluster, services=ecs_service
            )

            # サービスが見つからない場合はスキップ
            if not response["services"]:
                continue

            # すべてのサービスをループで処理
            for service in response["services"]:
                # タグ情報を取得
                tags = ecs_client.list_tags_for_resource(
                    resourceArn=service["serviceArn"]
                )["tags"]

                # 本番環境を除くリソース等は、監視対象から外すよう処理をスキップ
                if any(
                    tag["key"] == "monitor-ecs" and tag["value"] == "false"
                    for tag in tags
                ):
                    continue

                for provider in service.get("capacityProviderStrategy", []):
                    if (
                        provider["capacityProvider"] == "FARGATE"
                        and provider["weight"] >= 1
                    ):
                        has_fargate_services.append(
                            {"cluster": ecs_cluster, "service": service["serviceName"]}
                        )

                        # FARGATEの重みを0に、FARGATE_SPOTの重みを1に更新
                        ecs_client.update_service(
                            cluster=cluster,
                            service=service["serviceName"],
                            forceNewDeployment=True,
                            capacityProviderStrategy=[
                                {"capacityProvider": "FARGATE", "weight": 0, "base": 0},
                                {
                                    "capacityProvider": "FARGATE_SPOT",
                                    "weight": 1,
                                    "base": 0,
                                },
                            ],
                        )
                        print(f"Faragate ECS Service:{service['serviceName']}")
        return has_fargate_services

    except ecs_client.exceptions.ClusterNotFoundException as e:
        logger.error(f"The specified cluster was not found.: {e}")
        raise
    except ecs_client.exceptions.ServiceNotFoundException as e:
        logger.error(f"The specified service was not found.: {e}")
        raise
    except ecs_client.exceptions.ServiceNotActiveException as e:
        logger.error(f"The specified service is not active.: {e}")
        raise
    except ClientError as e:
        logger.error(f"The specified cluster was not found.: {e}")
        raise
