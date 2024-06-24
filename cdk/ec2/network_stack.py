import os
import aws_cdk as cdk
from  aws_cdk import aws_ec2 as ec2
import json


with open('config.json') as conf:
    config = json.load(conf)

account_id = config.get("account_id")
region = config.get("region")
az_1a = config.get("az_1a")
az_1c = config.get("az_1c")
az_1d = config.get("az_1d")
cdn_prefix_id = config.get("cdn_managed_prefix_id")
full_open_ip = "0.0.0.0/0"


class NetworkStack(cdk.Stack):

    def __init__(self, scope:cdk.App , id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.CfnVPC(self,"cdk_vpc",
            cidr_block = "10.0.0.0/16",
            enable_dns_support = True,
            enable_dns_hostnames = True,
            tags=[{
                "key": "Name",
                "value": "cdk_vpc"
            }]
        )

        # ループ対象のサブネットの情報を定義
        subnet_configs = [
            {"name": "cdk_public_a", "cidr": "10.0.5.0/24", "az": az_1a, "public": True},
            {"name": "cdk_public_c", "cidr": "10.0.6.0/24", "az": az_1c, "public": True},
            {"name": "cdk_private_a", "cidr": "10.0.7.0/24", "az": az_1a, "public": False},
            {"name": "cdk_private_c", "cidr": "10.0.8.0/24", "az": az_1c, "public": False},
        ]

        # ループでサブネットを作成
        for subnet_config in subnet_configs:
            ec2.CfnSubnet(self, subnet_config["name"],
                        cidr_block = subnet_config["cidr"],
                        vpc_id = vpc.ref,
                        availability_zone = subnet_config["az"],
                        map_public_ip_on_launch = subnet_config["public"],
                        tags=[{
                            "key": "Name",
                            "value": subnet_config["name"]
                        }]
            )

        # IGW
        cdk_igw = ec2.CfnInternetGateway(self, "cdk_igw",
            tags=[{
                "key":"Name",
                "value":"cdk-igw"
            }]
        )

        # IGWをVPCへアタッチ
        cdk_igw_attach = ec2.CfnVPCGatewayAttachment(self, "cdk_igw_attach",
            vpc_id= vpc.ref,
            internet_gateway_id= cdk_igw.ref,
        )

        
        # SG作成
        cfn_sg = ec2.CfnSecurityGroup(self,"cdk_web",
            group_name= "cdk-web",
            group_description= "Python-based CDK",
            vpc_id = vpc.ref,

            tags=[{
                "key":"Name",
                "value":"cdk-sg"
            }]
        )

        ec2.CfnSecurityGroupIngress(self,"ingress-web",
            group_id = cfn_sg.attr_group_id,
            ip_protocol= "tcp",
            cidr_ip= full_open_ip,
            from_port = 443,
            to_port = 443,
        )

        ec2.CfnSecurityGroupIngress(self,"ingress-cdn",
            group_id = cfn_sg.attr_group_id,
            ip_protocol= "tcp",
            source_prefix_list_id = cdn_prefix_id,
            from_port = 443,
            to_port = 443,
        )

        ec2.CfnSecurityGroupEgress(self,"egress-all",
            group_id = cfn_sg.attr_group_id,
            ip_protocol= "-1",
            cidr_ip= full_open_ip,
            from_port = 0,
            to_port = 0,
        )
