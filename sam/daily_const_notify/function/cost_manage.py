import boto3
from logger import logger


class CostExplorerManager:
    def __init__(self):
        self.client = boto3.client("ce", region_name="us-east-1")
        self.organizations_client = boto3.client(
            "organizations", region_name="us-east-1"
        )

    def _get_account_name(self, account_id: str) -> str:
        """アカウントIDからアカウント名を取得"""
        try:
            response = self.organizations_client.describe_account(AccountId=account_id)
            account_name = response["Account"]["Name"]
            logger.debug(f"Retrieved account name for {account_id}: {account_name}")
            return account_name
        except Exception as e:
            logger.warning(f"Failed to get account name for {account_id}: {e}")
            # フォールバック: アカウントIDの末尾4桁
            fallback_name = f"Account-{account_id[-4:]}"
            return fallback_name

    def get_cost_monthly_total(self, start_date, end_date) -> float:
        response = self.client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            Filter={
                "Not": {
                    "Dimensions": {"Key": "RECORD_TYPE", "Values": ["Refund", "Credit"]}
                }
            },
        )

        monthly_cost = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
        return float(monthly_cost)

    def get_users_by_cost(self, start_date, end_date) -> list:
        response = self.client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"}],
            Filter={
                "Not": {
                    "Dimensions": {"Key": "RECORD_TYPE", "Values": ["Refund", "Credit"]}
                }
            },
        )

        user_costs = []
        for result in response["ResultsByTime"]:
            for group in result["Groups"]:
                account_id = group["Keys"][0]
                cost = float(group["Metrics"]["UnblendedCost"]["Amount"])

                if cost > 1:  # $1ドル以上から収集
                    # アカウント名を取得
                    user_name = self._get_account_name(account_id)
                    user_costs.append(
                        {
                            "account_id": account_id,
                            "user": user_name,  # アカウントIDの末尾4桁
                            "cost": cost,
                        }
                    )

        return sorted(user_costs, key=lambda x: x["cost"], reverse=True)

    def get_cost_by_service_for_users(
        self, start_date, end_date, top_users: list
    ) -> dict:
        """ユーザーのサービス別コストを取得"""
        user_service_costs = {}

        logger.debug(f"top_users: {top_users}")
        for user_info in top_users[:3]:  # 上位3ユーザーのみ
            account_id = user_info["account_id"]

            # 特定アカウントのサービス別コスト
            response = self.client.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
                Filter={
                    "And": [
                        {
                            "Dimensions": {
                                "Key": "LINKED_ACCOUNT",
                                "Values": [account_id],
                            }
                        },
                        {
                            "Not": {
                                "Dimensions": {
                                    "Key": "RECORD_TYPE",
                                    "Values": ["Refund", "Credit"],
                                }
                            }
                        },
                    ]
                },
            )

            services = []
            for result in response["ResultsByTime"]:
                for group in result["Groups"]:
                    service = group["Keys"][0]
                    cost = float(group["Metrics"]["UnblendedCost"]["Amount"])

                    if cost > 0.01:  # $0.01以上のみ
                        services.append({"service": service, "cost": cost})

            # コスト順でソート
            services.sort(key=lambda x: x["cost"], reverse=True)
            user_service_costs[account_id] = {
                "user": user_info["user"],
                "total_cost": user_info["cost"],
                "services": services[:5],  # 上位5サービス
            }

        return user_service_costs

    @staticmethod
    def format_user_details(user_service_costs: dict) -> str:
        logger.info(f"user_service_costs: {user_service_costs}")

        if not user_service_costs:
            return None

        details = []
        for _, user_data in user_service_costs.items():
            user_name = user_data["user"]
            total_cost = user_data["total_cost"]
            services = user_data["services"]

            detail_lines = [f"🤑 {user_name} (${total_cost:.2f})"]
            for i, service in enumerate(services[:3], 1):  # 上位3サービス
                detail_lines.append(
                    f"  {i}. {service['service']}: ${service['cost']:.2f}"
                )

            details.append("\n".join(detail_lines))

        return "\n\n".join(details)
