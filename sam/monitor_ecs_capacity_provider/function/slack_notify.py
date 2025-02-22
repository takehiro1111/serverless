"""This module provides functions to send notifications to Slack."""

from typing import Any

import boto3
import requests
from logger import logger
from setting import DEFAULT_REGION, SSM_PARAMETER_NAME


class SlackNotify:
    """
    A class for sending notifications to Slack about ECS Capacity Provider status.

    This class manages webhook URL retrieval from SSM Parameter Store and sends notifications
    to Slack when ECS services are running on FARGATE or when errors occur during checks.

    Attributes:
        day_format (str): The formatted date string for the notification
        has_fargate (list[dict[str, Any]]): List of services running on FARGATE
        get_webhook_url (str): The Slack webhook URL retrieved from SSM Parameter Store
    """

    def __init__(self, day_format: str, has_fargate: list[dict[str, Any]]):
        """
        Initialize the SlackNotify instance.

        Args:
            day_format (str): The formatted date string for the notification
            has_fargate (list[dict[str, Any]]): List of services running on FARGATE
        """
        self.day_format = day_format
        self.has_fargate = has_fargate
        self.get_webhook_url = self._get_webhook_url(SSM_PARAMETER_NAME, DEFAULT_REGION)

    @staticmethod
    def _get_webhook_url(ssm_parameter_name: str, region_name: str) -> str:
        """
        Retrieve the Slack webhook URL from SSM Parameter Store.

        Args:
            ssm_parameter_name (str): The name of the SSM parameter containing the webhook URL
            region_name (str): The AWS region where the SSM parameter is stored

        Returns:
            str: The webhook URL for Slack notifications

        Raises:
            ParameterNotFound: If the specified SSM parameter does not exist
            ParameterVersionNotFound: If the specified parameter version does not exist
            Exception: For other unexpected errors
        """
        ssm = boto3.client("ssm", region_name=region_name)
        try:
            response = ssm.get_parameter(
                Name=ssm_parameter_name,
                WithDecryption=True,
            )
            return response["Parameter"]["Value"]

        except ssm.exceptions.ParameterNotFound as e:
            logger.error(f"SSM parameter not found.:{e}")
            raise
        except ssm.exceptions.ParameterVersionNotFound as e:
            logger.error(f"SSM parameter version not found.:{e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred.: {e}")
            raise

    def monitor_result_slack_notification(self) -> None:
        """
        Send a notification to Slack when ECS services are found running on FARGATE.

        This method constructs and sends a formatted message to Slack containing details
        about the ECS services that are running on FARGATE instead of FARGATE_SPOT.

        Raises:
            RequestException: If the request to Slack fails
        """
        try:
            slack_webhook_url = self.get_webhook_url
            result_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{self.day_format}*\n\n*:bell: [INFO] ECS Capacity Provider Fargate detected. *",
                        },
                    },
                    {"type": "divider"},
                ]
            }

            for rule in self.has_fargate:
                ecs_services_list = [i["service"] for i in rule["ecs_service"]]
                ecs_services_str = ",".join(
                    [f"`{service}`" for service in ecs_services_list]
                )
                result_message["blocks"].append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Account:* `{rule['account']}` / *ECS:* {ecs_services_str}",
                        },
                    }
                )

            response = requests.post(
                slack_webhook_url,
                json=result_message,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Slack returned an error: {e}")
            raise

    def error_result_slack_notification(self) -> None:
        """
        Send an error notification to Slack when ECS Capacity Provider check fails.

        This method sends a notification to Slack when an error occurs during the
        ECS Capacity Provider monitoring process.

        Raises:
            RequestException: If the request to Slack fails
        """
        try:
            webhook_url = self.get_webhook_url
            result_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{self.day_format}*\n\n*:no_entry_sign: Error occurred during ECS Capacity Provider check*",
                        },
                    }
                ]
            }
            response = requests.post(
                webhook_url,
                json=result_message,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(
                f"error_result_slack_notification Request to Slack returned an error: {e}"
            )
            raise
