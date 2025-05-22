"""This module provides functions to send notifications to Slack."""

from typing import Any

import boto3
import requests
from logger import logger
from setting import DEFAULT_REGION, SSM_PARAMETER_NAME


class SlackNotify:
    """Handles Slack notifications for ECS Capacity Provider monitoring."""

    def __init__(self, day_format: str, has_fargate: list[dict[str, Any]]):
        """Initialize with notification data.

        Args:
            day_format: Date string for notification
            has_fargate: List of services running on FARGATE
        """
        self.day_format = day_format
        self.has_fargate = has_fargate
        self.webhook_url = self._get_webhook_url(SSM_PARAMETER_NAME, DEFAULT_REGION)

    @staticmethod
    def _get_webhook_url(ssm_parameter_name: str, region_name: str) -> str:
        """Get Slack webhook URL from SSM Parameter Store.

        Args:
            ssm_parameter_name: SSM parameter name for webhook URL
            region_name: AWS region name

        Returns:
            Slack webhook URL
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

    def _requests_post(self, message: dict[str, Any]) -> None:
        response = requests.post(
            self.webhook_url,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()

    def _create_message(
        self, message_text: str, add_service_info: bool = False
    ) -> dict[str, Any]:
        """Create formatted Slack message.

        Args:
            message_text: Main message text
            add_service_info: Whether to add service information

        Returns:
            Formatted message dictionary
        """
        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{self.day_format}*\n\n{message_text}",
                    },
                },
                {"type": "divider"},
            ]
        }

        if add_service_info and self.has_fargate:
            for rule in self.has_fargate:
                ecs_services_list = [i["service"] for i in rule["ecs_service"]]
                ecs_services_str = ",".join(
                    [f"`{service}`" for service in ecs_services_list]
                )
                message["blocks"].append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Account:* `{rule['account']}` / *ECS:* {ecs_services_str}",
                        },
                    }
                )

        return message

    def monitor_result_slack_notification(self) -> None:
        """Send notification about services running on FARGATE."""
        try:
            message = self._create_message(
                "*:bell: [INFO] ECS Capacity Provider Fargate detected. *",
                add_service_info=True,
            )
            self._requests_post(message)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending monitor notification: {e}")
            raise

    def error_result_slack_notification(self) -> None:
        """Send error notification for monitoring failures."""
        try:
            message = self._create_message(
                "*:no_entry_sign: Error occurred during ECS Capacity Provider check*"
            )
            self._requests_post(message)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending error notification: {e}")
            raise
