package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"strings"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sts"
)

func handler(ctx context.Context) error {
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return fmt.Errorf("load aws config: %w", err)
	}

	ident, err := sts.NewFromConfig(cfg).GetCallerIdentity(ctx, &sts.GetCallerIdentityInput{})
	if err != nil {
		return fmt.Errorf("get caller identity: %w", err)
	}
	accountID := *ident.Account

	ex := exclusion{
		stackName:    os.Getenv("STACK_NAME"),
		functionName: os.Getenv("AWS_LAMBDA_FUNCTION_NAME"),
	}

	var findings []finding
	for i, region := range targetRegions() {
		rcfg := cfg.Copy()
		rcfg.Region = region
		fs, err := detectRegional(ctx, rcfg, ex)
		if err != nil {
			return fmt.Errorf("detect in %s: %w", region, err)
		}
		findings = append(findings, fs...)
		if i == 0 {
			gs, err := detectGlobal(ctx, rcfg, ex)
			if err != nil {
				return fmt.Errorf("detect global: %w", err)
			}
			findings = append(findings, gs...)
		}
	}

	if len(findings) == 0 {
		slog.Info("no remaining resources", "account", accountID)
		return nil
	}

	slog.Info("remaining resources found", "account", accountID, "services", len(findings))
	return notifySlack(ctx, buildMessage(accountID, findings))
}

func targetRegions() []string {
	var regions []string
	for _, r := range strings.Split(os.Getenv("TARGET_REGIONS"), ",") {
		if r = strings.TrimSpace(r); r != "" {
			regions = append(regions, r)
		}
	}
	if len(regions) == 0 {
		regions = []string{os.Getenv("AWS_REGION")}
	}
	return regions
}

func main() {
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))
	lambda.Start(handler)
}
