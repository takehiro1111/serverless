import os
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
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
my_ip_1 = config.get("my_ip_1")
my_ip_2 = config.get("my_ip_2")


####################################################################
# Stack
####################################################################
class NetworkStack(cdk.Stack):

####################################################################
# Constructor
####################################################################
  def __init__(self, scope: cdk.App, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.vpc = self.create_vpc()
    self.subnets = self.create_subnets()
    self.igw = self.create_igw()
    self.eip_nat = self.create_eip_nat()
    self.nat_gw = self.create_nat_gw()
    self.route_tables = self.create_route_tables()
    self.sg = self.create_sg()

####################################################################
# VPC
####################################################################
  def create_vpc(self) -> ec2.CfnVPC:
    return ec2.CfnVPC(self, "cdk_vpc",
    cidr_block=vpc_ip,
      enable_dns_support=True,
      enable_dns_hostnames=True,
      tags=[{
        "key": "Name",
        "value": "cdk_vpc"
      }]
    )

####################################################################
# Subnets
####################################################################
  def create_subnets(self) -> dict:
    subnet_configs = [
      ("cdk_public_a", "10.0.1.0/24", az_1a, True),
      ("cdk_public_c", "10.0.2.0/24", az_1c, True),
      ("cdk_private_a", "10.0.3.0/24", az_1a, False),
      ("cdk_private_c", "10.0.4.0/24", az_1c, False)
    ]
    subnets = {}
    for name, cidr, az, public_ip_bool in subnet_configs:
      subnets[name] = ec2.CfnSubnet(self, name,
        cidr_block=cidr,
        vpc_id=self.vpc.ref,
        availability_zone=az,
        map_public_ip_on_launch=public_ip_bool,
        tags=[{
          "key": "Name",
          "value": name
        }]
      )
    return subnets
  
####################################################################
# IGW
####################################################################
  def create_igw(self) -> ec2.CfnInternetGateway:
    igw = ec2.CfnInternetGateway(self, "cdk_igw",
      tags=[{
        "key": "Name",
        "value": "cdk-igw"
      }])
    ec2.CfnVPCGatewayAttachment(self, "cdk_igw_attach",
      vpc_id=self.vpc.ref,
      internet_gateway_id=igw.ref)
    return igw

####################################################################
# EIP
####################################################################
  def create_eip_nat(self) -> ec2.CfnEIP:
    eip_nat = ec2.CfnEIP(self, "cdk_nat_a_eip",
      domain="vpc"
    )
    return eip_nat

####################################################################
# NAT GW
####################################################################
  def create_nat_gw(self) -> ec2.CfnNatGateway:
    nat_gw = ec2.CfnNatGateway(self, "cdk_nat_gw",
    subnet_id= self.subnets["cdk_public_a"].ref,
    allocation_id = self.eip_nat.attr_allocation_id
    )
    return nat_gw

####################################################################
# Rout Table
####################################################################
  def create_route_tables(self) -> dict:
    rtb_configs = {
      "public": ("cdk-public", self.igw.ref),
      "private": ("cdk-private", self.nat_gw.ref)
    }
    rtb = {}
    for name, (rtb_name, gateway_id) in rtb_configs.items():
      rtb[name] = ec2.CfnRouteTable(self, rtb_name,
        vpc_id=self.vpc.ref,
        tags=[{
          "key": "Name",
          "value": f"{rtb_name}-test"
        }]
      )
      if gateway_id:
        ec2.CfnRoute(self, f"{name}_route_cdk",
          route_table_id=rtb[name].ref,
          gateway_id=gateway_id if name == "public" else None,
          nat_gateway_id=gateway_id if name == "private" else None,
          destination_cidr_block=full_open_ip
        )

    associations = [
      ("public", "cdk_public_a"),
      ("public", "cdk_public_c"),
      ("private", "cdk_private_a"),
      ("private", "cdk_private_c")
    ]
    for rtb_name, subnet_name in associations:
      ec2.CfnSubnetRouteTableAssociation(self, f"{subnet_name}_route_associate",
        route_table_id=rtb[rtb_name].ref,
        subnet_id=self.subnets[subnet_name].ref
      )
    return rtb

####################################################################
# Security Group
####################################################################
  def create_sg(self) -> ec2.CfnSecurityGroup:
    sg = ec2.CfnSecurityGroup(self, "cdk_web",
      group_name="cdk-ou",
      group_description="Python-based CDK",
      vpc_id=self.vpc.ref,
      tags=[{
        "key": "Name",
        "value": "cdk-sg"
      }])

    sg_params = [
      {"constract": "my-ip1", "protocol": "tcp", "from_port": 443, "to_port": 443, "cidr_ip": my_ip_1},
      {"constract": "my-ip2", "protocol": "tcp", "from_port": 443, "to_port": 443, "cidr_ip": my_ip_2}
    ]

    for ingress_cidr in sg_params:
      ec2.CfnSecurityGroupIngress(self, ingress_cidr["constract"],
        group_id=sg.attr_group_id,
        ip_protocol=ingress_cidr["protocol"],
        from_port=ingress_cidr["from_port"],
        to_port=ingress_cidr["to_port"],
        cidr_ip=ingress_cidr["cidr_ip"])

    ec2.CfnSecurityGroupIngress(self, "ingress-cdn",
      group_id=sg.attr_group_id,
      ip_protocol="tcp",
      source_prefix_list_id=cdn_prefix_id,
      from_port=443,
      to_port=443)

    ec2.CfnSecurityGroupEgress(self, "egress-all-ip-2",
      group_id=sg.attr_group_id,
      ip_protocol="-1",
      cidr_ip=full_open_ip,
      from_port=0,
      to_port=0)
    return sg
