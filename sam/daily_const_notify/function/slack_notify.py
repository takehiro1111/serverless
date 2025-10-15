import boto3
from logger import logger
from setting import (
    LAST_MONTH,
    NOTIFY_END_DATE,
    NOTIFY_SLACK_CHANNEL,
    NOTIFY_START_DATE,
    SLACK_BOT_TOKEN,
)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackManager:
    def __init__(self) -> None:
        self.slack_token = self._get_ssm_parameter()
        self.client = WebClient(token=self.slack_token)

    @staticmethod
    def _get_ssm_parameter() -> str:
        ssm = boto3.client("ssm", "ap-northeast-1")
        try:
            response = ssm.get_parameter(Name=SLACK_BOT_TOKEN, WithDecryption=True)
            return response["Parameter"]["Value"]
        except ssm.exceptions.ParameterNotFound:
            logger.error("SSM parameter not found.")
            raise
        except ssm.exceptions.ParameterVersionNotFound:
            logger.error("SSM parameter version not found.")
            raise
        except Exception as e:
            logger.error(f"Failed to get SSM parameter: {e}")
            raise

    def send_slack_notification(
        self,
        month_cost: float,
        last_month_cost: float,
        user_service_costs: str = None,
        start_date=NOTIFY_START_DATE,
        end_date=NOTIFY_END_DATE,
        last_month=LAST_MONTH,
        channel=NOTIFY_SLACK_CHANNEL,
    ):
        day = end_date.split("/")[1]
        msg = (
            f"{last_month}月のAWS使用料の合計は `${last_month_cost:.2f}` でした。"
            if int(day) == 1
            else f"{start_date}から{end_date}までのAWS使用料は `${month_cost:.2f}` です。"
        )

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":moneybag: 夕学AWSアカウント",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": msg,
                        },
                    },
                ],
            )

            # コストが発生している場合はスレッドに追加
            if int(day) == 1:
                month_cost = last_month_cost
            if month_cost > 1:
                if response["ok"] and user_service_costs:
                    self._post_traceback_thread(response["ts"], user_service_costs)

            return response["ok"]

        except SlackApiError as e:
            logger.error(f"failed to send cost notification: {e}")
            raise ValueError(f"slack notification failed: {e}")

    def _post_traceback_thread(
        self, thread_ts: str, user_service_costs: str, channel=NOTIFY_SLACK_CHANNEL
    ):
        logger.info(f"user_service_costs: {user_service_costs}")

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                thread_ts=thread_ts,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"ユーザーごとの使用サービス\n```{user_service_costs[:3000]}```",
                        },
                    }
                ],
            )

            if response["ok"]:
                logger.info("posted to thread successfully")
            else:
                logger.error("Failed to post to thread")

        except SlackApiError as e:
            # スレッド投稿失敗はメイン通知の成功に影響しないよう例外は発生させない。
            logger.error(f"Failed to post to thread: {e}")
