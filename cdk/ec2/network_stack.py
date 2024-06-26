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
vpc_ip = "10.0.0.0/16"


class NetworkStack(cdk.Stack):

    def __init__(self, scope:cdk.App , id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.CfnVPC(self,"cdk_vpc",
            cidr_block = vpc_ip,
            enable_dns_support = True,
            enable_dns_hostnames = True,
            tags=[{
                "key": "Name",
                "value": "cdk_vpc"
            }]
        )

        # Subnet
        cdk_public_a = ec2.CfnSubnet(self, "cdk_public_a",
                cidr_block = "10.0.1.0/24",
                vpc_id = vpc.ref,
                availability_zone = az_1a,
                map_public_ip_on_launch = True,
                tags=[{
                    "key": "Name",
                    "value": "cdk_public_a"
                }]
                )
        
        cdk_public_c = ec2.CfnSubnet(self, "cdk_public_c",
                cidr_block = "10.0.2.0/24",
                vpc_id = vpc.ref,
                availability_zone = az_1c,
                map_public_ip_on_launch = True,
                tags=[{
                    "key": "Name",
                    "value": "cdk_public_c"
                }]
                )
        
        cdk_private_a = ec2.CfnSubnet(self, "cdk_private_a",
                cidr_block = "10.0.3.0/24",
                vpc_id = vpc.ref,
                availability_zone = az_1a,
                map_public_ip_on_launch = False,
                tags=[{
                    "key": "Name",
                    "value": "cdk_private_a"
                }]
                )
        
        cdk_private_c = ec2.CfnSubnet(self, "cdk_private_c",
                cidr_block = "10.0.4.0/24",
                vpc_id = vpc.ref,
                availability_zone = az_1c,
                map_public_ip_on_launch = False,
                tags=[{
                    "key": "Name",
                    "value": "cdk_private_c"
                }]
                )

        # IGW
        cdk_igw = ec2.CfnInternetGateway(self, "cdk_igw",
            tags=[{
                "key":"Name",
                "value":"cdk-igw"
            }]
        )

        # IGW associate VPC
        cdk_igw_attach = ec2.CfnVPCGatewayAttachment(self, "cdk_igw_attach",
            vpc_id= vpc.ref,
            internet_gateway_id= cdk_igw.ref,
        )


        # EIP for NAT GW
        # eip = ec2.CfnEIP(self, "cdk_nat_a_eip",
        #     domain="vpc"
        # )

        # NAT GW
        # nat_gateway = ec2.CfnNatGateway(self, "cdk_nat_gw",
        #     subnet_id= cdk_public_a.ref,
        #     allocation_id = eip.attr_allocation_id
        # )

        # RouteTable
        rtb_public = ec2.CfnRouteTable(self, "cdk_public",
            vpc_id= vpc.ref,

            tags=[{
                "key":"Name",
                "value":"cdk-public-test"
            }]
        )

        rtb_private = ec2.CfnRouteTable(self, "cdk_private_test",
            vpc_id= vpc.ref,

            tags=[{
                "key":"Name",
                "value":"cdk-private-test"
            }]
        )

        # Route
        route_public = ec2.CfnRoute(self, 
            "public_route_cdk",
            route_table_id= rtb_public.ref,
            gateway_id = cdk_igw.ref,
            destination_cidr_block=full_open_ip,
        )

        # route_private = ec2.CfnRoute(self, 
        #     "private_route_cdk",
        #     route_table_id= rtb_private.ref,
        #     nat_gateway_id = nat_gateway.ref,
        #     destination_cidr_block=full_open_ip,
        # )

        # RouteTable assoxiate Subnet
        associate1 = ec2.CfnSubnetRouteTableAssociation(self, "publuc_subnet_route_1a",
                route_table_id = rtb_public.ref,
                subnet_id= cdk_public_a.ref
            )
        
        associate2 = ec2.CfnSubnetRouteTableAssociation(self, "publuc_subnet_route_1c",
                route_table_id = rtb_public.ref,
                subnet_id= cdk_public_c.ref
            )
        
        associate3 = ec2.CfnSubnetRouteTableAssociation(self, "private_subnet_route_1a",
                route_table_id = rtb_private.ref,
                subnet_id= cdk_private_a.ref
            )

        associate4 = ec2.CfnSubnetRouteTableAssociation(self, "private_subnet_route_1c",
                route_table_id = rtb_private.ref,
                subnet_id= cdk_private_c.ref
            )

        # SG
        cfn_sg = ec2.CfnSecurityGroup(self,"cdk_web",
            group_name= "cdk-ou",
            group_description= "Python-based CDK",
            vpc_id = vpc.ref,

            tags=[{
                "key":"Name",
                "value":"cdk-sg"
            }]
        )
        
        # SG Roule
        sg_params = [
            {"constract":"my-ip1","protocol" : "tcp" , "from_port" : 443 ,  "to_port" : 443 , "cidr_ip" : "11.31.11.5/32" },
            {"constract":"my-ip2","protocol" : "tcp" , "from_port" : 443 ,  "to_port" : 443 , "cidr_ip" : "11.34.11.6/32" }
        ]

        for ingress_cidr in sg_params:
            ec2.CfnSecurityGroupIngress(self,ingress_cidr["constract"],
                group_id = cfn_sg.attr_group_id,
                ip_protocol= ingress_cidr["protocol"],
                from_port = ingress_cidr["from_port"],
                to_port = ingress_cidr["to_port"],
                cidr_ip = ingress_cidr["cidr_ip"]
            )

        ec2.CfnSecurityGroupIngress(self,"ingress-cdn",
            group_id = cfn_sg.attr_group_id,
            ip_protocol= "tcp",
            source_prefix_list_id = cdn_prefix_id,
            from_port = 443,
            to_port = 443,
        )

        ec2.CfnSecurityGroupEgress(self,"egress-all-ip-2",
            group_id = cfn_sg.attr_group_id,
            ip_protocol= "-1",
            cidr_ip= full_open_ip,
            from_port = 0,
            to_port = 0,
        )
