package main

import (
	"strings"
	"testing"
)

func TestBuildMessage(t *testing.T) {
	got := buildMessage("123456789012", []finding{
		{Region: "ap-northeast-1", Service: "EC2 Instance", IDs: []string{"i-aaa (running)"}},
		{Region: "global", Service: "S3 Bucket", IDs: []string{"bucket-a", "bucket-b"}},
	})

	for _, want := range []string{
		"sandbox (123456789012)",
		"*ap-northeast-1 / EC2 Instance* (1)",
		"• i-aaa (running)",
		"*global / S3 Bucket* (2)",
		"• bucket-b",
	} {
		if !strings.Contains(got, want) {
			t.Errorf("message missing %q:\n%s", want, got)
		}
	}
}

func TestTargetRegions(t *testing.T) {
	t.Setenv("AWS_REGION", "ap-northeast-1")

	t.Setenv("TARGET_REGIONS", "")
	if got := targetRegions(); len(got) != 1 || got[0] != "ap-northeast-1" {
		t.Errorf("default: got %v", got)
	}

	t.Setenv("TARGET_REGIONS", "ap-northeast-1, us-east-1,")
	if got := targetRegions(); len(got) != 2 || got[1] != "us-east-1" {
		t.Errorf("csv: got %v", got)
	}
}
