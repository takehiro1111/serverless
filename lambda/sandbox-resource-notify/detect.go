package main

import (
	"context"
	"fmt"
	"strings"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/cloudformation"
	cfntypes "github.com/aws/aws-sdk-go-v2/service/cloudformation/types"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	ec2types "github.com/aws/aws-sdk-go-v2/service/ec2/types"
	"github.com/aws/aws-sdk-go-v2/service/ecs"
	"github.com/aws/aws-sdk-go-v2/service/eks"
	"github.com/aws/aws-sdk-go-v2/service/elasticloadbalancingv2"
	lambdasvc "github.com/aws/aws-sdk-go-v2/service/lambda"
	"github.com/aws/aws-sdk-go-v2/service/rds"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

const (
	samManagedStackName    = "aws-sam-cli-managed-default"
	samManagedBucketPrefix = "aws-sam-cli-managed-default-samclisourcebucket"
)

type exclusion struct {
	stackName    string
	functionName string
}

type finding struct {
	Region  string
	Service string
	IDs     []string
}

type checker struct {
	service string
	list    func(ctx context.Context, cfg aws.Config, ex exclusion) ([]string, error)
}

var regionalCheckers = []checker{
	{"EC2 Instance", listEC2Instances},
	{"EBS Volume", listEBSVolumes},
	{"Elastic IP", listElasticIPs},
	{"NAT Gateway", listNATGateways},
	{"RDS Instance", listRDSInstances},
	{"RDS Cluster", listRDSClusters},
	{"ELB", listLoadBalancers},
	{"ECS Cluster", listECSClusters},
	{"EKS Cluster", listEKSClusters},
	{"Lambda Function", listLambdaFunctions},
	{"CloudFormation Stack", listCFnStacks},
}

var globalCheckers = []checker{
	{"S3 Bucket", listS3Buckets},
}

func detectRegional(ctx context.Context, cfg aws.Config, ex exclusion) ([]finding, error) {
	return runCheckers(ctx, cfg, ex, regionalCheckers, cfg.Region)
}

func detectGlobal(ctx context.Context, cfg aws.Config, ex exclusion) ([]finding, error) {
	return runCheckers(ctx, cfg, ex, globalCheckers, "global")
}

func runCheckers(ctx context.Context, cfg aws.Config, ex exclusion, checkers []checker, region string) ([]finding, error) {
	var findings []finding
	for _, c := range checkers {
		ids, err := c.list(ctx, cfg, ex)
		if err != nil {
			return nil, fmt.Errorf("%s: %w", c.service, err)
		}
		if len(ids) > 0 {
			findings = append(findings, finding{Region: region, Service: c.service, IDs: ids})
		}
	}
	return findings, nil
}

func listEC2Instances(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	client := ec2.NewFromConfig(cfg)
	input := &ec2.DescribeInstancesInput{
		Filters: []ec2types.Filter{{
			Name:   aws.String("instance-state-name"),
			Values: []string{"pending", "running", "stopping", "stopped"},
		}},
	}
	var ids []string
	p := ec2.NewDescribeInstancesPaginator(client, input)
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, r := range out.Reservations {
			for _, i := range r.Instances {
				ids = append(ids, fmt.Sprintf("%s (%s)", aws.ToString(i.InstanceId), i.State.Name))
			}
		}
	}
	return ids, nil
}

func listEBSVolumes(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := ec2.NewDescribeVolumesPaginator(ec2.NewFromConfig(cfg), &ec2.DescribeVolumesInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, v := range out.Volumes {
			ids = append(ids, fmt.Sprintf("%s (%s, %dGiB)", aws.ToString(v.VolumeId), v.State, aws.ToInt32(v.Size)))
		}
	}
	return ids, nil
}

func listElasticIPs(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	out, err := ec2.NewFromConfig(cfg).DescribeAddresses(ctx, &ec2.DescribeAddressesInput{})
	if err != nil {
		return nil, err
	}
	var ids []string
	for _, a := range out.Addresses {
		ids = append(ids, fmt.Sprintf("%s (%s)", aws.ToString(a.PublicIp), aws.ToString(a.AllocationId)))
	}
	return ids, nil
}

func listNATGateways(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	input := &ec2.DescribeNatGatewaysInput{
		Filter: []ec2types.Filter{{
			Name:   aws.String("state"),
			Values: []string{"pending", "available"},
		}},
	}
	var ids []string
	p := ec2.NewDescribeNatGatewaysPaginator(ec2.NewFromConfig(cfg), input)
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, n := range out.NatGateways {
			ids = append(ids, aws.ToString(n.NatGatewayId))
		}
	}
	return ids, nil
}

func listRDSInstances(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := rds.NewDescribeDBInstancesPaginator(rds.NewFromConfig(cfg), &rds.DescribeDBInstancesInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, d := range out.DBInstances {
			ids = append(ids, fmt.Sprintf("%s (%s)", aws.ToString(d.DBInstanceIdentifier), aws.ToString(d.DBInstanceStatus)))
		}
	}
	return ids, nil
}

func listRDSClusters(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := rds.NewDescribeDBClustersPaginator(rds.NewFromConfig(cfg), &rds.DescribeDBClustersInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, c := range out.DBClusters {
			ids = append(ids, fmt.Sprintf("%s (%s)", aws.ToString(c.DBClusterIdentifier), aws.ToString(c.Status)))
		}
	}
	return ids, nil
}

func listLoadBalancers(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := elasticloadbalancingv2.NewDescribeLoadBalancersPaginator(
		elasticloadbalancingv2.NewFromConfig(cfg), &elasticloadbalancingv2.DescribeLoadBalancersInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, lb := range out.LoadBalancers {
			ids = append(ids, fmt.Sprintf("%s (%s)", aws.ToString(lb.LoadBalancerName), lb.Type))
		}
	}
	return ids, nil
}

func listECSClusters(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := ecs.NewListClustersPaginator(ecs.NewFromConfig(cfg), &ecs.ListClustersInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, arn := range out.ClusterArns {
			ids = append(ids, arnResourceName(arn))
		}
	}
	return ids, nil
}

func listEKSClusters(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	var ids []string
	p := eks.NewListClustersPaginator(eks.NewFromConfig(cfg), &eks.ListClustersInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		ids = append(ids, out.Clusters...)
	}
	return ids, nil
}

func listLambdaFunctions(ctx context.Context, cfg aws.Config, ex exclusion) ([]string, error) {
	var ids []string
	p := lambdasvc.NewListFunctionsPaginator(lambdasvc.NewFromConfig(cfg), &lambdasvc.ListFunctionsInput{})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, f := range out.Functions {
			name := aws.ToString(f.FunctionName)
			if name == ex.functionName {
				continue
			}
			ids = append(ids, name)
		}
	}
	return ids, nil
}

func listCFnStacks(ctx context.Context, cfg aws.Config, ex exclusion) ([]string, error) {
	var active []cfntypes.StackStatus
	for _, s := range cfntypes.StackStatusCreateComplete.Values() {
		if s != cfntypes.StackStatusDeleteComplete {
			active = append(active, s)
		}
	}
	var ids []string
	p := cloudformation.NewListStacksPaginator(cloudformation.NewFromConfig(cfg),
		&cloudformation.ListStacksInput{StackStatusFilter: active})
	for p.HasMorePages() {
		out, err := p.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, s := range out.StackSummaries {
			name := aws.ToString(s.StackName)
			if name == ex.stackName || name == samManagedStackName || s.ParentId != nil {
				continue
			}
			ids = append(ids, fmt.Sprintf("%s (%s)", name, s.StackStatus))
		}
	}
	return ids, nil
}

func listS3Buckets(ctx context.Context, cfg aws.Config, _ exclusion) ([]string, error) {
	out, err := s3.NewFromConfig(cfg).ListBuckets(ctx, &s3.ListBucketsInput{})
	if err != nil {
		return nil, err
	}
	var ids []string
	for _, b := range out.Buckets {
		name := aws.ToString(b.Name)
		if strings.HasPrefix(name, samManagedBucketPrefix) {
			continue
		}
		ids = append(ids, name)
	}
	return ids, nil
}

func arnResourceName(arn string) string {
	if i := strings.LastIndex(arn, "/"); i >= 0 {
		return arn[i+1:]
	}
	return arn
}
