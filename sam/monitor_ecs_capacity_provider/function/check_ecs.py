"""This module provides functions to interact with AWS ECS and manage ECS Capacity Provider Strategy.

It includes functions to assume IAM roles, list ECS clusters and services, and check and update
the ECS Capacity Provider Strategy for services running on FARGATE.
"""

from typing import Any

import boto3
from botocore.exceptions import ClientError
from logger import logger
from setting import DEFAULT_REGION


# 各AWSアカウントへクロスアカウントアクセスを行うための権限をAssumeRoleで取得。
def sts_assume_role(account_name: str, account_id: int, role_name: str) -> boto3.client:
    """
    Assume an IAM role in another AWS account and return an ECS client.

    :param account_name: The name of the AWS account
    :param account_id: The ID of the AWS account
    :param role_name: The name of the IAM role to assume
    :return: An ECS client authenticated with the assumed role
    :raises: Various exceptions if the role assumption fails
    """
    sts = boto3.client("sts")
    try:
        # AssumeRoleで一時クレデンシャルを取得。
        response = sts.assume_role(
            RoleArn=f"arn:aws:iam::{str(account_id)}:role/{role_name}",
            RoleSessionName=f"monitor_ecs_service_{account_name}_{str(account_id)}",
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
def list_ecs_clusters(ecs_client: boto3.client) -> list[str]:
    """
    List ECS clusters in the STG environment.

    :param ecs_client: An authenticated ECS client
    :return: A list of ECS cluster names
    :raises: ClientError if an unexpected error occurs
    """
    try:
        ecs_clusters = ecs_client.list_clusters()

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
def get_ecs_service(ecs_client: boto3.client) -> list[str]:
    """
    List ECS services in the STG environment.

    :param ecs_client: An authenticated ECS client
    :return: A list of ECS service names
    :raises: Various exceptions if the service listing fails
    """
    try:
        ecs_cluster_names = list_ecs_clusters(ecs_client)

        ecs_service_arn = []
        for cluster in ecs_cluster_names:
            response = ecs_client.list_services(
                cluster=cluster,
            )
            # クラスターの中に複数サービスを含むため、データ構造は多次元配列で持つ。
            ecs_service_arn.extend(response["serviceArns"])

        ecs_service_names = [arn.split("/")[-1] for arn in ecs_service_arn]
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


# describe_services時にAPIレート制限に引っかからないようECSサービスを10個ずつに分割する処理。
def chunk_list(ecs_chunk_list: list[Any], chunk_size: int = 10) -> list[list[Any]]:
    """
    Divide a list into smaller chunks.

    :param ecs_chunk_list: The list to be chunked
    :param chunk_size: The size of each chunk (default is 10)
    :return: A list of lists, where each inner list is a chunk
    """
    chunk_ecs_services = [
        ecs_chunk_list[i : i + chunk_size]
        for i in range(0, len(ecs_chunk_list), chunk_size)
    ]
    logger.info(f"chunk_ecs_services:{chunk_ecs_services}")

    return chunk_ecs_services


# FargateになっているECSサービスをFargateSpotに戻す処理。
def update_capacity_provider(
    ecs_client: boto3.client,
    cluster: str,
    service: dict[str, Any],
    has_fargate_chunk: list[dict[str, str]],
) -> bool:
    """
    Update the ECS Capacity Provider Strategy.

    :param ecs_client: An authenticated ECS client
    :param cluster: The name of the ECS cluster
    :param service: The ECS service details
    :param has_fargate_chunk: A list to record services updated from FARGATE to FARGATE_SPOT
    :return: True if the update was successful
    """
    try:
        for provider in service.get("capacityProviderStrategy", []):
            # capacityProviderStrategyにて、Fargateが1以上になっている場合はFargateSpotに変更する。
            if provider["capacityProvider"] == "FARGATE" and provider["weight"] >= 1:
                has_fargate_chunk.append(
                    {"cluster": cluster, "service": service["serviceName"]}
                )

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
        return True

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
        logger.error(f"An unexpected error occurred update_capacity_provider: {e}")
        raise


# ECSサービスのタグ情報を取得し、monitor_ecs_capacity_provider = false のタグが存在する場合は処理しない。
def check_ecs_service(ecs_client, cluster, service_batch):
    """
    Check and update the ECS Capacity Provider Strategy for a batch of ECS services.

    :param ecs_client: An authenticated ECS client
    :param cluster: The name of the ECS cluster
    :param service_batch: A batch of ECS service names
    :return: A list of services that were running on FARGATE
    """
    try:
        response = ecs_client.describe_services(cluster=cluster, services=service_batch)

        has_fargate_chunk = []
        for service in response["services"]:
            tags = ecs_client.list_tags_for_resource(resourceArn=service["serviceArn"])[
                "tags"
            ]

            # monitor_ecs_capacity_provider = false のタグが設定されている場合は処理しない。
            if any(
                tag["key"] == "monitor_ecs_capacity_provider"
                and tag["value"] == "false"
                for tag in tags
            ):
                continue

            # FARGATEの重みを0に、FARGATE_SPOTの重みを1に更新する。
            update_capacity_provider(ecs_client, cluster, service, has_fargate_chunk)

        return has_fargate_chunk

    except ecs_client.exceptions.InvalidParameterException as e:
        logger.error(f"Invalid parameter provided when listing tags for resource: {e}")
        raise
    except ClientError as e:
        logger.error(f"An unexpected error occurred check_ecs_service: {e}")
        raise


def check_capacity_provider(
    ecs_client: boto3.client, ecs_cluster: list[str], ecs_service: list[str]
) -> list[dict[str, Any]]:
    """
    Check and update the ECS Capacity Provider Strategy for services running on FARGATE.

    :param ecs_client: An authenticated ECS client
    :param ecs_cluster: A list of ECS cluster names
    :param ecs_service: A list of ECS service names
    :return: A list of services that were running on FARGATE
    :raises: Various exceptions if the capacity provider check or update fails
    """
    try:
        has_fargate_services = []
        for cluster in ecs_cluster:
            service_batches = chunk_list(ecs_service)

            for service_batch in service_batches:
                has_fargate_services.extend(
                    check_ecs_service(ecs_client, cluster, service_batch)
                )

        return has_fargate_services

    except ClientError as e:
        logger.error(f"An unexpected error occurred check_capacity_provider: {e}")
        raise
