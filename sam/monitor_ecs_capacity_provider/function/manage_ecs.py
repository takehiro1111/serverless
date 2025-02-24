"""This module provides functions to interact with AWS ECS and manage ECS Capacity Provider Strategy.

It includes functions to assume IAM roles, list ECS clusters and services, and check and update
the ECS Capacity Provider Strategy for services running on FARGATE.
"""

from typing import Any

import boto3
from botocore.exceptions import ClientError
from logger import logger
from setting import DEFAULT_REGION


class ECSManager:
    """Manages AWS ECS services and their Capacity Provider Strategy."""

    def __init__(self, account_name: str, account_id: int, role_name: str):
        """Initialize with AWS account details.

        Args:
            account_name: AWS account name
            account_id: AWS account ID
            role_name: IAM role name to assume
        """
        self.account_name = account_name
        self.account_id = account_id
        self.role_name = role_name
        self.ecs_client = self._assume_role()

    # 各AWSアカウントへクロスアカウントアクセスを行うための権限をAssumeRoleで取得。
    def _assume_role(self) -> boto3.client:
        """Assume IAM role for cross-account access.

        Returns:
            Authenticated ECS client
        """
        sts = boto3.client("sts")
        try:
            # AssumeRoleで一時クレデンシャルを取得。
            response = sts.assume_role(
                RoleArn=f"arn:aws:iam::{str(self.account_id)}:role/{self.role_name}",
                RoleSessionName=f"monitor_ecs_service_{self.account_name}_{str(self.account_id)}",
            )

            # AssumeRoleでクロスアカウントでのアクセスを実行するクライアントを定義。
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
            logger.error(f"An unexpected error occurred sts_assume_role: {e}")
            raise

    # ECSクラスターの一覧を取得。
    def list_ecs_clusters(self) -> list[str]:
        """Get list of ECS clusters.

        Returns:
            List of cluster names
        """
        try:
            ecs_clusters = self.ecs_client.list_clusters()

            stg_cluster_arns = []
            for cluster_arn in ecs_clusters["clusterArns"]:
                # "stg"の文字列が含まれるECSクラスターのみを処理対象に限定する。
                if "stg" in cluster_arn.lower():
                    stg_cluster_arns.append(cluster_arn)

            # ECSクラスターをARNではなくnameで取得したいため。
            cluster_names = [arn.split("/")[-1] for arn in stg_cluster_arns]

            return cluster_names

        except ClientError as e:
            logger.error(f"An unexpected error occurred list_cluster: {e}")
            raise

    # クラスターに対応するECSサービスの一覧を取得。
    def list_ecs_services(self) -> list[str]:
        """Get list of ECS services across all clusters.

        Returns:
            List of service names
        """
        try:
            ecs_cluster_names = self.list_ecs_clusters()
            ecs_service_arn = []

            for cluster in ecs_cluster_names:
                # ECSサービス数が多い場合にページネーションして処理する際のフラグ機能を持つ変数
                next_token = None

                while True:
                    if next_token:
                        response = self.ecs_client.list_services(
                            cluster=cluster, nextToken=next_token
                        )
                    else:
                        response = self.ecs_client.list_services(cluster=cluster)
                    ecs_service_arn.extend(response["serviceArns"])

                    # 次のページがあるかチェック
                    next_token = response.get("nextToken")
                    if not next_token:
                        break

            ecs_service_names = [arn.split("/")[-1] for arn in ecs_service_arn]
            return ecs_service_names

        except self.ecs_client.exceptions.ClusterNotFoundException as e:
            logger.error(f"The specified cluster was not found.: {e}")
            raise
        except self.ecs_client.exceptions.ServerException as e:
            logger.error(f"A 500 server error occurred related to the API call.: {e}")
            raise
        except ClientError as e:
            logger.error(f"An unexpected error occurred get_ecs_service: {e}")
            raise

    # describe_services時にAPIレート制限に引っかからないようECSサービスを10個ずつに分割する処理。
    @staticmethod
    def chunk_list(ecs_chunk_list: list[Any], chunk_size: int = 10) -> list[list[Any]]:
        """
        Split a list into smaller chunks to avoid API rate limits.

        Args:
            ecs_chunk_list: List to be divided into chunks
            chunk_size: Maximum size of each chunk (default: 10)

        Returns:
            list[list[Any]]: List of chunked lists
        """
        chunk_ecs_services = []
        # リストの長さ分繰り返し、chunk_sizeごとに分割
        for i in range(0, len(ecs_chunk_list), chunk_size):
            # i から i+chunk_size までの要素を取得
            chunk = ecs_chunk_list[i : i + chunk_size]
            # 分割したチャンクを結果リストに追加
            chunk_ecs_services.append(chunk)

        # ログ出力
        logger.debug(f"chunk_ecs_services:{chunk_ecs_services}")

        return chunk_ecs_services

    def update_ecs_services(self, cluster: str, service: dict[str, Any]) -> None:
        """Update ECS service capacity provider settings.

        Args:
            cluster: Cluster name
            service: Service details
        """
        self.ecs_client.update_service(
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

    # FargateになっているECSサービスをFargateSpotに戻す処理。
    def update_capacity_provider(
        self,
        cluster: str,
        service: dict[str, Any],
        has_fargate_chunk: list[dict[str, str]],
    ) -> bool:
        """Update service from FARGATE to FARGATE_SPOT.

        Args:
            cluster: Cluster name
            service: Service details
            has_fargate_chunk: List to track updated services

        Returns:
            True if update successful
        """
        try:
            for provider in service.get("capacityProviderStrategy", []):
                # capacityProviderStrategyにて、Fargateが1以上になっている場合はFargateSpotに変更する。
                if (
                    provider["capacityProvider"] == "FARGATE"
                    and provider["weight"] >= 1
                ):
                    has_fargate_chunk.append(
                        {"cluster": cluster, "service": service["serviceName"]}
                    )

                self.update_ecs_services(cluster, service)
            return True

        except self.ecs_client.exceptions.ClusterNotFoundException as e:
            logger.error(f"The specified cluster was not found.: {e}")
            raise
        except self.ecs_client.exceptions.ServiceNotFoundException as e:
            logger.error(f"The specified service was not found.: {e}")
            raise
        except self.ecs_client.exceptions.ServiceNotActiveException as e:
            logger.error(f"The specified service is not active.: {e}")
            raise
        except ClientError as e:
            logger.error(f"An unexpected error occurred update_capacity_provider: {e}")
            raise

    # ECSサービスのタグ情報を取得し、monitor_ecs_capacity_provider = false のタグが存在する場合は処理しない。
    def check_ecs_env(self, cluster, service_batch):
        """Check and update services to use FARGATE_SPOT.

        Args:
            cluster: Cluster name
            service_batch: List of services

        Returns:
            List of updated services
        """
        try:
            response = self.ecs_client.describe_services(
                cluster=cluster, services=service_batch
            )

            has_fargate_chunk = []
            for service in response["services"]:
                tags = self.ecs_client.list_tags_for_resource(
                    resourceArn=service["serviceArn"]
                )["tags"]

                # monitor_ecs_capacity_provider = false のタグが設定されている場合は処理しない。
                if any(
                    tag["key"] == "monitor_ecs_capacity_provider"
                    and tag["value"] == "false"
                    for tag in tags
                ):
                    continue

                # FARGATEの重みを0に、FARGATE_SPOTの重みを1に更新する。
                self.update_capacity_provider(cluster, service, has_fargate_chunk)

            return has_fargate_chunk

        except self.ecs_client.exceptions.InvalidParameterException as e:
            logger.error(
                f"Invalid parameter provided when listing tags for resource: {e}"
            )
            raise
        except ClientError as e:
            logger.error(f"An unexpected error occurred check_ecs_service: {e}")
            raise

    # このModuleでmainの関数
    def main_ecs_processing(
        self, ecs_cluster: list[str], ecs_service: list[str]
    ) -> list[dict[str, str]]:
        """Process ECS services across multiple clusters.

        Args:
            ecs_cluster: List of clusters
            ecs_service: List of services

        Returns:
            List of services running on FARGATE
        """
        try:
            has_fargate_services = []
            for cluster in ecs_cluster:
                service_batches = ECSManager.chunk_list(ecs_service)

                for service_batch in service_batches:
                    has_fargate_services.extend(
                        self.check_ecs_env(cluster, service_batch)
                    )

            return has_fargate_services

        except ClientError as e:
            logger.error(f"An unexpected error occurred check_capacity_provider: {e}")
            raise
